from Backgammon_Class import Proxy_Backgammon_Board, turnTree
from random import randint
from copy import deepcopy

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
        board = {"black": [6, 6, 6, 6, 6, 8, 8, 8, 13, 13, 13, 13, 13, 24, 24],
                 "white": [1, 1, 12, 12, 12, 12, 12, 17, 17, 17, 19, 19, 19, 19, 19]}
        self.board = Proxy_Backgammon_Board(board)

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
        elif endBoard.get("black").count("home") == 15:
            self.p1.end_game(endBoard, False)
            self.p2.end_game(endBoard, True)
            self.gameInProgress = False


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

    def get_name(self):
        assert isinstance(self.name, str)
        return self.name

    def set_strategy(self, strategy):
        self.strategy = strategy

    def start_game(self, color, opponentName):
        assert isinstance(opponentName, str)
        assert color in self.colors
        # print(f"You are playing as {color}. Your opponent is {opponentName}")
        # Informs the player a game has started, its color, and what its opponent’s name is
        return None

    def generate_moves(self, board, die):
        JSONBoard = deepcopy(board.getSolution())
        ourTurnTree = turnTree(JSONBoard, self.color, deepcopy(die))
        moveSet = ourTurnTree.get_all_turns()
        return moveSet

    def random_move(self, moveSet):
        randIndex = randint(0, len(moveSet) - 1)
        randomMove = moveSet[randIndex]
        return randomMove

    def smart_move(self, board, moveSet):
        answer = []
        for turn in moveSet:
            newScore = self.score(deepcopy(turn), deepcopy(board))
            answer.append([turn, newScore])

        answer.sort(key=lambda pair: pair[1])
        bestMove = answer[0]
        return bestMove

    def score(self, turn, board):
        score = 0
        oldBoard = board
        newBoard = deepcopy(board)
        newBoard.moving(turn)
        oldJSONBoard = oldBoard.getSolution()
        newJSONBoard = newBoard.getSolution()
        if oldJSONBoard[self.otherColor] == newJSONBoard[self.otherColor]:
            score += 1
        return score


    def turn(self, board, dice, random):
        newboard = deepcopy(board)
        moveSet = self.generate_moves(newboard, deepcopy(dice))
        if random:
            if self.strategy == "good":
                moves = self.smart_move(moveSet)
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