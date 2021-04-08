import json
import fileinput

inputObjects = []
d = json.JSONDecoder()
e = json.JSONEncoder()

for line in fileinput.input():
    if line.isspace():
        continue
    line = line.replace("\'","\"")
    object = d.decode(line)
    inputObjects.append(object)

inputObjects.sort(key=lambda item: item["content"])
sortedArray = inputObjects

print(e.encode(sortedArray))
