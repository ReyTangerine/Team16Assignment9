import unittest
from Backgammon_Class import Proxy_Backgammon_Board

class GameTest(unittest.TestCase):
    """
    def test1(self):
        x = {"black": [1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 6, "home", "home", "home"], "white": ["bar", "bar", 12, 15, 15, 15, 16, 18, 18, 20, 20, 20, 22, 24, 24]}
        board = Proxy_Backgammon_Board(x)
        board.moving("white", [3, 4], [[12, 16], [15, 18]])
        board = board.getSolution()
        board1 = False
        self.assertEqual(board, board1)


    def test2(self):
        x = {"black":[1,1,2,2,3,3,4,4,5,5,6,6,"home","home","home"], "white":["bar","bar",12,15,15,15,16,18,18,20,20,20,22,24,24]}
        board = Proxy_Backgammon_Board(x)
        board.moving("black", [2,6], [[3,1],[6,12]])
        board2 = False
        self.assertEqual(board.getSolution(), board2)

    def test3(self):
        x = {"black":[1,1,2,2,3,3,4,4,5,5,6,6,"home","home","home"], "white":["bar","bar",12,15,15,15,16,18,18,20,20,20,22,24,24]}
        board = Proxy_Backgammon_Board(x)
        board.moving("black", [4,4,4,4], [[6,2],[4,"home"],[5,1],[4,"home"]])
        board2 = {"black":[1,1,1,2,2,2,3,3,5,6,"home","home","home","home","home"], "white":["bar","bar",12,15,15,15,16,18,18,20,20,20,22,24,24]}
        self.assertEqual(board.getSolution(), board2)

    def test4(self):
        x = {"black":[2,3,3,3,4,4,4,5,5,6,6,7,"home","home","home"], "white":["bar","bar",12,15,15,15,16,18,18,20,20,20,22,24,24]}
        board = Proxy_Backgammon_Board(x)
        board.moving("white",[1,2],[["bar",1],["bar",2]])
        board2 = {"black":["bar",3,3,3,4,4,4,5,5,6,6,7,"home","home","home"], "white":[1,2,12,15,15,15,16,18,18,20,20,20,22,24,24]}
        self.assertEqual(board.getSolution(), board2)

    def test11(self):
        x = {"black": [1, 1, 3, 3, 4, 4, 4, 10, 10, 11, 17, 17, 20, "home", "home"],
             "white": ["bar", "bar", 2, 2, 2, 5, 5, 7, 8, 9, 12, 15, "home", "home", "home"]}
        board = Proxy_Backgammon_Board(x)
        board.moving("white", [3, 3, 3, 3], [])
        board = board.getSolution()
        board2 = {"black": [1, 1, 3, 3, 4, 4, 4, 10, 10, 11, 17, 17, 20, "home", "home"],
                  "white": ["bar", "bar", 2, 2, 2, 5, 5, 7, 8, 9, 12, 15, "home", "home", "home"]}
        self.assertEqual(board, board2)



    def test111_0(self):
        x = {"black": [7,7,7,7,7,7,7,7,7,7,7,7,7,7,11],"white": ["bar", "bar", 4, 4,4, 5, 5, 8, 8, 21, 23, 23, "home", "home", "home"]}
        board1 = Proxy_Backgammon_Board(x)
        board = board1.possibleBoard("black", [2,3])
        board2 = [[[11, 9]]]
        self.assertEqual(board, board2)

    def test111_1(self):
        x = {"black": [1, 1, 3, 3, 4, 4, 4, 10, 10, 11, 17, 17, 20, "home", "home"],"white": ["bar", "bar", 2, 2, 2, 5, 5, 7, 8, 9, 12, 15, "home", "home", "home"]}
        board1 = Proxy_Backgammon_Board(x)
        board = board1.possibleBoard("white", [3, 3, 3, 3])
        board2 = []
        self.assertEqual(board, board2)


    def test5(self):
        x = {"black":[2,2,2,2,3,3,4,4,5,5,6,6,"home","home","home"],"white":["bar",12,12,15,15,15,16,18,18,20,20,20,22,24,24]}
        board = Proxy_Backgammon_Board(x)
        board.moving("white",[1,2],[[12,14],["bar",1]])
        board2 = False
        self.assertEqual(board.getSolution(), board2)

    def test6(self):
        x = {"black":["bar", "bar", 1, 2, 3, 4, 5, 6, 7, 7, 7, 7, 7, 8, 9], "white":["bar", 10, 10, 10, 11, 12, 13, 14, 15, 15, 15, 15, 17, 18, 19]}
        board = Proxy_Backgammon_Board(x)
        board.moving("white", [4, 4, 4, 4], [["bar", 4], [4, 8], [8, 12], [12, 16]])
        board_ans = board.getSolution()
        board2 = {"black":["bar", "bar", "bar", "bar", 1, 2, 3, 5, 6, 7, 7, 7, 7, 7, 9], "white":[10, 10, 10, 11, 12, 13, 14, 15, 15, 15, 15, 16, 17, 18, 19]}
        self.assertEqual(board_ans, board2)


    def test7(self):
        x = {"black": [1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 6, "home", "home", "home"], "white": ["bar", "bar", 12, 15, 15, 15, 16, 18, 18, 20, 20, 20, 22, 24, 24]}
        board = Proxy_Backgammon_Board(x)
        board.moving("black", [2, 6], [[3, 1], [6, "home"]])
        board2 = {"black":[1,1,1,2,2,3,4,4,5,5,6,"home","home","home","home"], "white":["bar","bar",12,15,15,15,16,18,18,20,20,20,22,24,24]}
        self.assertEqual(board.getSolution(), board2)


    def test8(self):
        x = {"black":[1,1,1,1,2,2,2,2,2,2,3,3,3,3,5],"white":[20,22,22,22,22,22,23,23,23,23,23,24,24,24,24]}
        board = Proxy_Backgammon_Board(x)
        board.moving("white", [6,4],[[20,"home"],[22,"home"]])
        board2 = {"black":[1,1,1,1,2,2,2,2,2,2,3,3,3,3,5],"white":[22,22,22,22,23,23,23,23,23,24,24,24,24,"home","home"]}
        self.assertEqual(board.getSolution(), board2)

    """
    def test9(self):
        x = {"black":[2,2,2,3,3,3,3,3,14,14,14,14,14,22,23],"white":[9,9,10,10,10,10,10,17,17,17,17,17,17,17,17]}
        board = Proxy_Backgammon_Board(x)
        z = board.possibleBoard("black", [2,1])
        print("ANSWER")
        #for x in z:
        print(z)
        board.moving("black",[1,2],[[23,22],[23,21]])
        board2 = False
        self.assertEqual(board.getSolution(), board2)

    """
    def test10(self):
        x = {"black":[1, "home","home", "home", "home", "home","home", "home", "home", "home", "home", "home", "home", "home", "home"], "white":[20,20,24,24,"home", "home", "home", "home","home", "home", "home", "home","home", "home", "home"]}
        y = ["black", [2,2,2,2], [[1, "home"]]]
        board = Proxy_Backgammon_Board(x, y)
        board2 = {"black":["home", "home","home", "home", "home", "home","home", "home", "home", "home", "home", "home", "home", "home", "home"], "white":[20,20,24,24,"home", "home", "home", "home","home", "home", "home", "home","home", "home", "home"]}
        self.assertEqual(board.getSolution(), board2)

    

    def test12(self):
        x = {"black": [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3], "white": [1, 1, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24]}
        y = ["black", [3, 4], [ [3, "home"], [3, "home"] ] ]
        board = Proxy_Backgammon_Board(x, y)
        board = board.getSolution()
        board2 = {"black": [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, "home", "home"], "white": [1, 1, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24]}
        self.assertEqual(board, board2)

    def test13(self):
        x = {"black":[6,6,6,22,22,22,22,23,23,23,23,24,24,24,24],"white":[1,2,12,16,16,16,17,17,17,18,18,19,19,20,20]}
        y = ["black",[6,4],[[6,2]]]
        board = Proxy_Backgammon_Board(x, y)
        board = board.getSolution()
        board2 = { "black": [2,6,6,22,22,22,22,23,23,23,23,24,24,24,24], "white": ["bar",1,12,16,16,16,17,17,17,18,18,19,19,20,20] }
        self.assertEqual(board, board2)

    ### This is for the final push on Thursday

    def test14(self):
        x = {"black":[12,20,"home","home","home","home","home","home","home","home","home","home","home","home","home"],"white":[6,6,8,8,16,16,"home","home","home","home","home","home","home","home","home"]}
        y = ["black",[2,4],[[20,18]]]
        board = Proxy_Backgammon_Board(x, y)
        board = board.getSolution()
        board2 = False
        self.assertEqual(board, board2)

    def test15(self):
        x = {"black":[1,8,"home","home","home","home","home","home","home","home","home","home","home","home","home"],"white":["home","home","home","home","home","home","home","home","home","home","home","home","home","home","home"]}
        y = ["black", [5, 5, 5, 5], [[8, 3], [3, "home"], [1, "home"]]]
        board = Proxy_Backgammon_Board(x, y)
        board = board.getSolution()
        board2 = {"black":["home","home","home","home","home","home","home","home","home","home","home","home","home","home","home"],"white":["home","home","home","home","home","home","home","home","home","home","home","home","home","home","home"]}
        self.assertEqual(board, board2)

    def test16(self):
        x = {"black":[1,8,"home","home","home","home","home","home","home","home","home","home","home","home","home"],"white":["bar","bar","home","home","home","home","home","home","home","home","home","home","home","home","home"]}
        y = ["black", [5, 5, 5, 5], [[8, 3], [1, "home"], [3, "home"]]]
        board = Proxy_Backgammon_Board(x, y)
        board = board.getSolution()
        board2 = False
        self.assertEqual(board, board2)

    def test17(self):
        x = { "black": [ 3, 4, "home", "home", "home", "home", "home", "home", "home", "home", "home", "home", "home", "home", "home" ], "white": ["bar", "bar", 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19] }
        y = ["black", [6, 1], [ [3, "home"], [4, 3] ] ]
        board = Proxy_Backgammon_Board(x, y)
        board = board.getSolution()
        board2 = False
        self.assertEqual(board, board2)

    def test18(self):
        x = {"black": [1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4, 5, 5, 5], "white": [20, 20, 20, 21, 21, 21, 22, 22, 22, 23, 23, 23, 24, 24, 24]}
        y = ["black", [6, 3], [[5, "home"],  [3, "home"]] ]
        board = Proxy_Backgammon_Board(x, y)
        board = board.getSolution()
        board2 = {"black":[1,1,1,2,2,2,3,3,4,4,4,5,5,"home","home"],"white":[20,20,20,21,21,21,22,22,22,23,23,23,24,24,24]}
        self.assertEqual(board, board2)

    def test19(self):
        x = {"black":[1,1,1,1,1,2,2,2,3,3,4,4,4,4,4],"white":[17,17,18,18,18,19,19,19,20,20,20,21,21,22,22]}
        y = ["black",[5,3],[[3,"home"],[4,"home"]]]
        board = Proxy_Backgammon_Board(x, y)
        board = board.getSolution()
        board2 = {"black":[1,1,1,1,1,2,2,2,3,4,4,4,4,"home","home"],"white":[17,17,18,18,18,19,19,19,20,20,20,21,21,22,22]}
        self.assertEqual(board, board2)
    """
    """
    ### FINAL PUSH BABY


    def test20(self):
        x = {"black":[1,1,1,2,2,2,3,3,3,3,18,18,19,19,19],"white":[6,21,21,22,22,22,23,23,23,23,23,23,23,23,23]}
        y = ["white",[4,4,4,4],[[6,10],[10,14]]]
        board = Proxy_Backgammon_Board(x, y)
        board = board.getSolution()
        board2 = {"black":[1,1,1,2,2,2,3,3,3,3,18,18,19,19,19],"white":[14,21,21,22,22,22,23,23,23,23,23,23,23,23,23]}
        self.assertEqual(board, board2)

    def test21(self):
        x = {"black":[11,"home","home","home","home","home","home","home","home","home","home","home","home","home","home"],"white":[22,"home","home","home","home","home","home","home","home","home","home","home","home","home","home"]}
        y = ["white",[1,4],[[22,"home"]]]
        board = Proxy_Backgammon_Board(x, y)
        board = board.getSolution()
        board2 = False
        self.assertEqual(board, board2)
    

    def test22(self):
        x = {"black": [12, 20, "home", "home", "home", "home", "home", "home", "home", "home", "home", "home", "home",
                       "home", "home"],
             "white": [6, 6, 8, 8, 16, 16, "home", "home", "home", "home", "home", "home", "home", "home", "home"]}
        y = ["black", [2, 4], [[12, 10]]]
        board = Proxy_Backgammon_Board(x, y)
        board = board.getSolution()
        board2 = False
        self.assertEqual(board, board2)
    """
if __name__== "__main__":
    unittest.main()