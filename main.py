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

remaining = 0

task = {}

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
    try:
        result.raise_for_status()
    except:
        print("error setting pixel")

    info = result.headers

    global remaining
    remaining = int(info["requests-remaining"])
    global reset
    reset = float(info["requests-reset"])

def check_remaining():
    global remaining
    result = requests.head("https://pixels.pythondiscord.com/set_pixel",headers=HEADERS)

    if "requests-remaining" in result.headers:
        remaining = int(result.headers['Requests-Remaining'])
    if "cooldown-reset" in result.headers:
        print("Set pixel cooldown reset. ", int(result.headers["cooldown-reset"]))
        time.sleep(int(result.headers["cooldown-reset"]))
    if remaining == 0:
        print("waiting... " + str(reset))
        time.sleep(reset)
        remaining = result.headers['Requests-limit']

while True:
    r = requests.get("http://churchofpepe.ddns.net:5000/get_task",headers=church_headers)
    try:
        task = json.loads(r.text)

        check_remaining()

        print(f"Setting pixel { task['x'] }, { task['y'] } with color { task['color'] } for project { task['source'] }")
        sendpixel(task["x"], task["y"], task["color"])
        church_headers["task-id"] = str(task["id"])
        result = requests.post("http://churchofpepe.ddns.net:5000/task_done",headers=church_headers)

    except Exception as e:
        print("No tasks available! - sleeping...")
        print(e)
        time.sleep(20)
