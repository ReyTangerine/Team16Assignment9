import json
import fileinput

inputObjects = []
d = json.JSONDecoder()
e = json.JSONEncoder()

for line in fileinput.input():
    object = d.decode(line)
    inputObjects.append(object)

inputObjects.sort(key=lambda item: list(item.values()))
sortedArray = inputObjects

print(e.encode(sortedArray))
