import json

with open("../data.json", 'r') as file:
    o = json.load(file)
    for item in o[0]['items']:
        print(item)