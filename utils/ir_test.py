import RPi.GPIO as GPIO
import time

# Set GPIO mode to BOARD (using physical pin numbers)
GPIO.setmode(GPIO.BOARD)

# Define IR sensor pins
AvoidSensorLeft = 21   # Left IR avoidance sensor
AvoidSensorRight = 19  # Right IR avoidance sensor
Avoid_ON = 22          # IR sensor power switch

# Set up GPIO pins
GPIO.setup(AvoidSensorLeft, GPIO.IN)
GPIO.setup(AvoidSensorRight, GPIO.IN)
GPIO.setup(Avoid_ON, GPIO.OUT)

# Turn on the IR avoidance sensors
GPIO.output(Avoid_ON, GPIO.HIGH)

try:
    print("IR Avoidance Sensor Test - Press CTRL+C to stop")
    while True:
        left_sensor = GPIO.input(AvoidSensorLeft)
        right_sensor = GPIO.input(AvoidSensorRight)

        if left_sensor == 0 and right_sensor == 0:
            print("Obstacle detected on BOTH sides!")
        elif left_sensor == 0:
            print("Obstacle detected on the LEFT!")
        elif right_sensor == 0:
            print("Obstacle detected on the RIGHT!")
        else:
            print("No obstacle detected.")

        time.sleep(0.5)  # Delay to prevent excessive prints

except KeyboardInterrupt:
    print("\nTest stopped by user. Cleaning up GPIO...")
    GPIO.cleanup()
