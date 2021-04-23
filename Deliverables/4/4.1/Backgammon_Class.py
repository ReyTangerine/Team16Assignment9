class Real_Backgammon_Board:

    """
    self.Black_Pos is a list of black positions
    self.White_Pos is a list of white positions
    self.listofTurnInfo is a 3-item list of turn based information [color, dice, turn], used in self.moving(), which:
        color: 'white' | 'black'
        dice: [die, die] | [die, die, die, die]
        die: 1 | 2 | 3 | 4 | 5 | 6
        turn: [[cpos, cpos], ...]
    self.solution is True | False

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
        self.listofActions = self.parse_moves(turnInfo)

        if self.valid_move(board, turnInfo):
            self.moving()
            self.solution = True
        else:
            self.solution = False

        for entry in (board["black"]):
            if entry == "bar":
                entry = 0
            elif entry == "home":
                entry = 25
            totalBlackCheckers = self.Black_Pos[entry] + 1
            self.Black_Pos[entry] = totalBlackCheckers
        for entry in (board["white"]):
            if entry == "bar":
                entry = 0
            elif entry == "home":
                entry = 25
            totalWhiteCheckers = self.White_Pos[entry] + 1
            self.White_Pos[entry] = totalWhiteCheckers
        self.listofTurnInfo = turnInfo

    ### THIS IS INCOMPLETE AS WE STILL HAVE NOT IMPLEMENTED THE RULE ENGINE
    ### Through the listofTurns, we move around pieces until we finally reach the end of the action set
    ### returns nothing
    def moving(self):
        while len(self.listofActions) != 0:
            newAction = self.listofActions.pop()
            oldPos = newAction[1]
            newPos = newAction[2]
            ### Turning position strings into ints
            if oldPos == "bar":
                oldPos = 0
            elif oldPos == "home":
                oldPos = 25
            if newPos == "bar":
                newPos = 0
            elif newPos == "home":
                newPos = 25
            ### Moving black's pieces
            if newAction[0] == "black":
                newPosValue = self.Black_Pos[newPos] + 1
                self.Black_Pos[newPos] = newPosValue
                oldPosValue = self.Black_Pos[oldPos] - 1
                self.Black_Pos[oldPos] = oldPosValue
            ### Moving white's pieces
            elif newAction[0] == "white":
                newPosValue = self.White_Pos[newPos] + 1
                self.White_Pos[newPos] = newPosValue
                oldPosValue = self.White_Pos[oldPos] - 1
                self.White_Pos[oldPos] = oldPosValue

    ### Returns the solution as either False or a Board (returns Board if the solution is True)
    def getSolution(self):
        if self.solution == True:
            return(self.returning_board())
        else:
            return(False)

    ### Uses the self.Black_Pos and self.White_Pos to create the board in the JSON format, and then returns that board
    def returning_board(self):
        BlackList = []
        WhiteList = []
        ### Reformatting the list of black checkers into the JSON list format...
        for x in range(len(self.Black_Pos)):
            if self.Black_Pos[x] == 0:
                pass
            else:
                if x == 0:
                    checkerPos = "bar"
                elif x == 25:
                    checkerPos = "home"
                else:
                    checkerPos = x
                for checkerCount in range(self.Black_Pos[x]):
                    BlackList.append(checkerPos)
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

    ## So far, this function checks whether
    ## 1. Checkers are moved off the bar first
    ## 2. Whether a checker is moved from a valid position.
    def valid_move(self, board, turnInfo):
        color = turnInfo[0]
        dice = turnInfo[1]
        turns = turnInfo[2]

        # 1.Checkers are moved off the bar first
        barCount = sum(turn.count("bar") for turn in turns)
        if board.get(color).count("bar") != barCount:
            return False

        # 2. Whether a checker is moved from a valid position.
        moveFromLocations = [turn[1] for turn in self.listofActions]
        numCheckersAfterMoving = {location:board.get(color).count(location) -
                                   moveFromLocations.count(location) for location in moveFromLocations}
        #print(numCheckersAfterMoving)
        for numCheckers in numCheckersAfterMoving.values():
            if numCheckers <= 0:
                return False

        return True

    # Reformats 4.1 input into how it was for 3.1

    ## TODO-- Need to convert "home" & "bar" to numbers. Beware of issues this causes with future "bar" & "home" conversions.

    def parse_moves(self, turnInfo):
        color = turnInfo[0]
        turns = turnInfo[2]
        ## Puts the smaller move before the bigger move it's white's turn
        ## and vice versa for black.
        if color == "black":
            moves = [[color, *sorted(turn, reverse=True)] for turn in turns]
        elif color == "white":
            moves = [[color, *sorted(turn)] for turn in turns]

        return moves


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




### Testing Cases
