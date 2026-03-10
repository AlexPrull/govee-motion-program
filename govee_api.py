"""
Govee OpenAPI helper functions.

This module provides a small abstraction layer over the Govee device
control endpoint. It handles request construction, authentication,
and error handling so higher-level automation code does not need to
deal with raw HTTP requests or API details.
"""

import uuid
import requests
from config import API_KEY, DEVICE_ID, MODEL

# Base endpoint for all Govee device control actions
BASE_URL = "https://openapi.api.govee.com/router/api/v1/device/control"
# Base endpoint for querying device state
STATE_URL = "https://openapi.api.govee.com/router/api/v1/device/state"

# Common headers required for all Govee API requests
HEADERS = {
    "Govee-API-Key": API_KEY,
    "Content-Type": "application/json",
}


def _send(capability: dict):
    """
    Send a control request to the Govee API.

    This internal helper constructs the full request payload,
    attaches a unique request ID, and sends the request to
    the Govee device control endpoint.

    Args:
        capability (dict): A Govee capability payload describing
                           the desired action (scene, brightness, power, etc.)

    Returns:
        dict: Parsed JSON response from the Govee API

    Raises:
        requests.exceptions.HTTPError: If the API returns a non-2xx status
    """
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
    """
    Activate a dynamic lighting scene on the Govee device.

    Args:
        param_id (int): Parameter ID associated with the scene
        scene_id (int): Scene ID to activate

    Returns:
        dict: API response
    """
    return _send({
        "type": "devices.capabilities.dynamic_scene",
        "instance": "lightScene",
        "value": {
            "paramId": param_id,
            "id": scene_id,
        },
    })


def set_brightness(level: int):
    """
    Set the brightness level of the Govee light.

    Args:
        level (int): Brightness level (typically 1–100)

    Returns:
        dict: API response
    """
    return _send({
        "type": "devices.capabilities.brightness",
        "instance": "brightness",
        "value": level,
    })


# Not currently used in main.py but provided for completeness
def set_power(on: bool):
    """
    Turn the Govee light on or off.

    Args:
        on (bool): True to turn on, False to turn off

    Returns:
        dict: API response
    """
    return _send({
        "type": "devices.capabilities.on_off",
        "instance": "powerSwitch",
        "value": 1 if on else 0,
    })


def get_device_state():
    """
    Fetch the current state of the Govee device.

    Returns:
        dict: Full device state response from API
    """
    body = {
        "requestId": str(uuid.uuid4()),
        "payload": {
            "device": DEVICE_ID,
            "sku": MODEL,
        },
    }

    response = requests.post(
        STATE_URL,
        headers=HEADERS,
        json=body,
        timeout=5,
    )
    response.raise_for_status()
    return response.json()


def is_power_on() -> bool:
    """
    Return True if the light is currently powered on.
    """
    data = get_device_state()

    # Govee returns capabilities list inside payload
    capabilities = data.get("payload", {}).get("capabilities", [])

    for cap in capabilities:
        if cap.get("instance") == "powerSwitch":
            state = cap.get("state", {})
            value = state.get("value")
            return value == 1 or value == "on" or value is True

    return False