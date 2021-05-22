from math import log2, ceil, modf
from random import random
from copy import deepcopy
import json
import sys
import socket
from Administrator_Class import Admin, CheatingError


class Tournament():

    # TODO --
    #       4*. Dummy var in randominfodict could need modification

    ### self.randomInfo is a dictionary filled with trash information
    ### {player1:randomInfo, player2:randomInfo, player3:randomInfo... playerN:randomInfo}
    ### randomInfo ::= {"name":str, "cheating" == bool, "filler player" == bool, "connection" == c}
    def __init__(self, tournament_type, num_players, socket):
        self.d = json.JSONDecoder()
        self.e = json.JSONEncoder()
        self.socket = socket

        # admin-networking-started::="started"
        admin_networking_started = self.e.encode("started")
        print(admin_networking_started)
        sys.stdout.flush()

        self.tournament_type = tournament_type
        self.num_players = num_players

        if tournament_type == "single elimination":
            if not self.isPowerofTwo(num_players):
                self.total_num_players = 2 ** ceil(log2(num_players))
        else:
            self.total_num_players = num_players

        # {Score: [number of wins, number of loses]}
        self.player_score = {score: [0, 0] for score in range(self.total_num_players)}
        ### RandomInfoDict is a class var since we reference it multiple times
        self.randomInfoDict = {"name": "nothin for now", "cheating": False, "filler player": True, "connection": None}
        self.randomInfo = {player: deepcopy(self.randomInfoDict) for player in range(self.total_num_players)}
        self.remove_dummy_bool = False
        self.socket.listen(self.num_players)
        # alphabetInt = 97
        for remotePlayer in range(self.num_players):
            c, addr = self.socket.accept()  # Establish connection with client.
            self.randomInfo[remotePlayer]["connection"] = c
            self.randomInfo[remotePlayer]["filler player"] = False
            # self.randomInfo[remotePlayer]["name"] = chr(alphabetInt)
            # alphabetInt += 1
        for player in range(self.total_num_players):
            if self.randomInfo[player]["filler player"] == True:
                self.randomInfo[player]["name"] = f"Filler_{player}"

    def isPowerofTwo(self, num):
        powerofTwo = log2(num)
        if modf(powerofTwo) == 0:
            return True
        else:
            return False

    def matching(self):
        players = [player for player in range(self.total_num_players)]
        if self.tournament_type == "round robin":
            ### Start a tournament bracket history list
            ### ideally should be a list of rounds: [round1, round2, round3... round_n]
            ### each round: [match1, match2, match3... match_n]
            ### each match: [playerA, playerB, winner]
            self.round_robin_history = []
            ### Insert dummy player here if there is an odd number of players
            if self.total_num_players % 2 == 1:
                self.buildDummyPlayer()
                players = [player for player in range(self.total_num_players)]
            ### Start the matching
            for round in range(self.total_num_players - 1):
                firstpair = players[0:int(self.total_num_players / 2)]
                secondpair = players[int(self.total_num_players / 2): self.total_num_players]
                secondpair.reverse()
                ### We append the current round to our round_robin_history list
                self.round_robin_history.append(list(map(list, zip(firstpair, secondpair))))
                currentRound = len(self.round_robin_history) - 1
                ### We faceoff the players
                for match in range(int(self.total_num_players / 2)):
                    ### If it's a dummy player, just skip through
                    if self.randomInfo[firstpair[match]]["name"] == "Dummy" or self.randomInfo[secondpair[match]]["name"] == "Dummy":
                        pass
                    else:
                        winner, _ = self.playGame(firstpair[match], secondpair[match])
                        self.round_robin_history[currentRound][match].append(winner)

                # Rotation occurs here
                lastPlayer = players.pop()
                players.insert(0, lastPlayer)
                players[0], players[1] = players[1], players[0]

            ### Remove dummy player here
            if self.remove_dummy_bool:
                self.removeDummyPlayer()


        elif self.tournament_type == "single elimination":
            remainingPlayers = deepcopy(players)

            # Play games until one victor emerges
            while len(remainingPlayers) > 1:
                numOfRemainingPlayers = len(remainingPlayers)
                firstpair = remainingPlayers[0:int(numOfRemainingPlayers / 2)]
                secondpair = remainingPlayers[int(numOfRemainingPlayers / 2): numOfRemainingPlayers]

                # Plays out each game
                for match in range(int(numOfRemainingPlayers / 2)):
                    winner, loser = self.playGame(firstpair[match], secondpair[match])
                    remainingPlayers.remove(loser)

    ### Here, for the odd number of players case with the round robin, we will both build a dummy player at the start
    ### Of the rounds, and remove the dummy player for the end

    def buildDummyPlayer(self):
        self.player_score[self.total_num_players] = "Dummy"
        self.randomInfo[self.total_num_players] = deepcopy(self.randomInfoDict)
        self.randomInfo[self.total_num_players]["name"] = "Dummy"
        self.total_num_players += 1
        self.remove_dummy_bool = True

    def removeDummyPlayer(self):
        self.total_num_players -= 1
        del self.player_score[self.total_num_players]
        self.remove_dummy_bool = False

    def playGame(self, PlayerA, PlayerB):
        # if isinstance(self.player_score[PlayerA], str) or isinstance(self.player_score[PlayerB], str):
        #     return None, None
        if self.randomInfo[PlayerA]["cheating"] == True:
            winner = PlayerB
            loser = PlayerA
            self.player_score[winner][0] += 1
            self.player_score[loser][1] += 1
            return winner, loser
        elif self.randomInfo[PlayerB]["cheating"] == True:
            winner = PlayerA
            loser = PlayerB
            self.player_score[winner][0] += 1
            self.player_score[loser][1] += 1
            return winner, loser
        else:
            newAdmin = Admin()  # This will print the right thing
            try:
                if self.randomInfo[PlayerA]["filler player"] and self.randomInfo[PlayerB]["filler player"]:
                    if random() < .5:
                        winner = PlayerA
                        loser = PlayerB
                        self.player_score[winner][0] += 1
                        self.player_score[loser][1] += 1
                        return winner, loser
                    else:
                        winner = PlayerB
                        loser = PlayerA
                        self.player_score[winner][0] += 1
                        self.player_score[loser][1] += 1
                        return winner, loser

                ### Setting Player A's Name
                if self.randomInfo[PlayerA]["connection"] is None:
                    newAdmin.setPlayerA(self.randomInfo[PlayerA]["name"])
                else:
                    newAdmin.setPlayerA(connection=self.randomInfo[PlayerA]["connection"])
                    if self.randomInfo[PlayerA]["name"] == "nothin for now":
                        self.randomInfo[PlayerA]["name"] = newAdmin.playerAName
                    elif self.randomInfo[PlayerA]["name"] != newAdmin.playerAName:
                        self.playerACheatingBool = True
                        raise CheatingError

                ### Setting Player B's Name
                if self.randomInfo[PlayerB]["connection"] is None:
                    newAdmin.setPlayerB(self.randomInfo[PlayerB]["name"])
                else:
                    newAdmin.setPlayerB(connection=self.randomInfo[PlayerB]["connection"])
                    if self.randomInfo[PlayerB]["name"] == "nothin for now":
                        self.randomInfo[PlayerB]["name"] = newAdmin.playerBName
                    elif self.randomInfo[PlayerB]["name"] != newAdmin.playerBName:
                        self.playerBCheatingBool = True
                        raise CheatingError
                newAdmin.start_game("rando")
                newAdmin.playThrough()
                winnerName = newAdmin.winnerName
                winnerNo = False
                for key in self.randomInfo:
                    if self.randomInfo[key]["name"] == winnerName:
                        winnerNo = key
                if winnerNo is False:
                    raise ("winner of game is not in our records. This is super awkward. I'm upset.")
                if winnerNo is PlayerA:
                    winner = PlayerA
                    loser = PlayerB
                elif winnerNo is PlayerB:
                    winner = PlayerB
                    loser = PlayerA
                # Increment whoever wins and loses
                self.player_score[winner][0] += 1
                self.player_score[loser][1] += 1
                return winner, loser

            except CheatingError:
                if newAdmin.playerACheatingBool is True:
                    winner, loser = self.cheating(PlayerA, PlayerA, PlayerB)
                    newAdmin.playerA.end_game(newAdmin.get_board(), False)
                    newAdmin.playerB.end_game(newAdmin.get_board(), True)
                    return winner, loser
                elif newAdmin.playerBCheatingBool is True:
                    winner, loser = self.cheating(PlayerB, PlayerA, PlayerB)
                    newAdmin.playerA.end_game(newAdmin.get_board(), True)
                    newAdmin.playerB.end_game(newAdmin.get_board(), False)
                    return winner, loser



    ### This should produce the winner/loser pair required of this function
    def cheating(self, cheater, playerA, playerB):
        if self.randomInfo[cheater]["connection"] is not None:
            self.randomInfo[cheater]["connection"].close()
            self.randomInfo[cheater]["connection"] = None
        if cheater == playerA:
            winner = playerB
        else:
            winner = playerA
        # if self.randomInfo[winner]["connection"] is not None:
        #     boolean = True
        #     board = {"black": [6, 6, 6, 6, 6, 8, 8, 8, 13, 13, 13, 13, 13, 24, 24],
        #          "white": [1, 1, 12, 12, 12, 12, 12, 17, 17, 17, 19, 19, 19, 19, 19]}
        #     end_game = {"end-game": [board, boolean]}
        #     JSONThing = self.e.encode(end_game)
        #     byteAnswer = bytes(JSONThing + "\n", 'utf-8')
        #     self.randomInfo[winner]["connection"].sendall(byteAnswer)
        if self.tournament_type == "round robin":
            self.round_robin_cheating(cheater)
            self.player_score[winner][0] += 1
            self.player_score[cheater][1] += 1
            return winner, cheater
        else:
            self.player_score[winner][0] += 1
            self.player_score[cheater][1] += 1
            return winner, cheater

    def round_robin_cheating(self, cheater):
        self.cheating_var_change(cheater)
        for roundNo in range(len(self.round_robin_history)):
            currRound = self.round_robin_history[roundNo]
            for matchNo in range(len(currRound)):
                if len(currRound[matchNo]) == 2:
                    pass
                elif cheater in currRound[matchNo] and currRound[matchNo][2] == cheater:
                    cheaterPosition = currRound[matchNo].index(cheater)
                    victimPosition = (cheaterPosition + 1) % 2
                    victim = currRound[matchNo][victimPosition]
                    if isinstance(self.player_score[cheater], str):
                        pass
                    elif self.randomInfo[victim]["cheating"] is True and self.randomInfo[cheater]["cheating"] is True:
                        self.player_score[cheater][0] -= 1
                        self.player_score[cheater][1] += 1
                    else:
                        self.player_score[victim][0] += 1
                        self.player_score[victim][1] -= 1
                        self.player_score[cheater][0] -= 1
                        self.player_score[cheater][1] += 1

    def cheating_var_change(self, playerNo):
        self.randomInfo[playerNo]["cheating"] = True

    def tournamentResult(self):
        for player in self.randomInfo:
            if self.randomInfo[player]["connection"] is not None:
                self.randomInfo[player]["connection"].close()
        newList = []
        for key in self.player_score:
            newListElement = [key]
            newListElement.extend(self.player_score[key])
            newList.append(newListElement)

        # Sort by winner
        newList.sort(key=lambda results: results[1], reverse=True)
        if self.num_players == 1:
            self.randomInfo[0]["name"] = "a"

        if self.tournament_type == "round robin":
            for result in newList:
                actualName = self.randomInfo[result[0]]["name"]
                player = deepcopy(result[0])
                result[0] = actualName
            print(self.e.encode(newList))
        elif self.tournament_type == "single elimination":
            winner = newList[0][0]
            if self.num_players == 1:
                print(self.e.encode("a"))
            else:
                if self.randomInfo[winner]["filler player"] is True:
                    print(self.e.encode(False))
                else:
                    winnerName = self.randomInfo[winner]["name"]
                    print(self.e.encode(winnerName))