"""
Main automation loop for Govee motion-based lighting.

- Runs continuously on a Raspberry Pi
- Activates a Govee scene when motion is detected after a configured hour
- Adjusts brightness based on time of day
- Allows manual shutoff; automation re-triggers on motion
- Scene activation is rate-limited via a cooldown timer
"""

import time
from datetime import datetime
from govee_api import activate_scene, set_brightness
from sensors.PIRlogic import motion_detected

# Import configuration values
from config import (
    LONGING_PARAM_ID,
    LONGING_SCENE_ID,
    LIGHT_ON_HOUR,
    DIM_HOUR,
    DAY_BRIGHTNESS,
    NIGHT_BRIGHTNESS,
)

# Timestamp of last scene activation (used to enforce cooldown)
last_scene_time = None

# Minimum time between scene activations (seconds)
SCENE_COOLDOWN = 60 * 60  # 1 hour

# Tracks current brightness to avoid redundant API calls
current_brightness = None

print("Govee motion system started")

while True:
    now = datetime.now()
    hour = now.hour

    try:
        # Activate scene on motion after the configured start hour,
        # but only if the cooldown period has expired
        if hour >= LIGHT_ON_HOUR and motion_detected():
            if (
                last_scene_time is None
                or time.time() - last_scene_time > SCENE_COOLDOWN
            ):
                activate_scene(LONGING_PARAM_ID, LONGING_SCENE_ID)
                last_scene_time = time.time()

        # Adjust brightness based on time of day
        if hour >= LIGHT_ON_HOUR:
            desired = (
                DAY_BRIGHTNESS if hour < DIM_HOUR else NIGHT_BRIGHTNESS
            )
            if desired != current_brightness:
                set_brightness(desired)
                current_brightness = desired

    # Catch all exceptions so the loop never exits unexpectedly
    except Exception as e:
        print("Error:", e)

    # Sleep to limit loop frequency and API calls
    time.sleep(5)