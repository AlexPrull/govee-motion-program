# Govee Motion Lighting (Raspberry Pi)


## Description
This project runs on a Raspberry Pi (Zero 2 W) and controls Govee Wi-Fi LED strip lights using the Govee OpenAPI.
Lighting behavior is automated based on time of day and motion detection from a PIR sensor. The Raspberry Pi acts as a local controller and runs continuously.


## Features
  - Govee OpenAPI integration (scenes, brightness, power)
  - Time-based lighting behavior
  - Motion-triggered scene activation
  - Designed for headless operation
  - Safe handling of API secrets (not committed)


## Hardware
  - Raspberry Pi Zero 2 W
  - Micro USB power supply
  - HC-SR501 PIR motion sensor
  - Govee Wi-Fi LED strip (e.g. H612D)

**If using Ethernet:**
  - USB-to-Ethernet adapter
  - USB OTG adapter


## Config Example
Create a `config.py` file in the root folder (this file is intentionally gitignored):
```python
API_KEY = "your-api-key"
DEVICE_ID = "your-govee-device-id"
MODEL = "H612D"

EXAMPLE_PARAM_ID = 172
EXAMPLE_SCENE_ID = 190

LIGHT_ON_HOUR = 17
DIM_HOUR = 21
DAY_BRIGHTNESS = 20
NIGHT_BRIGHTNESS = 1
```


## Notes
  - The Raspberry Pi is intended to run continuously
  - Manual control of the lights (via physical buttons or app) is supported and intended for shutoff; automation resumes on the next motion event.