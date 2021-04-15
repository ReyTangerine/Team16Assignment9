import sys
import json
from Backgammon_Class import BackgammonBoard

d = json.JSONDecoder()
e = json.JSONEncoder()

str = sys.stdin.read()
input = d.decode(str)

board = BackgammonBoard(input)
print(e.encode(board.answer))