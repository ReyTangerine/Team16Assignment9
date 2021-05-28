from copy import deepcopy
import time

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
    self.moving(self, color, dice, turns) uses the self.listofTurnInfo to move checkers and if a move is illegal, self.solution = False
    self.getSolution(self) returns the solution (if self.solution is true, then self.returning_board() is called.
    self.returning_board(self) returns either False or a Board

    """

    ### In order to initialize the Backgammon Board, pass in a dictionary (board) that has "white" and "black" keys
    ### which are attached to the value of a list with which squares hold checkers, and then a 3-item list
    ### with the color (string), dice (list of numbers 1-6), and turn (list of 2-item list of cpos)

    def __init__(self, board):
        ## Filling up the different player lists with the appropriate piece positions
        self.Black_Pos = [0 for i in range(26)]
        self.White_Pos = [0 for i in range(26)]
        self.turnCount = 0

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
    def new_moving(self, color, dice, turns):
        self.turnCount += 1
        self.color = color
        self.dice = dice
        self.turns = turns
        newTurns = self.turnsCleanUp(self.turns)
        self.turns = newTurns
        self.validState = True
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

    ### Through the listofTurns, we move around pieces until we finally reach the end of the action set
    ### returns nothing
    def moving(self, color, dice, turns):
        self.turnCount += 1
        self.color = color
        self.dice = dice
        self.turns = turns
        newTurns = self.turnsCleanUp(self.turns)
        self.turns = newTurns
        self.validState = True
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
                            movesLeft = (movesLeft or self.valid_move(oldPos, newPos))
            if movesLeft == False:
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
                # print("it was rule 1!")
                return False

        # 2. All checkers are in homeboard before going home
        if newPos == home:
            sum = 0
            for space in homeBoard:
                sum = pos[space] + sum
            if sum != 15:
                # print("it was rule 2!")
                return False

        # 3. If directionality is correct
        if self.color == "black":
            spaceDiff = newPos - oldPos
            if spaceDiff > 0:
                # print("it was rule 3!")
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
            # print("it was rule 4!")
            return False
        # 5. Whether the space moved to is a valid spot.
        if newPos == bar or newPos == home:
            pass
        else:
            if otherpos[newPos] >= 2:
                # print("it was rule 5!")
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
                    # print("it was rule 6! Inner Conditional")
                    return False

            else:
                # print("it was rule 6! Outer Conditional")
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
        if self.turnCount == 0:
            return(self.returning_board())
        else:
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

    def __init__(self, board):
        self.validSpaces = list(range(26))
        self.validSpaces[0] = "bar"
        self.validSpaces[25] = "home"
        self.counterColors = ["white", "black"]
        if self.Board_Check(board):
            pass
        else:
            raise("initialization input for board is not correct!")
        self.Real_Board = Real_Backgammon_Board(board)

    ### Void function that moves pieces according to color, dice, and turns
    def new_moving(self, color, dice, turns):
        self.Real_Board.new_moving(color, dice, turns)

    ### Void function that moves pieces according to color, dice, and turns
    def moving(self, color, dice, turns):
        self.Color_Check(color)
        self.Dice_Check(dice)
        if color == "black":
            bar = 25
            home = 0
        else:
            bar = 0
            home = 25
        for move in turns:
            for cposNo in range(len(move)):
                if move[cposNo] == home:
                    move[cposNo] = "home"
                elif move[cposNo] == bar:
                    move[cposNo] = "bar"
        self.Turn_Check(turns)
        for move in turns:
            for cpos in move:
                if cpos == "home":
                    cpos = home
                elif cpos == "bar":
                    cpos = bar
        self.Real_Board.moving(color, dice, turns)

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

    # checking if the color arguments are correct
    def Color_Check(self, color):

        if (not isinstance(color, str)):
            raise("the color argument of the turnInfo is an incorrect data type")
        else:
            if color not in self.counterColors:
                raise("the color argument of the turnInfo is an invalid color")

    # checking if the dice arguments are correct
    def Dice_Check(self, dice):
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
    def Turn_Check(self, turns):
        for turn in turns:
            if len(turn) != 2:
                raise("invalid number of cpos in one of the turns")
            else:
                for cpos in turn:
                    if cpos not in self.validSpaces:
                        raise("invalid cpos within one of the turns")

        return(True)

    def valid_move(self, oldPos, newPos):
        assert isinstance(oldPos, int)
        assert isinstance(newPos, int)
        self.Real_Board.valid_move(oldPos, newPos)

    def move(self, oldPos, newPos):
        assert isinstance(oldPos, int)
        assert isinstance(newPos, int)
        self.Real_Board.move(oldPos, newPos)

    def returning_board(self):
        return self.Real_Board.returning_board()

# self.children is a list of child nodes
# self.diceRemaining is list of remaining die
# self.allTurns is a list of moves that lead up to this point (the current move should always be the last element)
# self.board is an updated Proxy_Backgammon_Board

class Node:
    def __init__(self, children, diceRemaining, allTurns, board):
        self.children = children
        self.diceRemaining = diceRemaining
        self.allTurns = allTurns
        self.board = board

class turnTree:
    def __init__(self, board, color, die):
        self.board = board
        self.die = die
        self.rootNode = Node([], die, [], board)
        self.color = color
        self.calculate_children(self.rootNode)
        self.allTurns = []
        if self.color == "black":
            self.home = 0
            self.bar = 25
        else:
            self.home = 25
            self.bar = 0
        ### If there's 2 die, calculate children for two layers of nodes
        # start_time = time.time()
        for childNode in self.rootNode.children:
            self.calculate_children(childNode)
            ### If there's 4 die, calculate children for two layers of nodes
            if len(die) == 4 and len(childNode.children) > 0:
                for grandchild in childNode.children:
                    self.calculate_children(grandchild)
                    for great_grandchild in grandchild.children:
                        self.calculate_children(great_grandchild)
        # print("--- grandchild + great_grandchild: %s seconds ---" % (time.time() - start_time))
        ### If there's 4 die, calculate children for four layers of nodes
        self.get_tree_leaves(self.rootNode)
        ### Removing duplicates while preserving original turn order
        seen = []
        newAllTurns = []
        sortedAllTurns = deepcopy(self.allTurns)
        for turnNo, turn in enumerate(sortedAllTurns):
            turn.sort()
            if turn in seen:
                pass
            else:
                seen.append(turn)
                newAllTurns.append(self.allTurns[turnNo])
        self.allTurns = newAllTurns

        for turn in self.allTurns:
            ### Sort if the final destination is home according to color
            isHomeTheFinalDestination = False
            for move in turn:
                if move[1] == self.home:
                    isHomeTheFinalDestination = True
            if isHomeTheFinalDestination:
                if self.color == "black":
                    turn.sort(reverse=True)
                else:
                    turn.sort()
            ### Changing all 0's and 25's back to "bar" and "home", depending on color
            for move in turn:
                if move[0] is self.bar:
                    move[0] = "bar"
                elif move[0] is self.home:
                    move[0] = "home"
                if move[1] is self.bar:
                    move[1] = "bar"
                elif move[1] is self.home:
                    move[1] = "home"

    def get_all_turns(self):
        ### we remove extraneous since because we generate all turns move by move, there will be some turns
        ### that are illegal but each move separately is legal (especially in homeboard condition)
        ### so this final check helps remove those additional edge cases.
        editedTurns = self.removeAllExtraneous(self.allTurns)
        editedTurns = self.removeHomeHome(editedTurns)
        return editedTurns

    def removeAllExtraneous(self, turns):
        newTurns = []
        for turn in turns:
            newTurn = deepcopy(turn)
            newBoard = deepcopy(self.board)
            testBoard = Proxy_Backgammon_Board(newBoard)
            testDie = deepcopy(self.die)
            testBoard.new_moving(self.color, testDie, newTurn)
            if testBoard.getSolution() is not False:
                newTurns.append(turn)
            else:
                pass
        return newTurns

    def removeHomeHome(self, turns):
        for turnNo in range(len(turns)):
            turn = turns[turnNo]
            toBeRemoved = []
            for moveNo in range(len(turn)):
                if turn[moveNo][0] == "home" and turn[moveNo][0] == "home":
                    toBeRemoved.append(turn[moveNo])
            if len(toBeRemoved) != 0:
                for removeIt in toBeRemoved:
                    turns[turnNo].remove(removeIt)
        return turns

    def get_tree_leaves(self, rootNode):
        if rootNode.children == []:
            self.allTurns.append(rootNode.allTurns)
        else:
            for child in rootNode.children:
                self.get_tree_leaves(child)

    def sort_board(self, turn):
        if self.color == "white":
            pass

        # whitepieces = [25 if item == "home" else item for item in whitepieces]
        # whitepieces = [0 if item == "bar" else item for item in whitepieces]
        # blackpieces = [0 if item == "home" else item for item in blackpieces]
        # blackpieces = [25 if item == "bar" else item for item in blackpieces]
        # blackpieces.sort()
        # whitepieces.sort()
        # whitepieces = ["home" if item == 25 else item for item in whitepieces]
        # whitepieces = ["bar" if item == 0 else item for item in whitepieces]
        # blackpieces = ["home" if item == 0 else item for item in blackpieces]
        # blackpieces = ["bar" if item == 25 else item for item in blackpieces]
        return turn

    def calculate_children(self, currNode):
        currBoard = deepcopy(currNode.board)
        if self.color == "white":
            pieces = currBoard.get("white")
            pieces = [25 if item == "home" else item for item in pieces]
            pieces = [0 if item == "bar" else item for item in pieces]
            bar = 0
            home = 25
            direction = 1
        elif self.color == "black":
            pieces = currBoard.get("black")
            pieces = [25 if item == "bar" else item for item in pieces]
            pieces = [0 if item == "home" else item for item in pieces]
            bar = 25
            home = 0
            direction = -1
        diceList = deepcopy(currNode.diceRemaining)
        seenTurn = []
        seenPosition = []
        for dice in diceList:
            if bar in pieces:
                pieces = [bar]
            if home in pieces:
                pieces = [piece for piece in pieces if piece != home]
            for piece in pieces:
                if piece in seenPosition:
                    continue
                else:
                    seenPosition.append(piece)
                currNodeCopy = deepcopy(currNode)
                oldPos = piece
                newPos = oldPos + (direction * dice)
                ### If the newPos overextends, then we will go back to "home"
                if self.color == "white":
                    if newPos > 25:
                        newPos = 25
                elif self.color == "black":
                    if newPos < 0:
                        newPos = 0
                turn = [[oldPos, newPos]]
                turn1 = deepcopy(turn)
                testBoard = deepcopy(currBoard)
                testBoard = Proxy_Backgammon_Board(testBoard)
                remainingDie = deepcopy(currNodeCopy.diceRemaining)
                remainingDieCopy = deepcopy(remainingDie)
                testBoard.new_moving(self.color, remainingDieCopy, turn1)
                isLegal = testBoard.getSolution()
                if isLegal == False:
                    pass
                else:
                    remainingDie.remove(dice)
                    ### turning numbers back to string
                    if self.color == "white":
                        turn = ["bar" if item == 0 else item for item in turn]
                        turn = ["home" if item == 25 else item for item in turn]
                    elif self.color == "black":
                        turn = ["bar" if item == 25 else item for item in turn]
                        turn = ["home" if item == 0 else item for item in turn]
                    currAllTurns = deepcopy(currNodeCopy.allTurns)
                    currAllTurns.extend(turn)
                    newNode = Node([], remainingDie, currAllTurns, isLegal)
                    if turn in seenTurn:
                        pass
                    else:
                        seenTurn.append(turn)
                        currNode.children.append(newNode)

        # whitepieces = ["home" if item == 25 else item for item in pieces]
        # whitepieces = ["bar" if item == 0 else item for item in pieces]
        # blackpieces = ["bar" if item == 0 else item for item in pieces]
        # blackpieces = ["home" if item == 25 else item for item in pieces]

# ourTree = turnTree({'black': [1, 1, 1, 1, 1, 1, 2, 3, 3, 4, 6, 6, 10, 15, 16],
#                     'white': [20, 21, 21, 22, 22, 22, 23, 23, 23, 23, 24, 24, 24, 24, 'home']},"white",[6,1])
# print(ourTree.get_all_turns())