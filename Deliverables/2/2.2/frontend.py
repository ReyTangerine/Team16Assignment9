import json
import sys
import math
#sys.path.append('../2.1/')
import backend

intermediateObject = ""
d = json.JSONDecoder()
e = json.JSONEncoder()

str1 = sys.stdin.read()

def parseJSON(input):
    outputObjects = []

    # Change ' to " and remove newlines
    input = input.replace("\'", "\"")
    input = input.replace("\n", "")

    # Since each dict ends with "}", split on it and remove the last trailing \n.
    # Then add the "}" back in.
    parsedJSON = json.loads(json.dumps(input)).split("}")
    parsedJSON.pop()

    for JSONobject in parsedJSON:
        JSONobject = JSONobject + "}"
        object = d.decode(JSONobject)

        # Cleaning up the objects from incorrect values
        # Ensuring that all values are between 0 & 24

        if object['content'] >= 0 and object['content'] <= 24:
            outputObjects.append(object)
        else:
            pass
    return outputObjects

def FrontendProcessing(FrontendInput):
    output = []
    mainOutput = []
    output.extend(parseJSON(FrontendInput))
    # Verify all keys are "content"
    output = [object for object in output if list(object.keys())[0] == "content"]
    ## Splitting the list into lists of ten
    NumberOfGroups = len(output) / 10
    NumberOfGroups = math.trunc(NumberOfGroups)
    for x in range(NumberOfGroups):
        mainOutput.append(output[(10 * x):(10 + 10 * x)])
    for x in range(len(mainOutput)):
        sortedList = backend.BackendProcessingOfList(mainOutput[x])
        mainOutput[x] = sortedList
    print(e.encode(mainOutput))

FrontendProcessing(str1)