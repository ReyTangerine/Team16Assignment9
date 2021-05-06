from GameTools import Player, Game
import sys
import json
import socket

d = json.JSONDecoder()
e = json.JSONEncoder()
s = socket.socket()         # Create a socket object

str = sys.stdin.read()
input = d.decode(str)

### network-config::= { "host" : string, "port" : number }
host = str["host"]
port = str["port"]

s.connect((host, port))
print s.recv(1024)
s.close

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


