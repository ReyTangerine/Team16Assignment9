import unittest
from GameTools import Game
import time

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
        self.assertEqual(retVal, [[7, 4], [10, 5]])


    ### Debugging Games

    ###### Originally was creating a ["home", "home"] move s.t. the turn would be:
    ###### [[5, "home"], [5, "home"], [5, "home"], ["home", "home"]]
    ###### FIX: We removed the ["home","home"] from turn directly

    def test_input1_team20(self):
        testBoard = {"black" : [5, 5, 5, "home", "home", "home", "home", "home", "home", "home", "home", "home", "home", "home", "home"],
                     "white" : [20, "home", "home", "home", "home", "home", "home", "home", "home", "home", "home", "home", "home", "home", "home"]}
        goodGame = Game("player1", strategy="good")
        goodGame.set_player_fields("black", "player2")
        goodGame.set_board(testBoard)
        retVal = goodGame.turn([5, 5, 5, 5])
        self.assertEqual(retVal, [[5, "home"], [5, "home"], [5, "home"]])

    ###### Originally was creating a "[]" turn
    ###### FIX: We hardcoded one of the opening moves wrong. We went back in and fixed it (while checking the others AGAIN)
    def test_input4_team27(self):
        testBoard = {"black": [6, 6, 6, 6, 6, 8, 8, 8, 13, 13, 13, 13, 13, 24, 24],
                     "white": [1, 1, 12, 12, 12, 12, 12, 17, 17, 17, 19, 19 ,19 ,19 ,19]}
        goodGame = Game("player1", strategy="good")
        goodGame.set_player_fields("white", "player2")
        goodGame.set_board(testBoard)
        retVal = goodGame.turn([4,5])
        self.assertEqual(retVal, [[1, 5], [12, 17]])

    def test_input7_team5(self):
        # start_time = time.time()
        testBoard = {"black":[5,6,7,8,9,10,10,11,12,13,14,15,16,17,18],
                      "white":[22,"home","home","home","home","home","home","home","home","home","home","home","home","home","home"]}
        goodGame = Game("player1", strategy="good")
        goodGame.set_player_fields("white", "player2")
        goodGame.set_board(testBoard)
        retVal = goodGame.turn([5,2])
        # print("--- test_input7_team5: %s seconds ---" % (time.time() - start_time))
        self.assertEqual(retVal, [[22,24],[24,"home"]])

    def test_input4_team37(self):
        # start_time = time.time()
        testBoard = {
            "black": [2, 4, 6, 8, 10, 10, 12, 14, 14, 16, 18, 20, 22, 24, "home"],
            "white": [1, 3, 5, 7, 9, 9, 11, 13, 13, 15, 17, 19, 21, 23, "home"]
        }
        goodGame = Game("player1", strategy="good")
        goodGame.set_player_fields("black", "player2")
        goodGame.set_board(testBoard)
        retVal = goodGame.turn([1,1,1,1])
        # print("--- test_input4_team37: %s seconds ---" % (time.time() - start_time))
        self.assertEqual(retVal, [[4, 3], [3, 2], [8, 7], [7, 6]])



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

