from Backgammon_Class import Proxy_Backgammon_Board, turnTree
from random import randint
from copy import deepcopy
import time

# Game Object which takes in two strings and creates players from them. The game is played by calling turn() with
# preexisting dice, or with random dice. It runs until the game ends, when it calls end_game() for both players.
# There are also functions to set the board as well.

class Game:

    def __init__(self, player1Name, strategy=None):
        assert isinstance(player1Name, str)
        self.playerName = player1Name
        self.strategy = strategy
        self.turnNum = 0
        self.gameInProgress = True
        self.p1 = None
        self.p2 = None
        self.StartingBoard = {"black": [6, 6, 6, 6, 6, 8, 8, 8, 13, 13, 13, 13, 13, 24, 24],
                 "white": [1, 1, 12, 12, 12, 12, 12, 17, 17, 17, 19, 19, 19, 19, 19]}
        self.board = Proxy_Backgammon_Board(self.StartingBoard)

    def set_player_fields(self, color, otherPlayerName):
        assert isinstance(color, str)
        assert isinstance(otherPlayerName, str)
        if color == "black":
            player1Name = otherPlayerName
            player2Name = self.playerName
            self.turnNum += 1
        elif color == "white":
            player1Name = self.playerName
            player2Name = otherPlayerName
        self.p1 = Player(player1Name, "white")
        self.p2 = Player(player2Name, "black")
        self.p1.start_game("white", player2Name)
        self.p2.start_game("black", player1Name)
        self.p1.set_strategy(self.strategy)
        self.p2.set_strategy(self.strategy)

    def turn(self, dice = False, turn = False):
        oldBoard = deepcopy(self.board)
        if dice is False:
            dice = self.roll_dice()
            self.debuggingDice = deepcopy(dice)
        # originalBoard = deepcopy(oldBoard.getSolution())
        # print(originalBoard)
        # print(self.StartingBoard)
        # if originalBoard == self.StartingBoard and len(dice) == 4:
        #     while len(dice) == 4:
        #         dice = self.roll_dice()
        if turn is False:
            ### Conditionals for strategies will be added here
            if self.turnNum % 2 == 0:
                move = self.p1.turn(self.board, dice, random=True)
                if move is False:
                    return []
                self.board.moving(self.p1.color, deepcopy(dice), deepcopy(move))
            else:
                move = self.p2.turn(self.board, dice, random=True)
                if move is False:
                    return []
                self.board.moving(self.p2.color, deepcopy(dice), deepcopy(move))
        else:
            move = turn
            if self.turnNum % 2 == 0:
                self.board.moving(self.p1.color, deepcopy(dice), deepcopy(turn))
            else:
                self.board.moving(self.p2.color, deepcopy(dice), deepcopy(turn))
        self.turnNum += 1
        if self.board.getSolution() == False:
            # print("this errored and the oldBoard is: ", oldBoard.getSolution())
            self.board = oldBoard
            return False
        self.game_end_check()
        return move

    def roll_dice(self):
        dice = [randint(1,6), randint(1,6)]
        # If both rolls are equal, generate 2 more dice with the same value.
        if dice[0] == dice[1]:
            dice.extend(dice)
        return dice

    def set_board(self, board):
        try:
            self.board = Proxy_Backgammon_Board(board)
        except AssertionError:
            print(False)

    def game_end_check(self):
        endBoard = self.board.getSolution()
        if endBoard is False:
            pass
        elif endBoard.get("white").count("home") == 15:
            self.p1.end_game(endBoard, True)
            self.p2.end_game(endBoard, False)
            self.gameInProgress = False
            self.winnerNameOfGame = [self.p1.get_name(), "p1"]
        elif endBoard.get("black").count("home") == 15:
            self.p1.end_game(endBoard, False)
            self.p2.end_game(endBoard, True)
            self.gameInProgress = False
            self.winnerNameOfGame = [self.p2.get_name(), "p2"]


    def get_board(self):
        realBoard = self.board.getSolution()
        if realBoard is False:
            raise("Something went terribly wrong and we should cry. Specifically, with get_board in GameTools.")
        else:
            return(realBoard)

# The player class implements the interface of name(), start_game(), end_game(), and turn(). I also supplied it
# with a random move function so it can play (very badly).

