import time
import random
from utils.ultrasonic import Ultrasonic
from utils.motor_control import RaspbotCar


# Initialize components
car = RaspbotCar()
sensor = Ultrasonic()

# Obstacle detection threshold (in cm)
OBSTACLE_DISTANCE = 15  # Stop if obstacle is within 15 cm

def avoid_obstacle():
    """Stops, reverses, and turns randomly to avoid obstacles."""
    print("Obstacle detected! Avoiding...")

    # Stop immediately
    car.stop()
    time.sleep(0.5)

    # Back up slightly
    car.run_backward(40)
    time.sleep(1)
    car.stop()

    # Choose a random turn direction
    turn_direction = random.choice(["left", "right"])
    if turn_direction == "left":
        print("Turning left...")
        car.turn_left()
    else:
        print("Turning right...")
        car.turn_right()
    
    # Turn for a random duration
    time.sleep(random.uniform(0.5, 1.5))
    car.stop()

    # Move forward again
    print("Resuming forward motion...")
    car.run_forward(70)

def main():
    """Continuously checks for obstacles and avoids them."""
    print("Starting autonomous navigation...")

    car.run_forward()  # Start moving forward

    try:
        while True:
            distance = sensor.get_distance()
            print(f"Distance: {distance:.2f} cm")

            if 0 < distance < OBSTACLE_DISTANCE:
                avoid_obstacle()

            time.sleep(0.1)  # Short delay to prevent excessive readings

    except KeyboardInterrupt:
        print("Stopping navigation...")
        car.stop()

if __name__ == "__main__":
    main()
