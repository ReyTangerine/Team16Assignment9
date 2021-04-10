import json
import sys

intermediateObject = ""
d = json.JSONDecoder()
e = json.JSONEncoder()

def countCurly(string):
    stringaslist = list(string)
    return stringaslist.count("{") + stringaslist.count("}")

def validObject(content):
    contentList = list(content)
    if "{" in content and "}" in content and contentList.count("}") == contentList.count("{"):
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

    return outputObjects

def BackendProcessingMain(file):
    #print("This is inside Backendprocessing: " + str(file))
    listing = []
    listing.extend(parseJSON(file))
    # Verify all keys are "content"
    listing = [object for object in listing if list(object.keys())[0] == "content"]
    print(e.encode(BackendProcessingOfList(listing)))

def BackendProcessingOfList(output):
    output.sort(key=lambda item: item["content"])
    sortedArray = output
    return(sortedArray)