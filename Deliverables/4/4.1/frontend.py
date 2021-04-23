import sys
import json
from Backgammon_Class import Proxy_Backgammon_Board


def inputdecoder(board, color, dice, move):
    return [board, [color, dice, move]]


d = json.JSONDecoder()
e = json.JSONEncoder()

str = sys.stdin.read()
input = d.decode(str)

board = Proxy_Backgammon_Board(*inputdecoder(*input))

print(e.encode(board.getSolution()))