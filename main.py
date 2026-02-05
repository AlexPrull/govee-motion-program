import time
from datetime import datetime
from govee_api import activate_scene, set_brightness
from sensors.PIRlogic import motion_detected

from config import (
    LONGING_PARAM_ID,
    LONGING_SCENE_ID,
    LIGHT_ON_HOUR,
    DIM_HOUR,
    DAY_BRIGHTNESS,
    NIGHT_BRIGHTNESS,
)

last_scene_time = None
SCENE_COOLDOWN = 60 * 60  # 1 hour
current_brightness = None

print("Govee motion system started")

while True:
    now = datetime.now()
    hour = now.hour

    try:
        if hour >= LIGHT_ON_HOUR and motion_detected():
            if (
                last_scene_time is None
                or time.time() - last_scene_time > SCENE_COOLDOWN
            ):
                activate_scene(LONGING_PARAM_ID, LONGING_SCENE_ID)
                last_scene_time = time.time()

        if hour >= LIGHT_ON_HOUR:
            desired = (
                DAY_BRIGHTNESS if hour < DIM_HOUR else NIGHT_BRIGHTNESS
            )
            if desired != current_brightness:
                set_brightness(desired)
                current_brightness = desired

    except Exception as e:
        print("Error:", e)

    time.sleep(5)