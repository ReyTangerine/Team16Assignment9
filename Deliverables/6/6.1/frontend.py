from GameTools import Game
import sys
import json
import socket

d = json.JSONDecoder()
e = json.JSONEncoder()
s = socket.socket()         # Create a socket object

# input = d.decode(str)
hostandport = sys.stdin.read()

hostandport = d.decode(hostandport)
### network-config::= { "host" : string, "port" : number }
host = hostandport["host"]
port = hostandport["port"]

s.connect((host, port))
while 1:
    jsoninput = s.recv(1024)
    input = d.decode(jsoninput.decode())

    ### Was used for testing code (input 1)
    #board = {"black":["bar",2,2,2,2,4,5,6,7,13,13,13,13,24,24],"white":["bar","bar",12,12,12,12,12,17,17,17,19,19,19,19,19]}
    #input = {"take-turn" : [board, [2,2,2,2]]}

    if isinstance(input, str):
        request = input
    elif isinstance(input, dict):
        keysList = list(input.keys())
        request = keysList[0]
        valuesList = list(input.values())
        info = valuesList[0]

    if request == "name":
        newGame = Game("playerInputted")
        newName = "playerInputted"
        answer = {"name":newName}
    elif request == "start-game":
        ### { "start-game" : [ color(your color at initialization), string(opponent player name) ] } --> "okay"
        newGame.set_player_fields(info[0], info[1])
        answer = "okay"
    elif request == "take-turn":
        ### { "take-turn" : [ board, dice ] } --> { "turn" : [ [ cpos, cpos ], ... ] }
        # newGame = Game("player1", "player2")
        newGame.set_board(info[0])
        newKey = newGame.turn(info[1])
        answer = {"turn":newKey}
    elif request == "end-game":
        ### { "end-game" : [ board, boolean ] } --> "okay"
        # newGame = Game("player1", "player2")
        newGame.set_board(info[0])
        newGame.p1.end_game(info[0], info[1]) ## returns null but ends game for player 1
        newGame.p2.end_game(info[0], info[1])  ## returns null but ends game for player 2
        answer = "okay"

    json_answer = e.encode(answer)
    s.sendall(bytes(json_answer + "\n", 'utf-8'))

# s.close()

