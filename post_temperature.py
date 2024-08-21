import requests
import random

url = "http://localhost:5000/temperature"

MIN_TEMP = 15.0
MAX_TEMP = 38.0

current_temperature = random.uniform(MIN_TEMP, MAX_TEMP)

UP = 1
DOWN = -1

GOING = UP

for i in range(120):
    roll = random.randint(0, 10)
    if roll == 10:
        if GOING == UP:
            GOING = DOWN
        else:
            GOING = UP

    delta = round(random.uniform(-0.1, 2.3), 2)
    if GOING == UP:
        current_temperature += delta
    else:
        current_temperature -= delta

    if current_temperature >= MAX_TEMP:
        GOING = DOWN
    if current_temperature <= MIN_TEMP:
        GOING = UP

    resp = requests.post(url, json={
        "temperature": round(current_temperature, 2),
        "device_id": "test_device_002"
    })

    print(f"{i}: {resp.status_code}")