import numpy as np
import time
import math
from utils.ultrasonic import Ultrasonic
from utils.motor_control import RaspbotCar

# Initialize components
car = RaspbotCar()
sensor = Ultrasonic()

# Define the map grid (100x100, each cell = 1 cm)
grid_size = 100
center_x, center_y = grid_size // 2, grid_size // 2  # Robot starts at center
map_grid = np.zeros((grid_size, grid_size), dtype=int)

# Define scanning parameters
angle_step = 15  # Degrees per turn step
total_turns = 360 // angle_step  # Number of turns for full 360-degree scan
car.speed = 45

def update_map():
    """Perform a full scan by rotating the car instead of using a servo."""
    print("Starting 360-degree scan...")

    for i in range(total_turns):
        car.stop()
        time.sleep(0.75)

        # Take distance reading
        distance = sensor.get_distance()
        angle = i * angle_step  # Calculate the angle of measurement

        print(f"Angle: {angle}, Distance: {distance:.2f} cm")

        # Convert distance into grid coordinates
        if 0 < distance < grid_size // 2:
            x = int(distance * math.cos(math.radians(angle))) + center_x
            y = int(distance * math.sin(math.radians(angle))) + center_y
            
            if 0 <= x < grid_size and 0 <= y < grid_size:
                map_grid[y, x] = 1  # Mark obstacle

        # Rotate the car slightly (left turn)
        car.turn_left()
        time.sleep(0.12)
        
    car.stop()
    print("Mapping complete.")

    # Mark the center position with a unique identifier (e.g., "X")
    map_grid[center_y, center_x] = 2  # Mark robot's position

    np.save("environment_map.npy", map_grid)  # Save map for later use
    print("Map saved as 'environment_map.npy'")

    # Print the grid representation in the console
    print("\nFinal Mapped Grid:\n")
    for row in map_grid:
        print("".join(["█" if cell == 1 else ("X" if cell == 2 else ".") for cell in row]))  # Console-friendly display

# Run the mapping process
print("Updating Map Starts in 3 Seconds")
time.sleep(3)
update_map()
