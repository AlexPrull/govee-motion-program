from gpiozero import MotionSensor

pir = MotionSensor(17)

def motion_detected():
    return pir.motion_detected