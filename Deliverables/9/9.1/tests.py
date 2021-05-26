import unittest
from GameTools import Game

class GameTest(unittest.TestCase):
    def test_bop1(self):
        testBoard = {
            "black": [7, 20, 22, "home", "home", "home", "home", "home", "home", "home", "home", "home", "home",
                      "home",
                      "home"], "white": ["bar", 1, 3, 5, 12, 12, 12, 17, 17, 18, 19, 19, 19, 19, 19]}
        goodGame = Game("player1", strategy="good")
        goodGame.set_player_fields("black", "player2")
        goodGame.set_board(testBoard)
        retVal = goodGame.turn([2, 2, 2, 2])
        self.assertEqual(retVal, [[7,5],[5,3],[3,1],[20,18]])

    def test_bop2(self):
        testBoard = {"black": [6, 6, 6, 6, 6, 8, 8, 8, 13, 13, 13, 15, 18, 24, 24],
                 "white": [1, 1, 12, 12, 12, 12, 12, 17, 17, 17, 17, 19, 19, 19, 19]}
        goodGame = Game("player1", strategy="good")
        goodGame.set_player_fields("white", "player2")
        goodGame.set_board(testBoard)
        retVal = goodGame.turn([3, 6])
        self.assertEqual(retVal, [[12, 15], [12, 18]])

    def test_start(self):
        testBoard = {"black": [6, 6, 6, 6, 6, 8, 8, 8, 13, 13, 13, 13, 13, 24, 24],
                 "white": [1, 1, 12, 12, 12, 12, 12, 17, 17, 17, 19, 19, 19, 19, 19]}
        goodGame = Game("player1", strategy="good")
        goodGame.set_player_fields("black", "player2")
        goodGame.set_board(testBoard)
        retVal = goodGame.turn([2, 2, 2, 2])
        self.assertEqual(len(retVal), 2)


if __name__== "__main__":
    unittest.main()