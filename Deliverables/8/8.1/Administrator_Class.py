from GameTools import Game
from copy import deepcopy
from random import randint
import socket
import json
import sys

d = json.JSONDecoder()
e = json.JSONEncoder()
s = socket.socket()  # Create a socket object

class Admin:
    def __init__(self):
        # PlayerA and PlayerB are currently None objects
        self.playerA = None
        self.playerB = None
        self.playerACheatingBool = False
        self.playerBCheatingBool = False
        self.turnNum = 0

    def setPlayerA(self, name=False, connection=False):
        if name is not False:
            self.playerA = LocalPlayer(name)
        else:
            try:
                self.playerA = RemotePlayer(connection)
                self.playerAName = self.playerA.get_name()
            except CheatingError:
                # self.playerA = LocalPlayer("Malnati")
                self.playerACheatingBool = True
                raise CheatingError("player A's name is invalid. boo.")

    def setPlayerB(self, name=False, connection=False):
        if name is not False:
            self.playerB = LocalPlayer(name)
        else:
            try:
                self.playerB = RemotePlayer(connection)
                self.playerBName = self.playerB.get_name()
            except CheatingError:
                # self.playerB = LocalPlayer("Malnati")
                self.playerBCheatingBool = True
                raise CheatingError("player B's name is invalid. boo.")

    def start_game(self, strategy):
        if self.playerA is None or self.playerB is None:
            raise("Either playerA or playerB has not been initialized")
        ### Determine who's going first
        while True:
            diceA = randint(1, 6)
            diceB = randint(1, 6)
            if diceA > diceB:
                victor = self.playerA
                loser = self.playerB
                self.playerA.set_color("white")
                self.playerB.set_color("black")
                self.turnNum = 0
                break
            elif diceB > diceA:
                victor = self.playerB
                loser = self.playerA
                self.playerB.set_color("white")
                self.playerA.set_color("black")
                self.turnNum = 1
                break
        self.game_instance = Game(victor.get_name(), strategy)
        self.game_instance.set_player_fields("white", loser.get_name())
        self.playerA.start_game(self.playerB.get_name())
        self.playerB.start_game(self.playerA.get_name())

    def roll_dice(self):
        dice = [randint(1, 6), randint(1, 6)]
        # If both rolls are equal, generate 2 more dice with the same value.
        if dice[0] == dice[1]:
            dice.extend(dice)
        return dice

    def playThrough(self):
        while self.is_game_over() is False:
            self.turn()
        if self.turnNum % 2 == 1:
            winnerName = self.playerA.get_name()
            if isinstance(self.playerA, RemotePlayer):
                self.winnerType = "RemotePlayer"
            else:
                self.winnerType = "LocalPlayer"
            A_Status = True
            B_Status = False
        else:
            winnerName = self.playerB.get_name()
            if isinstance(self.playerB, RemotePlayer):
                self.winnerType = "RemotePlayer"
            else:
                self.winnerType = "LocalPlayer"
            A_Status = False
            B_Status = True
        admin_game_over = {"winner-name": winnerName}
        # sys.stdout.flush()
        # print(e.encode(admin_game_over))
        # sys.stdout.flush()
        self.winnerName = winnerName
        self.playerA.end_game(self.game_instance.get_board(), A_Status)
        self.playerB.end_game(self.game_instance.get_board(), B_Status)

    def turn(self):
        dice = self.roll_dice()
        if self.turnNum % 2 == 0:
            # print("White is moving")
            try:
                newGameInstance = self.playerA.turn(dice, self.game_instance)
                self.game_instance = newGameInstance
            except CheatingError:
                oldColor = self.playerA.get_color()
                self.setPlayerA("Malnati")
                self.playerA.set_color(oldColor)
                newGameInstance = self.playerA.turn(dice, self.game_instance)
                self.game_instance = newGameInstance
                self.playerACheatingBool = True
                raise CheatingError("player A's name is invalid. boo.")
        elif self.turnNum % 2 == 1:
            # print("Black is moving")
            try:
                newGameInstance = self.playerB.turn(dice, self.game_instance)
                self.game_instance = newGameInstance
            except CheatingError:
                oldColor = self.playerB.get_color()
                self.setPlayerB("Malnati")
                self.playerB.set_color(oldColor)
                newGameInstance = self.playerB.turn(dice, self.game_instance)
                self.game_instance = newGameInstance
                self.playerBCheatingBool = True
                raise CheatingError("player B's name is invalid. boo.")
        self.turnNum = self.turnNum + 1
        # print(self.game_instance.get_board())

    def get_board(self):
        ourBoard = self.game_instance.get_board()
        return ourBoard

    def is_game_over(self):
        gameInProgress = self.game_instance.gameInProgress
        return not gameInProgress

    ### Please note, this will always return the names so that, in string form
    ### [localPlayer::string, remotePlayer::string]
    def get_names(self):
        p1Name = self.game_instance.p1.get_name()
        p2Name = self.game_instance.p2.get_name()
        return [p1Name,p2Name]

    def set_remote_name(self, name):
        self.game_instance.p2.name = name

    def get_winner_name(self):
        if self.winnerType == "RemotePlayer":
            return self.winnerName
        elif self.winnerType == "LocalPlayer":
            return False

