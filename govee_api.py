import uuid
import requests
from config import API_KEY, DEVICE_ID, MODEL

BASE_URL = "https://openapi.api.govee.com/router/api/v1/device/control"

HEADERS = {
    "Govee-API-Key": API_KEY,
    "Content-Type": "application/json",
}


def _send(capability: dict):
    body = {
        "requestId": str(uuid.uuid4()),
        "payload": {
            "device": DEVICE_ID,
            "sku": MODEL,
            "capability": capability,
        },
    }

    response = requests.post(
        BASE_URL,
        headers=HEADERS,
        json=body,
        timeout=5,
    )
    response.raise_for_status()
    return response.json()


def activate_scene(param_id: int, scene_id: int):
    return _send({
        "type": "devices.capabilities.dynamic_scene",
        "instance": "lightScene",
        "value": {
            "paramId": param_id,
            "id": scene_id,
        },
    })


def set_brightness(level: int):
    return _send({
        "type": "devices.capabilities.brightness",
        "instance": "brightness",
        "value": level,
    })


def set_power(on: bool):
    return _send({
        "type": "devices.capabilities.on_off",
        "instance": "powerSwitch",
        "value": 1 if on else 0,
    })