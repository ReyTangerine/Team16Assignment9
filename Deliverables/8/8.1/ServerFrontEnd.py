import socket
import json
import sys
from copy import deepcopy
from Administrator_Class import Admin


### Helper function to play rest of game out

def playGameOut():
    newAdmin.set_remote_name("Malnati")
    while True:
        if newAdmin.is_game_over() is True:
            ### { "end-game" : [ board, boolean ] }
            ### we need to print: admin-game-over ::= { "winner-name" : string }
            winnerName = newAdmin.get_names()
            winnerName = winnerName[1]
            admin_game_over = {"winner-name": winnerName}
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

s.bind(("", port))  # Bind to the port

s.listen(5)  # Now wait for client connection.
newAdmin = Admin()  # This will print the right thing
c, addr = s.accept()  # Establish connection with client.

### newAdmin is the class for administrator which will be controlling all players
### newAdmin assumes P1 is white and local
localPlayer = "Lou"
local_strategy = admin_config["local"]

newAdmin.setPlayerA(localPlayer)
newAdmin.setPlayerB(connection=c)
newAdmin.start_game(local_strategy)
newAdmin.playThrough()