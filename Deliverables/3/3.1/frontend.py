import sys
import json
from Backgammon_Class import BackgammonBoard

d = json.JSONDecoder()

str = sys.stdin.read()
input = d.decode(str)

board = BackgammonBoard(input)
print(board.answer)