from Backgammon_Class import Proxy_Backgammon_Board, Real_Backgammon_Board
from random import randint
from copy import deepcopy

# Game Object which takes in two strings and creates players from them. The game is played by calling turn() with
# preexisting dice, or with random dice. It runs until the game ends, when it calls end_game() for both players.
# There are also functions to set the board as well.

class Game:

    def __init__(self, player1Name):
        assert isinstance(player1Name, str)
        self.playerName = player1Name
        self.turnNum = 0
        self.board = {"black": [6, 6, 6, 6, 6, 8, 8, 8, 13, 13, 13, 13, 13, 24, 24],
                 "white": [1, 1, 12, 12, 12, 12, 12, 17, 17, 17, 19, 19, 19, 19, 19]}

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

    def turn(self, dice = False):
        if dice is False:
            dice = self.roll_dice()
        if self.turnNum == 0:
            move = self.p1.turn(self.board, dice, random=True)
            if move is False:
                return []
            self.board = Proxy_Backgammon_Board(self.board, [self.p1.color, dice, move]).getSolution()
        else:
            move = self.p2.turn(self.board, dice, random=True)
            if move is False:
                return []
            self.board = Proxy_Backgammon_Board(self.board, [self.p2.color, dice, move]).getSolution()
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
            Proxy_Backgammon_Board(board, ["white", [1,2], [[1,3],[1,2]]]).getSolution()
        except AssertionError:
            print(False)
        self.board = board

    def game_end_check(self):
        if self.board.get("white").count(25) == 15:
            self.p1.end_game(self.board, True)
            self.p2.end_game(self.board, False)
        elif self.board.get("black").count(0) == 15:
            self.p1.end_game(self.board, False)
            self.p2.end_game(self.board, True)

# The player class implements the interface of name(), start_game(), end_game(), and turn(). I also supplied it
# with a random move function so it can play (very badly).

class Player:

    def __init__(self, name, color):
        self.name = name
        self.color = color
        self.colors = ["white", "black"]
        self.gameInProgress = True
        self.exampleTurn = ["white", [1,2], [[1,3],[1,2]]]
        self.moveCache = []

    def get_name(self):
        assert isinstance(self.name, str)
        return self.name

    def start_game(self, color, opponentName):
        assert isinstance(opponentName, str)
        assert color in self.colors
        # print(f"You are playing as {color}. Your opponent is {opponentName}")
        # Informs the player a game has started, its color, and what its opponent’s name is
        return None

    def possible_moves(self, dice):
        pass

    def random_move(self, board, dice):
        board = deepcopy(board)
        board = self.sort_board(board)
        moves = []
        for die in dice:
            notInHome = 15 - board.get(self.color).count("home")
            if board.get(self.color)[0] == "bar":
                checkerToMove = "bar"
            else:
                checkerToMove = board.get(self.color)[randint(0, notInHome-1)]
            if self.color == "black":
                if checkerToMove == "bar":
                    checkerToMove = 25
                movement = checkerToMove - die
                if checkerToMove == 25:
                    checkerToMove = "bar"
                if movement <= 0:
                    movement = "home"
                    moves.append([checkerToMove, "home"])
                else:
                    moves.append([checkerToMove, movement])
                board.get(self.color).remove(checkerToMove)
                board.get(self.color).append(movement)

            elif self.color == "white":
                if checkerToMove == "bar":
                    checkerToMove = 0
                movement = die + checkerToMove
                if checkerToMove == 0:
                    checkerToMove = "bar"
                if movement >= 25:
                    movement = "home"
                    moves.append([checkerToMove, "home"])
                else:
                    moves.append([checkerToMove, movement])
                board.get(self.color).remove(checkerToMove)
                board.get(self.color).append(movement)
            board = self.sort_board(board)
        return moves



    def turn(self, board, dice, random):
        movesValid = False
        movesCache = 0
        if random:
            while movesValid is False:
                try:
                    moves = self.random_move(board, dice)
                    movesValid = Proxy_Backgammon_Board(board, [self.color, dice, moves]).getSolution()
                    movesCache += 1
                    if movesCache > 100:
                        return False
                except AssertionError:
                    pass
            return moves
        return

    def end_game(self, board, didYouWin):

        assert self.gameInProgress is True
        self.gameInProgress = False
        # Check if board is valid
        Proxy_Backgammon_Board(board, self.exampleTurn)

        if didYouWin:
            pass
            # print("Game Over.\nYou Won!")
        else:
            pass
        #     print("Game Over.\nYou Lost.")
        # print("The final board was:\n")
        # print(board)

        return

    def sort_board(self, board):
        whitepieces = board.get("white")
        blackpieces = board.get("black")
        whitepieces = [25 if item == "home" else item for item in whitepieces]
        whitepieces = [0 if item == "bar" else item for item in whitepieces]
        blackpieces = [0 if item == "bar" else item for item in blackpieces]
        blackpieces = [25 if item == "home" else item for item in blackpieces]
        blackpieces.sort()
        whitepieces.sort()
        whitepieces = ["home" if item == 25 else item for item in whitepieces]
        whitepieces = ["bar" if item == 0 else item for item in whitepieces]
        blackpieces = ["bar" if item == 0 else item for item in blackpieces]
        blackpieces = ["home" if item == 25 else item for item in blackpieces]
        board["white"] = whitepieces
        board["black"] = blackpieces
        return board
