from copy import deepcopy

class Real_Backgammon_Board:

    """
    self.Black_Pos is a list of black positions
    self.White_Pos is a list of white positions
    self.color: 'white' | 'black'
    self.dice: [die, die] | [die, die, die, die]
        die: 1 | 2 | 3 | 4 | 5 | 6
    self.turns: [[cpos, cpos], ...]
    self.validState is True | False
    self.init(self, board, turnInfo) initializes the self.Black_Pos, self.White_Pos, and self.listofTurnInfo
    self.moving(self) uses the self.listofTurnInfo to move checkers and if a move is illegal, self.solution = False
    self.getSolution(self) returns the solution (if self.solution is true, then self.returning_board() is called.
    self.returning_board(self) returns either False or a Board

    """

    ### In order to initialize the Backgammon Board, pass in a dictionary (board) that has "white" and "black" keys
    ### which are attached to the value of a list with which squares hold checkers, and then a 3-item list
    ### with the color (string), dice (list of numbers 1-6), and turn (list of 2-item list of cpos)

    def __init__(self, board, turnInfo):
        ## Filling up the different player lists with the appropriate piece positions
        self.Black_Pos = [0 for i in range(26)]
        self.White_Pos = [0 for i in range(26)]
        self.source = turnInfo #The iHateTeamFifteen function uses the original die to backtrack/figure smth out
        self.color = turnInfo[0]
        self.dice = turnInfo[1]
        self.turns = turnInfo[2]

        ### These next steps are essentially cleaning up the board
        ### We reorder the Black moves since they're in descending order
        ### We also change the strings of the positions to their integral equivalents according to color

        for entry in (board["black"]):
            if entry == "bar":
                entry = 25
            elif entry == "home":
                entry = 0
            totalBlackCheckers = self.Black_Pos[entry] + 1
            self.Black_Pos[entry] = totalBlackCheckers
        for entry in (board["white"]):
            if entry == "bar":
                entry = 0
            elif entry == "home":
                entry = 25
            totalWhiteCheckers = self.White_Pos[entry] + 1
            self.White_Pos[entry] = totalWhiteCheckers
        newTurns = self.turnsCleanUp(self.turns)
        self.turns = newTurns
        self.validState = True
        self.moving()

    ### Turning position strings ('home' | 'bar') into ints within the listofTurns

    def turnsCleanUp(self, listofTurns):
        for turn in listofTurns:
            for turnNo in list(range(len(turn))):
                if self.color == 'white':
                    if turn[turnNo] == "bar":
                        turn[turnNo] = 0
                    elif turn[turnNo] == "home":
                        turn[turnNo] = 25
                elif self.color == 'black':
                    if turn[turnNo] == "bar":
                        turn[turnNo] = 25
                    elif turn[turnNo] == "home":
                        turn[turnNo] = 0
        return (listofTurns)

    ### Through the listofTurns, we move around pieces until we finally reach the end of the action set
    ### returns nothing
    def moving(self):
        while (len(self.turns) != 0) and (self.validState is True):
            newTurn = self.turns.pop(0)
            oldPos = newTurn[0]
            newPos = newTurn[1]
            if self.valid_move(oldPos, newPos):
                pass
            else:
                self.validState = False
            self.move(oldPos, newPos)
            ### If Victory Condition is met, then stop moving and end turn, returning the board
            if self.color == "black":
                if self.Black_Pos[0] == 15:
                    self.dice = []
                    self.turns = []
                    self.validState = True
            elif self.color == "white":
                if self.White_Pos[25] == 15:
                    self.dice = []
                    self.turns = []
                    self.validState = True
        ### This is a post moving check basically to see if all die have been used.
        ### If not, then we check if there's any moves left. If there are, then we change validState to False
        ### Cause that means that the user didn't input the remaining available move.
        if len(self.dice) != 0 and self.validState == True:
            movesLeft = False
            for die in self.dice:
                if self.color == "white":
                    for x in range(len(self.White_Pos)):
                        if self.White_Pos[x] != 0:
                            oldPos = x
                            newPos = oldPos + die
                            if newPos > 25:
                                newPos = 25
                            movesLeft = (movesLeft or self.valid_move(oldPos, newPos))
                elif self.color == "black":
                    for x in range(len(self.Black_Pos)):
                        if self.Black_Pos[x] != 0:
                            oldPos = x
                            newPos = oldPos - die
                            if newPos < 0:
                                newPos = 0
                            print("This is oldPos: " + str(oldPos))
                            print("This is newPos: " + str(newPos))
                            print("This is movesLeft: " + str(movesLeft))
                            print("This is self.valid_move: " + str(self.valid_move(oldPos, newPos)))
                            movesLeft = (movesLeft or self.valid_move(oldPos, newPos))
            if movesLeft == False:
                print("case hit")
                self.validState = True
            else:
                self.validState = False

    """
    ### I won't lie to you. This function is in direct response to Team 15's awful awful edge case. I hate it. I HATE IT.
    ### Essentially this is an optimization function, called after victory is achieved. It basically double checks if
    ### all the die were used in the last move to victory. If so, then great. If not, then it checks if the last die
    ### used was less than the distance between final position and victory. If so, then it sets validState to False.
    ### Confused? Me too.
    ### God, iHateTeamFifteen().
    def iHateTeamFifteen(self):
        iHateColor = self.source[0]
        iHateDice = self.source[1]
        iHateTurns = self.source[2]
        for x in range(len(iHateTurns)):
            if x == len(self.turns) - 1:
                pass
            else:
                distance = abs(iHateTurns[x][1] - iHateTurns[x][0])
                
    """

    ## So far, this function checks whether
    ## 1. Checkers are moved off the bar first
    ## 2. All checkers are in pos 1-6 before going home
    ## 3. Whether the checkers are moving in the right direction.
    ## 4. Whether a checker is moved from a valid position.
    ## 5. Whether the space moved to is a valid spot.
    ## 6. If valid moves are being made with dice

    def valid_move(self, oldPos, newPos):
        if self.color == "black":
            home = 0
            bar = 25
            otherpos = self.White_Pos
            pos = self.Black_Pos
            homeBoard = [0, 1, 2, 3, 4, 5, 6]
        elif self.color == "white":
            home = 25
            bar = 0
            otherpos = self.Black_Pos
            pos = self.White_Pos
            homeBoard = [19, 20, 21, 22, 23, 24, 25]
        # 1.Checkers are moved off the bar first
        if oldPos != bar:
            if pos[bar] == 0:
                pass
            else:
                return False

        # 2. All checkers are in homeboard before going home
        if newPos == home:
            sum = 0
            for space in homeBoard:
                sum = pos[space] + sum
            if sum != 15:
                return False

        # 3. If directionality is correct
        if self.color == "black":
            spaceDiff = newPos - oldPos
            if spaceDiff > 0:
                return False
            else:
                pass
        elif self.color == "white":
            spaceDiff = newPos - oldPos
            if spaceDiff < 0:
                return False
            else:
                pass

        # 4. Whether a checker is moved from a valid position.
        if pos[oldPos] <= 0:
            return False
        # 5. Whether the space moved to is a valid spot.
        if newPos == bar or newPos == home:
            pass
        else:
            if otherpos[newPos] >= 2:
                return False
        ## 6. If valid moves are being made with dice
        spacesMoved = abs(newPos - oldPos)
        dicePoppedCond = False
        ### 6a. Checking for movement that is not to home
        for dieNo in range(len(self.dice)):
            if spacesMoved == self.dice[dieNo]:
                dicePopped = spacesMoved
                dicePoppedCond = True
        if dicePoppedCond:
            self.dice.remove(dicePopped)
        else:
        ### 6b. Checking for movement that is to home if the distance is not the same
        ###     if newPos is not home, then return False. Special board rules don't apply.
            if newPos == home:
                sumDice = 0
                biggestDice = 0
                for die in self.dice:
                    sumDice = sumDice + die
                    if die > biggestDice:
                        biggestDice = die
                ### Checking now for if value of die is larger than distance for
                ### any remaining checker to imaginary point, and checking for furthest away point
                mostDist = 0
                farthestSpace = 26
                for x in range(len(pos)):
                    if pos[x] != 0:
                        distance = abs(x - home)
                        if mostDist < distance and distance != 0:
                            mostDist = distance
                            if self.color == "white":
                                farthestSpace = x
                            elif self.color == "black":
                                farthestSpace = x
                if (mostDist <= sumDice) and (oldPos == farthestSpace):
                    self.dice.remove(biggestDice)
                    return True
                else:
                    return False
            else:
                return False
        return True

    def move(self, oldPos, newPos):
        ### Moving black's pieces
        if self.color == "black":
            newPosValue = self.Black_Pos[newPos] + 1
            self.Black_Pos[newPos] = newPosValue
            oldPosValue = self.Black_Pos[oldPos] - 1
            self.Black_Pos[oldPos] = oldPosValue

            # Removing Blots back to bar
            if self.White_Pos[newPos] == 1:
                self.White_Pos[newPos] -= 1
                self.White_Pos[0] += 1

        ### Moving white's pieces
        elif self.color == "white":
            newPosValue = self.White_Pos[newPos] + 1
            self.White_Pos[newPos] = newPosValue
            oldPosValue = self.White_Pos[oldPos] - 1
            self.White_Pos[oldPos] = oldPosValue

            # Removing Blots back to bar
            if (self.Black_Pos[newPos]) == 1:
                self.Black_Pos[newPos] -= 1
                self.Black_Pos[25] += 1


    ### Returns the solution as either False or a Board (returns Board if the solution is True)
    def getSolution(self):
        if self.validState:
            return(self.returning_board())
        else:
            return(False)

    ### Uses the self.Black_Pos and self.White_Pos to create the board in the JSON format, and then returns that board
    def returning_board(self):
        BlackList = []
        WhiteList = []
        blackHomeCount = 0
        ### Reformatting the list of black checkers into the JSON list format...
        for x in range(len(self.Black_Pos)):
            if self.Black_Pos[x] == 0:
                pass
            else:
                if x == 25:
                    checkerPos = "bar"
                elif x == 0:
                    checkerPos = "home"
                else:
                    checkerPos = x
                for checkerCount in range(self.Black_Pos[x]):
                    if checkerPos == "bar":
                        BlackList.insert(0, checkerPos)
                    elif checkerPos == "home":
                        blackHomeCount = blackHomeCount + 1
                    else:
                        BlackList.append(checkerPos)
        ### Adding in the "home" for black checkers at the end
        for x in range(blackHomeCount):
            BlackList.append('home')
        ### Reformatting the list of white checkers into the JSON list format...
        for x in range(len(self.White_Pos)):
            if self.White_Pos[x] == 0:
                pass
            else:
                if x == 0:
                    checkerPos = "bar"
                elif x == 25:
                    checkerPos = "home"
                else:
                    checkerPos = x
                for checkerCount in range(self.White_Pos[x]):
                    WhiteList.append(checkerPos)
        ## Constructing final dictionary to be returned
        currBoard = {}
        currBoard["black"] = BlackList
        currBoard["white"] = WhiteList
        return(currBoard)

