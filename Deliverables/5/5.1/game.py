class Game:

    def __init__(self):
        self.colors = ["white", "black"]
        self.gameInProgress = True

    def name(self):
        assert isinstance(self.name, str)
        return self.name

    def start_game(self, color, opponentName):
        assert isinstance(self.name, str)
        assert color in self.colors
        print(f"You are playing as {color}. Your opponent is {opponentName}")
        # Informs the player a game has started, its color, and what its opponent’s name is
        return None

    def turn(self, board, dice):
        # turn = playerMoves
        # Player makes turn
        # assert isinstance(playerMoves, list)
        # return playerMoves
        pass

    def end_game(self, board, didYouWin):
        assert self.gameInProgress is True
        self.gameInProgress = False
        # informs the player that the game is over, what the final board was, and if it won
        return None