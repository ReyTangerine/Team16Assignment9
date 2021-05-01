from GameTools import Player, Game
import sys
import json

d = json.JSONDecoder()
e = json.JSONEncoder()

str = sys.stdin.read()
input = d.decode(str)

game = Game("player1", "player2")

board = input[0]
color = input[1]
dice = input[2]

game.set_board(board)
if color == "black":
    game.turnNum = 1

retVal = game.turn(dice)
if retVal is False:
    print(False)
else:
    print(e.encode(retVal))


