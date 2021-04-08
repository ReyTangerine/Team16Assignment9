import json
import fileinput

output = []
intermediateObject = ""
d = json.JSONDecoder()
e = json.JSONEncoder()

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

    return outputObjects

for line in fileinput.input():

    # Checking for black lines
    if line.isspace():
        continue

    # If object is split across multiple lines, compose the object into one string/line

    # If initial line is valid, parse it. Otherwise store it.
    if validObject(line):
        output.extend(parseJSON(line))
    else:
        intermediateObject = intermediateObject + line

    # If the stored object + the new line is valid, parse it, otherwise get the next line.
    if validObject(intermediateObject):
        output.extend(parseJSON(intermediateObject))
        intermediateObject = ""
    else:
        pass

# Verify all keys are "content"
output = [object for object in output if list(object.keys())[0] == "content"]
output.sort(key=lambda item: item["content"])
sortedArray = output

print(e.encode(sortedArray))
