from GameTools import Player, Game
import sys
import json

d = json.JSONDecoder()
e = json.JSONEncoder()

str = sys.stdin.read()
input = d.decode(str)

game = Game("player1", strategy="good")

board = input[0]
color = input[1]
dice = input[2]

game.set_player_fields(color, "player2")
game.set_board(board)

retVal = game.turn(dice)

if retVal is False:
    print(e.encode([]))
else:
    print(e.encode(retVal))


