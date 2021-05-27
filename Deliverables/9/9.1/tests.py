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

    ### Opening Moves Cases
    def test_opening25b(self):
        goodGame = Game("player1", strategy="good")
        goodGame.set_player_fields("black", "player2")
        retVal = goodGame.turn([2, 5])
        self.assertEqual(retVal, [[24, 22], [13, 8]])

    def test_opening25w(self):
        goodGame = Game("player1", strategy="good")
        goodGame.set_player_fields("white", "player2")
        retVal = goodGame.turn([5, 2])
        self.assertEqual(retVal, [[1, 3], [12, 17]])

    def test_opening13b(self):
        goodGame = Game("player1", strategy="good")
        goodGame.set_player_fields("black", "player2")
        retVal = goodGame.turn([1, 3])
        self.assertEqual(retVal, [[8, 5], [6, 5]])

    def test_opening56b(self):
        goodGame = Game("player1", strategy="good")
        goodGame.set_player_fields("black", "player2")
        retVal = goodGame.turn([5, 6])
        self.assertEqual(retVal, [[24, 18], [18, 13]])

    def test_opening34w(self):
        goodGame = Game("player1", strategy="good")
        goodGame.set_player_fields("white", "player2")
        retVal = goodGame.turn([3, 4])
        self.assertEqual(retVal, [[12, 15], [12, 16]])

    ### Points Test Case

    def test_homepoints(self):
        testBoard = {"black": [2, 2, 3, 3, 4, 5, 7, 10, 16, 16, 16, 18, 18, 18, 20],
                     "white": [1, 1, 12, 12, 12, 12, 12, 17, 17, 17, 17, 19, 19, 19, 19]}
        goodGame = Game("player1", strategy="good")
        goodGame.set_player_fields("black", "player2")
        goodGame.set_board(testBoard)
        retVal = goodGame.turn([5, 3])
        self.assertEqual(retVal, [[10, 5], [7, 4]])

    ### Game simulation, good vs rando
    def test_game_simulation(self):
        try:
            goodGame = Game("player1", strategy="good")
            goodGame.set_player_fields("black", "player2")
            goodGame.p2.set_strategy("rando")
            while goodGame.gameInProgress:
                goodGame.turn(dice = False, turn = False)
        except:
            print(goodGame.turnNum)
            print(goodGame.get_board())
            print("dice, ", goodGame.debuggingDice)

        self.assertEqual(goodGame.winnerNameOfGame[1], "p1")


if __name__== "__main__":
    unittest.main()

