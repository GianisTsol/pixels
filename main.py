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


church_headers = {"Authentication": f"{keys[1]}"}

HEADERS = {"Authorization": f"Bearer {keys[0]}"}
data = {"x": 123,"y": 12,"rgb": "87CEEB",}

def sendpixel(x, y, rgb):
    global data
    data['x'] = int(x)
    data['y'] = int(y)
    data['rgb'] = str(rgb)

    result = requests.post(
      "https://pixels.pythondiscord.com/set_pixel",
      json=data,
      headers=HEADERS
    )
    result.raise_for_status()
    print(result.json()["message"])

    info = result.headers

    global remaining
    remaining = int(info["requests-remaining"])
    global reset
    reset = float(info["requests-reset"])


result = requests.head("https://pixels.pythondiscord.com/set_pixel",headers=HEADERS)
remaining = result.headers['Requests-Remaining']

while True:
    r = requests.get("http://churchofpepe.ddns.net:5000/get_task",headers=church_headers)
    print(r.text)
    if r.text == "\"no tasks\"":
        print("No tasks available! - sleeping...")
        time.sleep(20)
    else:
        task = r.json()
        if remaining == 0:
            print("Write waiting... " + str(reset))
            time.sleep(reset)
            result = requests.head("https://pixels.pythondiscord.com/set_pixel",headers=HEADERS)
            remaining = result.headers['Requests-Remaining']

        sendpixel(task["x"], task["y"], task["color"])
        church_headers["task-id"] = str(task["id"])
        result = requests.post("http://churchofpepe.ddns.net:5000/task_done",headers=church_headers)
