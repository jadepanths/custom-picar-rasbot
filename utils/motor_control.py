import smbus
import time

class RaspbotCar:
    """Yahboom Raspbot I2C Motor Control"""
    
    def __init__(self):
        self._addr = 0x16  # Yahboom's I2C motor driver address
        self._device = smbus.SMBus(1)  # I2C bus 1
        self.speed = 40  # Default speed

    def write_array(self, reg, data):
        """Send block data to I2C device"""
        try:
            self._device.write_i2c_block_data(self._addr, reg, data)
        except:
            print("I2C error: write_array")

    def Ctrl_Car(self, l_dir, l_speed, r_dir, r_speed):
        """Control left & right motors"""
        try:
            reg = 0x01  # Motor control register
            data = [l_dir, l_speed, r_dir, r_speed]
            self.write_array(reg, data)
        except:
            print("I2C error: Ctrl_Car")

    def run_forward(self, speed=None):
        """Move forward with a customizable speed (default: self.speed)"""
        speed = speed if speed is not None else self.speed
        self.Ctrl_Car(1, 200, 1, 200)  # Initial burst
        time.sleep(0.1)
        self.Ctrl_Car(1, 40, 1, 40)  # Use provided speed or default

    def run_backward(self, speed=None):
        """Move backward with a customizable speed (default: self.speed)"""
        speed = speed if speed is not None else self.speed
        self.Ctrl_Car(0, 200, 0, 200)  # Initial burst
        time.sleep(0.1)
        self.Ctrl_Car(0, 40, 0, 40)  # Use provided speed or default

    def turn_left(self):
        """Turn left with a stronger initial kick"""
        self.Ctrl_Car(0, 200, 1, 200)
        time.sleep(0.5)
        self.Ctrl_Car(0, 40, 1, 40)

    def turn_right(self):
        """Turn right with a stronger initial kick"""
        self.Ctrl_Car(1, 200, 0, 200)
        time.sleep(0.5)
        self.Ctrl_Car(1, 40, 0, 40)


    def stop(self):
        """Stop the car"""
        try:
            reg = 0x02
            self._device.write_byte_data(self._addr, reg, 0x00)
        except:
            print("I2C error: Car_Stop")
