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


headers = {"Authentication": f"{keys[1]}"}


while True:
    cmd = input("$>")

    if cmd == "add_project":
        headers["project-name"] = input("Name: ")
        headers["project-image"] = input("Image path: ")
        headers["project-coords-x"] = input("X: ")
        headers["project-coords-y"] = input("Y: ")
        try:
            r = requests.post("http://churchofpepe.ddns.net:5000/add_project", headers=headers)
        except:
            print("conn error")
        print(r.text)

    if cmd == "projects":
        try:
            r = requests.get("http://churchofpepe.ddns.net:5000/get_projects", headers=headers)
        except:
            print("conn error")
        print(r.json())

    if cmd == "new_key":
        headers["key-name"] = input("Name: ")
        headers["key-level"] = input("Access level (1): ")
        if headers["key-level"] == "":
            headers["key-level"] = '1'
        r = requests.post("http://churchofpepe.ddns.net:5000/new_key", headers=headers)
        print(r.text)
            #print("conn error")

    if cmd == "del_key":
        headers["other-key"] = input("Key to delete !: ")
        y = input("U sure (y/n)")
        if y =="y":
            try:
                r = requests.post("http://churchofpepe.ddns.net:5000/del_key", headers=headers)
            except:
                print("conn error")
            print(r.text)
        else:
            print("Canceled.")
