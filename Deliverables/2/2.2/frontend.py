import json
import fileinput
import backend
import math

d = json.JSONDecoder()
e = json.JSONEncoder()
fileinputted = fileinput.input()

def validObject(content):
    if "{" in content and "}" in content:
        return True
    else:
        return False

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
        outputObjects.append(object)
    #print("This is outputObjects: " + str(outputObjects))
    #print("This is outputObjects Type: " + str(type(outputObjects)))
    if outputObjects[0]['content'] >= 0 and outputObjects[0]['content'] <= 24:
        return outputObjects
    else:
        return None

    """
        if 0 <= object[0] <= 24:
            outputObjects.append(object)
        else:
            pass
    print("This is outputObjects" + str(outputObjects))
    return outputObjects
    """

def FrontendProcessing(file):
    output = []
    mainOutput = []
    intermediateObject = ""
    for line in file:
        # Checking for black lines
        if line.isspace():
            continue
        # If object is split across multiple lines, compose the object into one string/line
        # If initial line is valid, parse it. Otherwise store it.
        if validObject(line):
            newList = parseJSON(line)
            if newList == None:
                pass
            else:
                output.extend(newList)
        else:
            intermediateObject = intermediateObject + line
        # If the stored object + the new line is valid, parse it, otherwise get the next line.
        if validObject(intermediateObject):
            newList = parseJSON(intermediateObject)
            if newList == None:
                pass
            else:
                output.extend(newList)
                intermediateObject = ""
        else:
            pass
    # Verify all keys are "content"
    output = [object for object in output if list(object.keys())[0] == "content"]
    ## Splitting the list into lists of ten
    #print(str(output))
    NumberOfGroups = len(output) / 10
    NumberOfGroups = math.trunc(NumberOfGroups)
    for x in range(NumberOfGroups):
        mainOutput.append(output[(10*x):(10 + 10*x)])
    for x in range(len(mainOutput)):
        """
        unsortedList = json.dumps(mainOutput[x])
        unsortedList = unsortedList.replace('[', '')
        unsortedList = unsortedList.replace(']', '')
        newString = ""
        newStringMark = 0
        for y in range(len(unsortedList)):
            if unsortedList[y] == ',':
                newString = newString + unsortedList[newStringMark:(y)] + ' /n'
                newStringMark = (y + 1)
            elif y == len(unsortedList) - 1:
                newString = newString + unsortedList[newStringMark:(y+1)] + ' /n'
                newStringMark = (y + 1)
            else:
                pass
        unsortedList = newString
        """
        #f = open("ProcessingJSON.json", "w")
        #json.dump(mainOutput[x], f)
        #f.close()
        #f = open("ProcessingJSON.json", "r")
        with open("ProcessingJSON.json", 'r+') as f:
            f.truncate(0)
        with open('ProcessingJSON.json', 'a') as outfile:
            for entry in mainOutput[x]:
                json.dump(entry, outfile)
                outfile.write('\n')
        sortedList = backend.BackendProcessing(open('ProcessingJSON.json', 'r'))
        mainOutput[x] = d.decode(sortedList)
    print("This is mainOutput: " + str(mainOutput))
    print(e.encode(mainOutput))
    return(e.encode(mainOutput))

FrontendProcessing(fileinputted)