import socket
import json
import sys
from copy import deepcopy
from Administrator_Class import Admin

### Helper functions to check if turn input are correct
# checking if the turn arguments are correct
def Turn_Check(turn_input):
    validSpaces = list(range(26))
    validSpaces[0] = "bar"
    validSpaces[25] = "home"
    answerBoolean = True
    if type(turn_input) is dict:
        turns = turn_input.get("turn")
        if turns is None:
            answerBoolean = False
            # raise("incorrect key to dictionary")
        elif type(turns) is not list:
            answerBoolean = False
            # raise("turns is not a list")
        else:
            for turn in turns:
                if len(turn) != 2:
                    answerBoolean = False
                    # raise ("invalid number of cpos in one of the turns")
                else:
                    for cpos in turn:
                        if cpos not in validSpaces:
                            answerBoolean = False
                            # raise ("invalid cpos within one of the turns")
    else:
        answerBoolean = False
        # raise("take-turn is not a dictionary")
    return answerBoolean

# checking if the turn arguments are correct
def Name_Check(name_input):
    answerBoolean = True
    if type(name_input) is dict:
        name = name_input.get("name")
        if name is None:
            answerBoolean = False
            # raise("incorrect key to dictionary")
        elif type(name) is not str:
            answerBoolean = False
            # raise("dictionary value is not a string!")
    else:
        answerBoolean = False
        # raise("name_input is not a dictionary, but instead it's a ", type(name_input))
    return answerBoolean

### Helper functions to convert objects back and forth through connections

def ObjectToJSONBytes(object):
    JSONThing = e.encode(object)
    return (bytes(JSONThing + "\n", 'utf-8'))

def JSONBytesToObject(Byte):
    return (d.decode(Byte.decode()))

### Helper function to play rest of game out

def playGameOut():
    newAdmin.set_remote_name("Malnati")
    while True:
        if newAdmin.is_game_over() is True:
            ### { "end-game" : [ board, boolean ] }
            ### we need to print: admin-game-over ::= { "winner-name" : string }
            winnerName = newAdmin.get_names()
            winnerName = winnerName[1]
            admin_game_over = {"winner-name":winnerName}
            print(e.encode(admin_game_over))
            break
        else:
            ### Local player now plays out turn
            localDice = newAdmin.roll_dice()
            newAdmin.turn(localDice)
        if newAdmin.is_game_over() is True:
            ### we need to print: admin-game-over ::= { "winner-name" : string }
            winnerName = newAdmin.get_names()
            winnerName = winnerName[0]
            admin_game_over = {"winner-name": winnerName}
            print(e.encode(admin_game_over))
            break
        else:
            ### Remove player now plays out turn
            dice = newAdmin.roll_dice()
            ### Send them this: { "take-turn" : [ board, dice ] }
            newAdmin.turn(dice)
    sys.exit()

d = json.JSONDecoder()
e = json.JSONEncoder()
s = socket.socket()  # Create a socket object



host = socket.gethostname()  # Get local machine name
## admin-config::= { "local" : local-strategy, "port" : number }
admin_config = sys.stdin.read()
admin_config = d.decode(admin_config)
port = admin_config["port"]  # Reserve a port for your service.
local_strategy = admin_config["local"]

### newAdmin is the class for administrator which will be controlling all players
### newAdmin assumes P1 is white and local
localPlayer = "Lou"
newAdmin = Admin(localPlayer, local_strategy)
s.bind(("", port))  # Bind to the port

# admin-networking-started::="started"
admin_networking_started = e.encode("started")
print(admin_networking_started)
sys.stdout.flush()

s.listen(5)  # Now wait for client connection.

c, addr = s.accept()  # Establish connection with client.


#### We ask for name and set the fields here
c.sendall(ObjectToJSONBytes("name"))
### NameInput :: { "name" : string }
jsoninput = c.recv(1024)
NameInput = JSONBytesToObject(jsoninput)

### Checking if input is correct

if Name_Check(NameInput):
    pass
else:
    newAdmin.start_game("white", "Malnati")
    c.close()
    playGameOut()

try:
    newAdmin.start_game("white", NameInput["name"])
except AssertionError:
    newAdmin.start_game("white", "Malnati")
    c.close()
    playGameOut()


### Now we tell 'em what their color and our name will be
### we must output -> { "start-game" : [ color, string ] }
theirColor = "black"
start_game_output = {"start-game": [theirColor, localPlayer]}
c.sendall(ObjectToJSONBytes(start_game_output))
start_game_output = c.recv(1024)

while True:
    if newAdmin.is_game_over() is True:
        ### we need to print: admin-game-over ::= { "winner-name" : string }
        winnerName = newAdmin.get_names()
        winnerName = winnerName[1]
        admin_game_over = {"winner-name": winnerName}
        print(e.encode(admin_game_over))
        ### { "end-game" : [ board, boolean ] }
        board = newAdmin.get_board()
        end_game = {"end-game": [board, True]}
        c.sendall(ObjectToJSONBytes(end_game))
        break
    else:
        ### Local player now plays out turn
        localDice = newAdmin.roll_dice()
        newAdmin.turn(localDice)
    if newAdmin.is_game_over() is True:
        ### we need to print: admin-game-over ::= { "winner-name" : string }
        winnerName = newAdmin.get_names()
        winnerName = winnerName[0]
        admin_game_over = {"winner-name": winnerName}
        print(e.encode(admin_game_over))
        ### send over the end-game info
        board = newAdmin.get_board()
        end_game = {"end-game": [board, False]}
        c.sendall(ObjectToJSONBytes(end_game))
        break
    else:
        ### Remove player now plays out turn
        board = newAdmin.get_board()
        dice = newAdmin.roll_dice()
        ### Send them this: { "take-turn" : [ board, dice ] }
        take_turn = {"take-turn": [board, dice]}
        take_turn = ObjectToJSONBytes(take_turn)
        c.sendall(take_turn)
        if newAdmin.cheatersNeverProsper is True:
            c.close()
            playGameOut()
        else:
            ### Receiving this: { "turn" : [ [ cpos, cpos ], ... ] }
            jsoninput = c.recv(1024)
            turnDictionary = JSONBytesToObject(jsoninput)
            if Turn_Check(turnDictionary):
                pass
            else:
                c.close()
                playGameOut()
            try:
                move = newAdmin.turn(dice, turnDictionary["turn"])
            except:
                c.close()
                playGameOut()


try:
    c.close()
except:
    pass

