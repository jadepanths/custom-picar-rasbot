import sys
import tty
import termios
import time
from utils.motor_control import RaspbotCar  # Corrected import

# Initialize the motor control
car = RaspbotCar()

def readchar():
    """Reads a single character from the keyboard"""
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch

def keyboard_control():
    """Controls the car using keyboard input"""
    print("Use W/A/S/D to move, 6 to increase speed, 4 to decrease speed, and Q to quit.")

    while True:
        key = readchar()

        if key == '6':
            if car.speed <= 90:
                car.speed += 10
                print(f"Speed increased: {car.speed}")
        elif key == '4':
            if car.speed >= 10:
                car.speed -= 10
                print(f"Speed decreased: {car.speed}")
        elif key == 'w':
            print("Moving forward")
            car.run_forward()
        elif key == 's':
            print("Moving backward")
            car.run_backward()
        elif key == 'a':
            print("Turning left")
            car.turn_left()
        elif key == 'd':
            print("Turning right")
            car.turn_right()
        elif key == 'q':
            print("Stopping and exiting...")
            car.stop()
            break
        else:
            print("Stopping")
            car.stop()

if __name__ == '__main__':
    keyboard_control()
