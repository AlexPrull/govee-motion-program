"""
Main automation loop for Govee motion-based lighting.

- Runs continuously on a Raspberry Pi
- Activates a Govee scene when motion is detected after a configured time
- Adjusts brightness based on time of day
- Allows manual shutoff; automation re-triggers on motion
- Scene activation is rate-limited via a cooldown timer
"""

import time
from datetime import datetime
from govee_api import activate_scene, set_brightness, is_power_on
from sensors.PIRlogic import motion_detected

# Import configuration values
from config import (
    PARAM_ID,
    SCENE_ID,
    LIGHT_ON_MINUTES,
    DIM_MINUTES,
    DAY_BRIGHTNESS,
    NIGHT_BRIGHTNESS,
)

last_scene_time = None  # Timestamp of last scene activation (used to enforce cooldown)
SCENE_COOLDOWN = 60 * 60  # Minimum time between scene activations (seconds) Set to 1 hour
current_brightness = None  # Tracks current brightness to avoid redundant API calls
last_power_check = 0  # Timestamp of last API call
power_check_interval = 60  # Seconds between API calls
device_is_on = False  # cached power state

print("Govee motion system started", flush=True)

try:
    device_is_on = is_power_on()
    last_power_check = time.time()
except Exception as e:
    print("Startup power check failed:", e)

while True:
    now = datetime.now()
    current_time = (now.hour * 60) + now.minute

    # Updating device_is_on every minute
    if (time.time() - last_power_check) > power_check_interval:
        try:
            device_is_on = is_power_on()
        except Exception as e:
            print("Error fetching device state:", e)
        last_power_check = time.time()

    try:
        # Activate scene on motion after the configured start hour,
        # but only if the cooldown period has expired
        if current_time >= LIGHT_ON_MINUTES and motion_detected():
            if ( (last_scene_time is None) or ((time.time() - last_scene_time) > SCENE_COOLDOWN) ):
                activate_scene(PARAM_ID, SCENE_ID)
                desired = DAY_BRIGHTNESS if current_time < DIM_MINUTES else NIGHT_BRIGHTNESS
                set_brightness(desired)
                current_brightness = desired
                last_scene_time = time.time()

        # Adjust brightness based on time of day
        if device_is_on and current_time >= LIGHT_ON_MINUTES:
            desired = DAY_BRIGHTNESS if current_time < DIM_MINUTES else NIGHT_BRIGHTNESS
            if current_brightness != desired:
                set_brightness(desired)
                current_brightness = desired

    # Catch all exceptions so the loop never exits unexpectedly
    except Exception as e:
        print("Error:", e)

    # Sleep to limit loop frequency and API calls
    time.sleep(1)