class Proxy_Backgammon_Board:

    """
    self.Real_Board holds the Real_Backgammon_Board initialization
    self.validSpaces is a list of valid spaces for the checkers to be on
    """

    ### In order to initialize the Real Backgammon Board, pass in a dictionary (board) that has "white" and "black" keys
    ### which are attached to the value of a list with which squares hold checkers, and then a 3-item list
    ### with the color (string), dice (list of numbers 1-6), and turn (list of 2-item list of cpos)

    ### This proxy initialization checks if the arguments being passed into the real board are correct. Also creates
    ### a list of valid checker-spaces to test the boards against for self.validSpaces

    def __init__(self, board, turnInfo):
        turnInfo = deepcopy(turnInfo)
        self.validSpaces = list(range(26))
        self.validSpaces[0] = "bar"
        self.validSpaces[25] = "home"
        self.counterColors = ["white", "black"]
        if self.Board_Check(board):
            pass
        else:
            raise("initialization input for board is not correct!")
        if self.Turn_Check(turnInfo):
            pass
        else:
            raise("turn_check is incorrect!")
        self.Real_Board = Real_Backgammon_Board(board, turnInfo)

    ### Returns the solution as either False or a Board (returns Board if the solution is True)
    def getSolution(self):
        board = self.Real_Board
        proxySolution = board.getSolution()
        if proxySolution == False:
            return(proxySolution)
        elif self.Board_Check(proxySolution):
            return(proxySolution)
        else:
            raise("getSolution is not returning the right data type")

    ### Checks if the input is a board (dictionary with 'white' and 'black' keys to a list of length 15),
    ### then returns True | False depending on if it matches the format
    def Board_Check(self, checkingBoard):
        if isinstance(checkingBoard, dict):
            whiteList = checkingBoard.get('white')
            blackList = checkingBoard.get('black')
            if (whiteList is None) or (blackList is None):
                raise("either white or black was missing as a key in the board dictionary")
            elif (len(whiteList) != 15) or (len(blackList) != 15):
                raise("the length of the list of cpos within the board was not 15")
            else:
                for entry in whiteList:
                    if entry not in self.validSpaces:
                        raise("invalid cpos in the list of white checkers")
                for entry in blackList:
                    if entry not in self.validSpaces:
                        raise("invalid cpos in the list of black checkers")
                return(True)
        else:
            raise("board is not a dictionary data type")

    ### Checks if the input is a 3-item list of turn based information [color, dice, turn], which:
        #color: 'white' | 'black'
        #dice: [die, die] | [die, die, die, die]
        #die: 1 | 2 | 3 | 4 | 5 | 6
        #turn: [[cpos, cpos], ...]
    ### then returns True | False depending on if it matches the format
    def Turn_Check(self, checkingTurnInfo):

        if len(checkingTurnInfo) != 3:
            raise("the turnInfo has an incorrect number of elements in the list!")
        # checking if the color arguments are correct
        color = checkingTurnInfo[0]
        if (not isinstance(color, str)):
            raise("the color argument of the turnInfo is an incorrect data type")
        else:
            if color not in self.counterColors:
                raise("the color argument of the turnInfo is an invalid color")
        # checking if the dice arguments are correct
        dice = checkingTurnInfo[1]
        if (len(dice) != 2) and (len(dice) != 4):
            raise("invalid number of die in game!")
        else:
            for die in dice:
                if isinstance(die, int):
                    if (die > 6) or (die < 1):
                        raise("one of the dice is an invalid integer value")
                    else:
                        pass
                else:
                    raise("one of the dice is an invalid data type")
        # checking if the turn arguments are correct
        turns = checkingTurnInfo[2]
        for turn in turns:
            if len(turn) != 2:
                raise("invalid number of cpos in one of the turns")
            else:
                for cpos in turn:
                    if cpos not in self.validSpaces:
                        raise("invalid cpos within one of the turns")

        return(True)