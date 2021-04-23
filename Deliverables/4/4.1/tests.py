import unittest
from Backgammon_Class import Proxy_Backgammon_Board

class GameTest(unittest.TestCase):
    def test1(self):
        x = {"black": [1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 6, "home", "home", "home"], "white": ["bar", "bar", 12, 15, 15, 15, 16, 18, 18, 20, 20, 20, 22, 24, 24]}
        y = ["white", [3, 4], [[12, 16], [15, 18]]]
        board = Proxy_Backgammon_Board(x,y)
        board1 = False
        self.assertEqual(board.getSolution(), board1)

    def test2(self):
        x = {"black": [1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 6, "home", "home", "home"], "white": ["bar", "bar", 12, 15, 15, 15, 16, 18, 18, 20, 20, 20, 22, 24, 24]}
        y = ["black", [2, 6], [[3, 1], [6, "home"]]]
        board = Proxy_Backgammon_Board(x, y)
        board2 = {"black":[1,1,1,2,2,3,4,4,5,5,6,"home","home","home","home"], "white":["bar","bar",12,15,15,15,16,18,18,20,20,20,22,24,24]}
        self.assertEqual(board.getSolution(), board2)

    def test3(self):
        x = {"black":[1,1,2,2,3,3,4,4,5,5,6,6,"home","home","home"], "white":["bar","bar",12,15,15,15,16,18,18,20,20,20,22,24,24]}
        y = ["black", [2,6], [[3,1],[6,12]]]
        board = Proxy_Backgammon_Board(x, y)
        board2 = False
        self.assertEqual(board.getSolution(), board2)

    def test4(self):
        x = {"black":[1,1,2,2,3,3,4,4,5,5,6,6,"home","home","home"], "white":["bar","bar",12,15,15,15,16,18,18,20,20,20,22,24,24]}
        y = ["black", [4,4,4,4], [[6,2],[4,"home"],[5,1],[4,"home"]]]
        board = Proxy_Backgammon_Board(x, y)
        board2 = {"black":[1,1,1,2,2,2,3,3,5,6,"home","home","home","home","home"], "white":["bar","bar",12,15,15,15,16,18,18,20,20,20,22,24,24]}
        self.assertEqual(board.getSolution(), board2)

    def test5(self):
        x = {"black":[2,3,3,3,4,4,4,5,5,6,6,7,"home","home","home"], "white":["bar","bar",12,15,15,15,16,18,18,20,20,20,22,24,24]}
        y = ["white",[1,2],[["bar",1],["bar",2]]]
        board = Proxy_Backgammon_Board(x, y)
        board2 = {"black":["bar",3,3,3,4,4,4,5,5,6,6,7,"home","home","home"], "white":[1,2,12,15,15,15,16,18,18,20,20,20,22,24,24]}
        self.assertEqual(board.getSolution(), board2)

if __name__== "__main__":
    unittest.main()