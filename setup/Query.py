"""
Setup helper for Govee Motion Lighting.

Finds your Govee device ID and model, then lists the scenes available
for that device so you can pick PARAM_ID and SCENE_ID for config.py.
Not used by the main automation runtime.

Usage:
    1. Set API_KEY below
    2. Run: python Query.py
"""

import sys
import uuid
import requests

API_KEY = "your-api-key"

BASE_URL = "https://openapi.api.govee.com/router/api/v1"
HEADERS = {"Govee-API-Key": API_KEY, "Content-Type": "application/json"}


def get_devices():
    response = requests.get(f"{BASE_URL}/user/devices", headers=HEADERS, timeout=10)
    response.raise_for_status()
    return response.json().get("data", [])


def get_scenes(device_id, model):
    body = {
        "requestId": str(uuid.uuid4()),
        "payload": {"sku": model, "device": device_id},
    }
    response = requests.post(f"{BASE_URL}/device/scenes", headers=HEADERS, json=body, timeout=10)
    response.raise_for_status()
    return response.json()


def choose_device(devices):
    if len(devices) == 1:
        return devices[0]
    print("Multiple devices found:")
    for i, d in enumerate(devices, start=1):
        print(f"  {i}. {d.get('deviceName', 'Unnamed')} ({d['sku']})")
    while True:
        choice = input("Enter the number of the device to use: ").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(devices):
            return devices[int(choice) - 1]
        print("Invalid choice, try again.")


def main():
    if API_KEY == "your-api-key":
        sys.exit("Set API_KEY at the top of this file first.")

    try:
        devices = get_devices()
    except requests.RequestException as e:
        sys.exit(f"Could not fetch devices: {e}")

    if not devices:
        sys.exit("No devices found for this API key.")

    device = choose_device(devices)
    device_id, model = device["device"], device["sku"]

    print(f"\nDEVICE_ID = \"{device_id}\"")
    print(f"MODEL = \"{model}\"")

    # Brightness range is device-specific
    for capability in device.get("capabilities", []):
        if capability.get("instance") == "brightness":
            r = capability.get("parameters", {}).get("range", {})
            print(f"BRIGHTNESS RANGE = {r.get('min')} to {r.get('max')}")
    
    try:
        data = get_scenes(device_id, model)
    except requests.RequestException as e:
        sys.exit(f"Could not fetch scenes: {e}")

    print("\nAvailable scenes (name: PARAM_ID, SCENE_ID):")
    found = False
    for capability in data.get("payload", {}).get("capabilities", []):
        for option in capability.get("parameters", {}).get("options", []):
            value = option.get("value", {})
            print(f"  {option.get('name')}: {value.get('paramId')}, {value.get('id')}")
            found = True

    if not found:
        print("  No scenes parsed. Raw response:")
        print(data)


if __name__ == "__main__":
    main()