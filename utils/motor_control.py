import smbus
import time

class RaspbotCar:
    """Yahboom Raspbot I2C Motor Control"""
    
    def __init__(self):
        self._addr = 0x16  # Yahboom's I2C motor driver address
        self._device = smbus.SMBus(1)  # I2C bus 1
        self.speed = 50  # Default speed

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

    def run_forward(self):
        """Move forward with an initial kick"""
        self.Ctrl_Car(1, 80, 1, 80)  # Short burst of 80% power
        time.sleep(0.2)  # Give it 0.2 seconds to start moving
        self.Ctrl_Car(1, self.speed, 1, self.speed)  # Return to normal speed

    def run_backward(self):
        """Move backward with an initial kick"""
        self.Ctrl_Car(0, 80, 0, 80)
        time.sleep(0.2)
        self.Ctrl_Car(0, self.speed, 0, self.speed)

    def turn_left(self):
        """Turn left with an initial kick"""
        self.Ctrl_Car(0, 80, 1, 80)
        time.sleep(0.2)
        self.Ctrl_Car(0, self.speed, 1, self.speed)

    def turn_right(self):
        """Turn right with an initial kick"""
        self.Ctrl_Car(1, 80, 0, 80)
        time.sleep(0.2)
        self.Ctrl_Car(1, self.speed, 0, self.speed)

    def stop(self):
        """Stop the car"""
        try:
            reg = 0x02
            self._device.write_byte_data(self._addr, reg, 0x00)
        except:
            print("I2C error: Car_Stop")
