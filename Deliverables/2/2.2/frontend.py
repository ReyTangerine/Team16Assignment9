import json
import sys
import math
sys.path.append('../2.1/')
import backend

intermediateObject = ""
d = json.JSONDecoder()
e = json.JSONEncoder()

str1 = sys.stdin.read()

def validObject(content):
    contentList = list(content)
    if "{" in content and "}" in content and contentList.count("}") == contentList.count("{"):
        return True
    else:
        return False

## Used with JSON to clean strings
## Removes the start of the string until the '{' is reached
def string_cleaner(string):
    while string[0] != '{':
        string = string[1:]
    return(string)

def parseJSON(input):
    outputObjects = []

    # Change ' to " and remove newlines
    input = input.replace("\'", "\"")
    input = input.replace("\n", "")

    # Since each dict ends with "}", split on it and remove the last trailing \n.
    # Then add the "}" back in.
    parsedJSON = json.loads(json.dumps(input)).split("}")
    print(str(parsedJSON))

    # Removing Empty elements in the dictionary
    parsedJSON.pop()
    for parsedTokenNumber in range(len(parsedJSON) - 1):
        if parsedJSON[parsedTokenNumber] == '':
            parsedJSON.pop(parsedTokenNumber)

    # Since some jerks added in characters for each line between the dictionary entries
    # We need to remove those characters (now in the start of the parsedJSON list entries)
    # We can remove these bad boys by eliminating tokens that aren't '['
    for parsedTokenNumber in range(len(parsedJSON)- 1):
        if parsedJSON[parsedTokenNumber] != '{':
            newString = string_cleaner(parsedJSON[parsedTokenNumber])
            parsedJSON[parsedTokenNumber] = newString
    #print("This is parsedJSON: " + str(parsedJSON))

    for JSONobject in parsedJSON:
        JSONobject = JSONobject + "}"
        if validObject(JSONobject):
            object = d.decode(JSONobject)

            # Cleaning up the objects from incorrect values
            # Ensuring that all values are between 0 & 24
            checking = object.get("content")
            if checking != None:
                contentValue = object['content']
                object.clear()
                object['content'] = contentValue
                if type(object['content']) is int:
                    if object['content'] >= 0 and object['content'] <= 24:
                        outputObjects.append(object)
                    else:
                        pass
                else:
                    pass
            else:
                pass
        else:
            pass
    return outputObjects

def FrontendProcessing(FrontendInput):
    #print("This is Front End Input: " + str(FrontendInput))
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