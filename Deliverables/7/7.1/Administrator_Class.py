from GameTools import Game
from copy import deepcopy

class Admin:
    def __init__(self, localPlayerName, strategy):
        self.game_instance = Game(localPlayerName, strategy)
        self.cheatersNeverProsper = False

    def start_game(self, color, otherPlayerName):
        self.game_instance.set_player_fields(color, otherPlayerName)

    def roll_dice(self):
        return (self.game_instance.roll_dice())

    def turn(self, dice=False, turn=False):
        dicecopy = deepcopy(dice)
        if self.cheatersNeverProsper is False:
            move = self.game_instance.turn(dice, turn)
            if move is False:
                move = self.game_instance.turn(dicecopy)
                self.cheatersNeverProsper = True
        else:
            move = self.game_instance.turn(dice)
        return move

    def get_board(self):
        ourBoard = self.game_instance.get_board()
        return ourBoard

    def is_game_over(self):
        gameInProgress = self.game_instance.gameInProgress
        return not gameInProgress

    ### Please note, this will always return the names so that, in string form
    ### [localPlayer::string, remotePlayer::string]
    def get_names(self):
        p1Name = self.game_instance.p1.get_name()
        p2Name = self.game_instance.p2.get_name()
        return [p1Name,p2Name]

    def set_remote_name(self, name):
        self.game_instance.p2.name = name


