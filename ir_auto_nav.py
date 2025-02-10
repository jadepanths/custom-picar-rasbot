import time
import random
import RPi.GPIO as GPIO
from utils.ultrasonic import Ultrasonic
from utils.motor_control import RaspbotCar
from utils.ir_sensor import detect_obstacle  # Import IR detection function

# Initialize components
car = RaspbotCar()
sensor = Ultrasonic()

# Obstacle detection threshold (in cm)
OBSTACLE_DISTANCE = 15  # Stop if obstacle is within 15 cm

def avoid_obstacle():
    """Stops, reverses, and turns away from obstacles based on IR sensor input."""
    print("Obstacle detected! Avoiding...")

    # Stop immediately
    car.stop()
    time.sleep(0.5)

    # Read IR sensor values
    detection = detect_obstacle()

    # Determine turn direction based on IR sensors
    if detection == "both":
        print("Obstacle detected on BOTH sides. Backing up and turning randomly.")
        car.run_backward()
        time.sleep(1)
        car.stop()
        turn_direction = random.choice(["left", "right"])
    elif detection == "left":
        print("Obstacle detected on LEFT. Turning right.")
        turn_direction = "right"
    elif detection == "right":
        print("Obstacle detected on RIGHT. Turning left.")
        turn_direction = "left"
    else:
        print("No IR detection, using ultrasonic sensor for avoidance.")
        turn_direction = random.choice(["left", "right"])

    # Perform turn with updated duration (2-4 seconds)
    if turn_direction == "left":
        car.turn_left()
    else:
        car.turn_right()

    time.sleep(random.uniform(2, 4))
    car.stop()

    # Move forward again
    print("Resuming forward motion.")
    car.run_forward()

def main():
    """Continuously checks for obstacles and avoids them using IR and ultrasonic sensors."""
    print("Starting autonomous navigation...")

    car.run_forward()  # Start moving forward

    try:
        while True:
            distance = sensor.get_distance()
            detection = detect_obstacle()

            print(f"Distance: {distance:.2f} cm | IR Detection: {detection}")

            if distance < OBSTACLE_DISTANCE or detection != "none":
                avoid_obstacle()

            time.sleep(0.1)  # Short delay to prevent excessive readings

    except KeyboardInterrupt:
        print("Stopping navigation...")
        car.stop()
        GPIO.cleanup()

if __name__ == "__main__":
    main()
