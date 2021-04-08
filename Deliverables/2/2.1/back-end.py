import json
import fileinput

inputObjects = []
d = json.JSONDecoder()
e = json.JSONEncoder()

for line in fileinput.input():

    ## These lines make sure the inputs are JSON Compatible
    if line.isspace():
        continue
    line = line.replace("\'","\"")

    # Since each dict ends with "}", split on it and remove the last trailing \n.
    # Then add the "}" back in.
    parsedline = json.loads(json.dumps(line)).split("}")
    parsedline.pop()
    for JSONobject in parsedline:
        JSONobject = JSONobject + "}"
        object = d.decode(JSONobject)
        inputObjects.append(object)

inputObjects.sort(key=lambda item: item["content"])
sortedArray = inputObjects

print(e.encode(sortedArray))
