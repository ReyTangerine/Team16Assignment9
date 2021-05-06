from GameTools import Player, Game
import sys
import json
import socket

d = json.JSONDecoder()
s = socket.socket()         # Create a socket object

# input = d.decode(str)
hostandport = sys.stdin.read()
### network-config::= { "host" : string, "port" : number }
host = hostandport["host"]
port = hostandport["port"]

s.connect((host, port))

input = sys.stdin.read()

print(input)
str = d.decode(input)

s.close()

"""
game = Game("player1", "player2")

board = input[0]
color = input[1]
dice = input[2]

game.set_board(board)
if color == "black":
    game.turnNum = 1

retVal = game.turn(dice)
if retVal is False:
    print(e.encode([]))
else:
    print(e.encode(retVal))
"""


