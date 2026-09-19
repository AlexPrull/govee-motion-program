import time
import uuid
import requests
from config import API_KEY, DEVICE_ID, MODEL
from govee_api import set_brightness

URL = "https://openapi.api.govee.com/router/api/v1/device/state"
HEADERS = {"Govee-API-Key": API_KEY, "Content-Type": "application/json"}


def read_brightness():
    body = {
        "requestId": str(uuid.uuid4()),
        "payload": {"sku": MODEL, "device": DEVICE_ID},
    }
    r = requests.post(URL, headers=HEADERS, json=body, timeout=10)
    r.raise_for_status()
    for cap in r.json()["payload"]["capabilities"]:
        if cap.get("instance") == "brightness":
            return cap["state"]["value"]


for value in (1, 5, 10, 15, 20, 25, 30, 35, 40, 50, 75, 100):
    set_brightness(value)
    time.sleep(3)
    print(f"sent {value:>3} -> API reports {read_brightness()}")