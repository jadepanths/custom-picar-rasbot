import RPi.GPIO as GPIO

# Define IR sensor pins
AvoidSensorLeft = 21
AvoidSensorRight = 19
Avoid_ON = 22  # Power switch for IR sensors

# Set up GPIO for IR sensors
GPIO.setmode(GPIO.BOARD)
GPIO.setup(AvoidSensorLeft, GPIO.IN)
GPIO.setup(AvoidSensorRight, GPIO.IN)
GPIO.setup(Avoid_ON, GPIO.OUT)
GPIO.output(Avoid_ON, GPIO.HIGH)  # Turn on IR sensors

def detect_obstacle():
    """Returns which side has an obstacle detected."""
    left_sensor = GPIO.input(AvoidSensorLeft)
    right_sensor = GPIO.input(AvoidSensorRight)

    if left_sensor == 0 and right_sensor == 0:
        return "both"
    elif left_sensor == 0:
        return "left"
    elif right_sensor == 0:
        return "right"
    else:
        return "none"

if __name__ == "__main__":
    try:
        while True:
            detection = detect_obstacle()
            print(f"IR Detection: {detection}")
    except KeyboardInterrupt:
        print("Stopping IR sensor test.")
        GPIO.cleanup()