class LocalPlayer:
    def __init__(self, name):
        self.name = name
        self.isCheating = None

    def set_color(self, color):
        self.color = color

    def get_color(self):
        return self.color

    def turn(self, dice, gameInstance):
        move = gameInstance.turn(dice)
        return(gameInstance)

    def get_name(self):
        return(self.name)

    def start_game(self, otherPlayerName):
        pass

    def end_game(self, board, boolean):
        pass

class RemotePlayer:
    def __init__(self, connection):
        self.c = connection
        self.isCheating = False

        #### We ask for name and set the fields here
        self.c.sendall(self.ObjectToJSONBytes("name"))
        ### NameInput :: { "name" : string }
        jsoninput = self.c.recv(1024)
        NameInput = self.JSONBytesToObject(jsoninput)

        ### Checking if input is correct

        if self.Name_Check(NameInput):
            pass
        else:
            self.c.close()
            raise CheatingError("That's not your name!")
        self.name = NameInput["name"]

    def set_color(self, color):
        self.color = color

    def get_color(self):
        return self.color

    def get_name(self):
        return(self.name)

    def start_game(self, otherPlayerName):
        ### Now we tell 'em what their color and their name will be
        ### we must output -> { "start-game" : [ color, string ] }
        start_game_output = {"start-game": [self.color, otherPlayerName]}
        self.c.sendall(self.ObjectToJSONBytes(start_game_output))
        this_should_be_okay = self.c.recv(1024)

    def turn(self, dice, gameInstance):
        board = gameInstance.get_board()
        ### Send them this: { "take-turn" : [ board, dice ] }
        take_turn = {"take-turn": [board, dice]}
        take_turn = self.ObjectToJSONBytes(take_turn)
        self.c.sendall(take_turn)
        ### Receiving this: { "turn" : [ [ cpos, cpos ], ... ] }
        jsoninput = self.c.recv(1024)
        turnDictionary = self.JSONBytesToObject(jsoninput)
        if self.Turn_Check(turnDictionary):
            move = gameInstance.turn(dice, turnDictionary["turn"])
            if move is False:
                self.c.close()
                raise CheatingError("Turn from remote player is invalid")
            return(gameInstance)
        else:
            self.c.close()
            raise CheatingError("Turn from remote player is not a dictionary")

    ### Helper functions to check if turn input are correct
    # checking if the turn arguments are correct
    def Turn_Check(self, turn_input):
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
    def Name_Check(self, name_input):
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

    def ObjectToJSONBytes(self, object):
        JSONThing = e.encode(object)
        return (bytes(JSONThing + "\n", 'utf-8'))

    def JSONBytesToObject(self, Byte):
        return (d.decode(Byte.decode()))

    def end_game(self, board, boolean):
        ### send over the end-game info
        end_game = {"end-game": [board, boolean]}
        self.c.sendall(self.ObjectToJSONBytes(end_game))
        this_is_okay = self.c.recv(1024)
        # self.c.close()

class CheatingError(Exception):
    pass

# newAdmin = Admin()
# newAdmin.setPlayerA("Lou")
# newAdmin.setPlayerB("Malnati")
# newAdmin.start_game("Rando")
# newAdmin.playThrough()
