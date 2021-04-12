import Contracts

class BackgammonBoard:

    """
    self.request is a string of the request given
    self.Black_Pos is a list of black positions
    self.White_Pos is a list of white positions
    self.listofActions is the remaining list of actions required
    self.query is a list of the query in case it's a query-type request
    self.answer is a dictionary OR string with the correct query/answer
    """

    ### In order to initialize the Backgammon Board, pass in a dictionary, with one key "request" to the value of
    ### a list with a dictionary. This dictionary has "white" and "black" keys which are attached to the value of
    ### a list with which squares hold checkers, and then the rest of the list followed with moves. This is basically
    ### the raw JSON input data structure.
    ### Then, this returns either a board (in the same list format as the input board) or a whole number.
    ### Dict -> Dict | Int

    def __init__(self, dict):
        Contracts.dict_contract(dict)
        DictKeys = list(dict.keys())
        self.request = DictKeys[0]
        Contracts.string_contract(self.request)
        #print("Request is: " + self.request)
        RemainingList = dict[self.request]
        Contracts.list_contract(RemainingList)
        ## Filling up the different player lists with the appropriate piece positions
        BG_Dictionary = RemainingList.pop(0)
        self.Black_Pos = [0 for i in range(26)]
        self.White_Pos = [0 for i in range(26)]
        for entry in (BG_Dictionary["black"]):
            if entry == "bar":
                entry = 0
            elif entry == "home":
                entry = 25
            totalBlackCheckers = self.Black_Pos[entry] + 1
            self.Black_Pos[entry] = totalBlackCheckers
        for entry in (BG_Dictionary["white"]):
            if entry == "bar":
                entry = 0
            elif entry == "home":
                entry = 25
            totalWhiteCheckers = self.White_Pos[entry] + 1
            self.White_Pos[entry] = totalWhiteCheckers
        self.listofActions = RemainingList
        if self.request == "ends-with-board":
            self.ends_with_board()
        elif self.request == "ends-with-query":
            self.query = self.listofActions.pop()
            self.ends_with_query()

    ### Fulfilling the "ends with board" request, this function solves all the way to the end of the board
    ### and calls a helper function to return the new board
    def ends_with_board(self):
        self.moving()
        #print("Solving all the way for the new board.")
        #print("This is the new board: " + "\n" + str(self.returning_board()))
        self.answer = self.returning_board()

    def ends_with_query(self):
        self.moving()
        #print("Ends with query.")
        #print("This is the new board: " + "\n" + str(self.returning_board()))
        if self.query[1] == "bar":
            self.query[1] = 0
        elif self.query[1] == "home":
            self.query[1] = 25
        Contracts.string_contract(self.query[0])
        Contracts.whole_number_contract(self.query[1])
        if self.query[0] == "black":
            self.answer = self.Black_Pos[self.query[1]]
        elif self.query[0] == "white":
            self.answer = self.White_Pos[self.query[1]]

    ### Through the listofActions, we move around pieces until we finally reach the end of the action set
    ### returns nothing
    def moving(self):
        while len(self.listofActions) != 0:
            newAction = self.listofActions.pop()
            Contracts.list_of_three_contract(newAction)
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
            Contracts.string_contract(newAction[0])
            Contracts.integer_contract(oldPos)
            Contracts.integer_contract(newPos)
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
        Contracts.dict_contract(currBoard)
        return(currBoard)

    def solve(self):
        return(self.answer)

### Testing Cases
#BGDict = {"ends-with-query":[{"black":["bar",1,1,1,1,2,3,4,4,5,5,23,24,"home","home"],"white":["bar",1,2,3,15,16,18,18,20,20,20,22,23,24,"home"]},["black","home",1],["black","home",1],["white","home","bar"],["white",24,23], ["white",24]]}
#BG_Instance = BackgammonBoard(BGDict)
#answer = BG_Instance.solve()
#print(str(answer))