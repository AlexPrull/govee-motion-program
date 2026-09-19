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
# --- Govee API Info ---
API_KEY = "your-api-key"
DEVICE_ID = "your-govee-device-id"
MODEL = "your-govee-device-model"

# --- Scene to trigger on motion ---
PARAM_ID = 172  # PARAM_ID for 'Longing'
SCENE_ID = 190  # SCENE_ID for 'Longing'

# --- Schedule (minutes since midnight) ---
LIGHT_ON_MINUTES = 17 * 60  # 5:00 PM
DIM_MINUTES = 21 * 60       # 9:00 PM

# --- Brightness (1-)
DAY_BRIGHTNESS = 30   # 92% on the H612D
NIGHT_BRIGHTNESS = 1  # 6% on the H612D
```


## What each setting does
`API_KEY` - Your Govee API key. Request one in the Govee Home app.
`DEVICE_ID` - Unique ID of your light. (see below)
`MODEL` - Your light's model/SKU (e.g. `H612D`). (see below)
`PARAM_ID` / `SCENE_ID` - The IDs identifying the scene to activate on motion. (see below)
`LIGHT_ON_MINUTES` - Earliest time of day the motion sensor can trigger the scene, in minutes since midnight.
`DIM_MINUTES` - Time when brightness switches from day to night level, in minutes since midnight.
`DAY_BRIGHTNESS` - Brightness used between `LIGHT_ON_MINUTES` and `DIM_MINUTES`.
`NIGHT_BRIGHTNESS` - Brightness used after `DIM_MINUTES`.

> **Brightness:** The Govee API documents a 1-100 range, but on the H612D the value you
> send is not a percentage. Each step raises brightness by about 2.5%, and any value
> around 40 or higher is full brightness (e.g. 1 ≈ 6%, 10 ≈ 29%, 20 ≈ 54%, 35 ≈ 92%).
> Other models may scale differently. Run `python setup/Calibrate.py` (after setting config)
> to see what your device reports for each value.


## Finding your device ID, model, and scene IDs
1. Get your API key from the Govee Home app.
2. Open `Query.py` and set `API_KEY` at the top.
3. Run it:
```bash
   python Query.py
```
4. Copy the printed `DEVICE_ID` and `MODEL` into `config.py`, then pick a scene from the list and copy its `PARAM_ID` and `SCENE_ID`.


## Notes
  - The Raspberry Pi is intended to run continuously
  - Manual control of the lights (via physical buttons or app) is supported and intended for shutoff; automation resumes on the next motion event.