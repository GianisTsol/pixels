import requests
import pickle
import json
import time

try:
    with open('keys.pickle', 'rb') as handle:
            keys = pickle.load(handle)
except:
    key1 = input("Please entr your pixels api key: ")
    key2 = input("Please enter your church API key: ")
    keys = (key1, key2)
    with open('keys.pickle', 'wb') as handle:
        pickle.dump(keys, handle, protocol=pickle.HIGHEST_PROTOCOL)


headers = {"api-key": f"{keys[1]}"}


while True:
    cmd = input("$>")

    if cmd == "add_project":
        headers["project-name"] = input("Name: ")
        headers["project-image"] = input("Image path: ")
        headers["project-coords-x"] = input("X: ")
        headers["project-coords-y"] = input("Y: ")
        try:
            r = requests.post("http://localhost:5000/add_project", headers=headers)
        except:
            print("conn error")
        print(r.text)

    if cmd == "projects":
        try:
            r = requests.get("http://localhost:5000/get_projects", headers=headers)
        except:
            print("conn error")
        print(r.json())
