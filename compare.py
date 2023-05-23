import json


def compare_json(file1, file2):
    with open(file1, "r") as json_file1:
        data1 = json.load(json_file1)
    with open(file2, "r") as json_file2:
        data2 = json.load(json_file2)

    return data1 == data2


file1 = "json/data17.1.json"
file2 = "json/data17.1.json"

if compare_json(file1, file2):
    print("JSON files the same.")
else:
    print("JSON files differents.")