class Player:

    def __init__(self, name, color):
        self.name = name
        self.color = color
        self.strategy = None
        self.colors = ["white", "black"]
        if self.color == self.colors[0]:
            self.otherColor = self.colors[1]
        elif self.color == self.colors[1]:
            self.otherColor = self.colors[0]
        self.gameInProgress = True
        self.exampleTurn = ["white", [1,2], [[1,3],[1,2]]]
        self.moveCache = []
        self.StartingBoard = {"black": [6, 6, 6, 6, 6, 8, 8, 8, 13, 13, 13, 13, 13, 24, 24],
                              "white": [1, 1, 12, 12, 12, 12, 12, 17, 17, 17, 19, 19, 19, 19, 19]}

    def get_name(self):
        assert isinstance(self.name, str)
        return self.name

    def set_strategy(self, strategy):
        self.strategy = strategy

    def start_game(self, color, opponentName):
        assert isinstance(opponentName, str)
        assert color in self.colors
        # print(f"You are playing as {color}. Your opponent is {opponentName}")
        # Informs the player a game has started, its color, and what its opponent???s name is
        return None

    def generate_moves(self, board, die):
        JSONBoard = deepcopy(board.getSolution())
        ourTurnTree = turnTree(JSONBoard, self.color, deepcopy(sorted(die)))
        moveSet = ourTurnTree.get_all_turns()
        return moveSet

    def random_move(self, moveSet):
        randIndex = randint(0, len(moveSet) - 1)
        randomMove = moveSet[randIndex]
        return randomMove

    def smart_move(self, board, moveSet, dice):
        answer = []
        ### Opening Moves Condition
        if board.getSolution() == self.StartingBoard:
            if len(dice) == 2:
                bestMove = self.starting_move(dice)
            elif len(dice) == 4:
                bestMove = self.random_move(moveSet)
        ### Else, we're in normal game
        else:

            for turn in moveSet:
                newScore = self.score(deepcopy(turn), deepcopy(board), deepcopy(dice))
                answer.append([turn, newScore])

            answer.sort(key=lambda pair: pair[1], reverse=True)
            # print(answer)
            bestMove = answer[0][0]
        return bestMove

    def starting_move(self, dice):
        ourDice = deepcopy(dice)
        ourDice.sort(reverse=True)
        ### Black's Opening Moves Occur Here
        if self.color == "black":
            if ourDice == [2, 1]:
                return [[13, 11], [6, 5]]
            elif ourDice == [3, 1]:
                return [[8, 5], [6, 5]]
            elif ourDice == [4, 1]:
                return [[24, 23], [13, 9]]
            elif ourDice == [5, 1]:
                return [[24, 23], [13, 8]]
            elif ourDice == [6, 1]:
                return [[13, 7], [8, 7]]
            elif ourDice == [3, 2]:
                return [[24, 21], [13, 11]]
            elif ourDice == [4, 2]:
                return [[8, 4], [6, 4]]
            elif ourDice == [5, 2]:
                return [[24, 22], [13, 8]]
            elif ourDice == [6, 2]:
                return [[24, 18], [13, 11]]
            elif ourDice == [4, 3]:
                return [[13, 10], [13, 9]]
            elif ourDice == [5, 3]:
                return [[8, 3], [6, 3]]
            elif ourDice == [6, 3]:
                return [[24, 18], [13, 10]]
            elif ourDice == [5, 4]:
                return [[24, 20], [13, 8]]
            elif ourDice == [6, 4]:
                return [[24, 18], [13, 9]]
            elif ourDice == [6, 5]:
                return [[24, 18], [18, 13]]

        ### White's Opening Moves Occur Here
        elif self.color == "white":
            if ourDice == [2, 1]:
                return [[12, 14], [19, 20]]
            elif ourDice == [3, 1]:
                return [[17, 20], [19, 20]]
            elif ourDice == [4, 1]:
                return [[1, 2], [12, 16]]
            elif ourDice == [5, 1]:
                return [[1, 2], [12, 17]]
            elif ourDice == [6, 1]:
                return [[12, 18], [17, 18]]
            elif ourDice == [3, 2]:
                return [[1, 4], [12, 14]]
            elif ourDice == [4, 2]:
                return [[17, 21], [19, 21]]
            elif ourDice == [5, 2]:
                return [[1, 3], [12, 17]]
            elif ourDice == [6, 2]:
                return [[1, 7], [12, 14]]
            elif ourDice == [4, 3]:
                return [[12, 15], [12, 16]]
            elif ourDice == [5, 3]:
                return [[17, 22], [19, 22]]
            elif ourDice == [6, 3]:
                return [[1, 7], [12, 15]]
            elif ourDice == [5, 4]:
                return [[1, 5], [12, 17]]
            elif ourDice == [6, 4]:
                return [[1, 7], [12, 16]]
            elif ourDice == [6, 5]:
                return [[1, 7], [7, 12]]


    # Bopping = 1/each piece
    # Can be bopped = -0.5/each piece
    # Candlestick = -0.3/each piece if >= 5 on a space.
    # if point = .5/each point
    # if point in our homeboard, add weight moreso than a normal point, so total = .75/each point

    def score(self, turn, board, dice):
        BoppingWeight = 1
        canBeBoppedWeight = -0.5
        candlestickWeight = -0.3
        pointWeight = 0.5
        pointHomeWeight = 0.75

        homeBoard = self.generateHomeBoard(self.color)

        score = 0.0
        oldBoard = board
        newBoard = deepcopy(board)
        newBoard.moving(self.color, dice, turn)
        oldJSONBoard = oldBoard.getSolution()
        newJSONBoard = newBoard.getSolution()

        # Bopping Condition
        numBopped = newJSONBoard[self.otherColor].count("bar") - oldJSONBoard[self.otherColor].count("bar")
        score += BoppingWeight * numBopped

        # Can be Bopped Condition
        oldpieces = set(oldJSONBoard[self.color])
        oldBlottables = 0
        for piece in oldpieces:
            if oldJSONBoard[self.color].count(piece) == 1:
                oldBlottables += 1

        newpieces = set(newJSONBoard[self.color])
        newBlottables = 0
        for piece in newpieces:
            if newJSONBoard[self.color].count(piece) == 1:
                newBlottables += 1

        blottableDiff = newBlottables - oldBlottables - numBopped
        score += blottableDiff * canBeBoppedWeight

        # Candlestick Condition
        for pieces in newJSONBoard[self.color]:
            if newJSONBoard[self.color].count(pieces) >= 5:
                score += candlestickWeight

        # Points Condition - (oldpieces is list of spaces we have checkers on in the old board,
        # and new pieces is list of spaces we have checkers on in the new board)
        oldhomePoint = 0
        newhomePoint = 0
        oldotherPoint = 0
        newotherPoint = 0
        for piece in oldpieces:
            if oldJSONBoard[self.color].count(piece) == 2:
                if piece in homeBoard:
                    oldhomePoint += 1
                else:
                    oldotherPoint += 1

        for piece in newpieces:
            if newJSONBoard[self.color].count(piece) == 2:
                if piece in homeBoard:
                    newhomePoint += 1
                else:
                    newotherPoint += 1

        oldPointScore = pointWeight * oldotherPoint + pointHomeWeight * oldhomePoint
        newPointScore = pointWeight * newotherPoint + pointHomeWeight * newhomePoint
        weightedPointChange = newPointScore - oldPointScore
        score += weightedPointChange
        return score

    def generateHomeBoard(self, color):
        boardSpaces = [i for i in range(26)]
        if color == "black":
            return boardSpaces[1:7]
        elif color == "white":
            return boardSpaces[19:25]

    def turn(self, board, dice, random):
        newboard = deepcopy(board)
        # start_time = time.time()
        moveSet = self.generate_moves(newboard, deepcopy(dice))
        # print("--- generate_moves: %s seconds ---" % (time.time() - start_time))
        if random:
            if self.strategy == "good":
                # start_time = time.time()
                moves = self.smart_move(newboard, moveSet, deepcopy(dice))
                # print("--- smart_move: %s seconds ---" % (time.time() - start_time))
            else:
                moves = self.random_move(moveSet)
            eatMove = deepcopy(moves)
            newboard.moving(self.color, deepcopy(dice), eatMove)
        return moves

    def end_game(self, board, didYouWin):
        assert self.gameInProgress is True
        self.gameInProgress = False
        boardToCheck = Proxy_Backgammon_Board(board)
        # Check if board is valid
        if boardToCheck.Board_Check(board):
            pass
        else:
            raise("end game is not passing in a board")

        if didYouWin:
            pass
            # print("Game Over.\nYou Won!")
        else:
            pass
        #     print("Game Over.\nYou Lost.")
        # print("The final board was:\n")

        return

    def sort_board(self, board):
        whitepieces = board.get("white")
        blackpieces = board.get("black")
        whitepieces = [25 if item == "home" else item for item in whitepieces]
        whitepieces = [0 if item == "bar" else item for item in whitepieces]
        blackpieces = [0 if item == "home" else item for item in blackpieces]
        blackpieces = [25 if item == "bar" else item for item in blackpieces]
        blackpieces.sort()
        whitepieces.sort()
        whitepieces = ["home" if item == 25 else item for item in whitepieces]
        whitepieces = ["bar" if item == 0 else item for item in whitepieces]
        blackpieces = ["home" if item == 0 else item for item in blackpieces]
        blackpieces = ["bar" if item == 25 else item for item in blackpieces]
        board["white"] = whitepieces
        board["black"] = blackpieces
        return board

### Case 1 that errored

# newGame = Game("playerInputted")
# newGame.set_player_fields("white", "p2")
# newGame.set_board({"black":[1,1,1,1,1,1,1,1,2,2,2,2,2,4,5],"white":[3,3,12,12,12,12,12,17,17,17,19,19,19,21,21]})
# key = newGame.turn([5,4])
# print(key)
# newKey = newGame.turn([5,4])
# print(newKey)

### Case 2 that errored

# newGame = Game("playerInputted")
# newGame.set_player_fields("white", "p2")
# newGame.set_board({"black":[5,4,"home","home","home","home","home","home","home","home","home","home","home","home","home"],"white":[3,3,12,12,12,12,12,17,17,17,19,19,19,21,21]})
# key = newGame.turn([5,4])
# print(key)
# newKey = newGame.turn([5,4], [[5,'home'], [4,'home']])
# print(newKey)
# gameInProgress = newGame.gameInProgress
# print(gameInProgress)