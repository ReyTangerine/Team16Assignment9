import json
import fileinput
import sys

output = []
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


str = sys.stdin.read()

output.extend(parseJSON(str))
# for line in fileinput.input():
#     # Checking for black lines
#     if line.isspace():
#         continue
#     # If object is split across multiple lines, compose the object into one string/line
#     # If initial line is valid, parse it. Otherwise store it (in intermediateObject).
#     if ((countCurly(line) + countCurly(intermediateObject)) % 2 == 1):
#         pass
#     elif validObject(line):
#         output.extend(parseJSON(line))
#         continue
#     else:
#         pass
#
#     # If intermediateObject + the new line is valid, parse it, otherwise get the next line.
#     if ((countCurly(line) + countCurly(intermediateObject)) % 2 == 1):
#         intermediateObject = intermediateObject + line
#     elif validObject(intermediateObject):
#         output.extend(parseJSON(intermediateObject))
#         intermediateObject = ""
#     else:
#         intermediateObject = intermediateObject + line
#
# if validObject(intermediateObject):
#     output.extend(parseJSON(intermediateObject))

# Verify all keys are "content"
output = [object for object in output if list(object.keys())[0] == "content"]
output.sort(key=lambda item: item["content"])
sortedArray = output

print(e.encode(sortedArray))
