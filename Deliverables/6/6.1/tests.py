import unittest
from Backgammon_Class import Proxy_Backgammon_Board
from frontend import runfile
import json

class GameTest(unittest.TestCase):

    def test1(self):
        e = json.JSONEncoder()
        input = e.encode({"host": "Nan-Desu-Ka.local", "port": 12345})
        runfile(input)
        # self.assertEqual(board, board1)

if __name__== "__main__":
    unittest.main()