import RPi.GPIO as GPIO
import time

class Ultrasonic:
    """Class for controlling an ultrasonic distance sensor"""

    def __init__(self, trig_pin=16, echo_pin=18, timeout=0.03):
        self.trig_pin = trig_pin
        self.echo_pin = echo_pin
        self.timeout = timeout

        # Set up GPIO
        GPIO.setmode(GPIO.BOARD)  # Use BOARD mode to match Yahboom setup
        GPIO.setup(self.trig_pin, GPIO.OUT)
        GPIO.setup(self.echo_pin, GPIO.IN)

    def get_distance(self):
        """Measure distance using the ultrasonic sensor"""
        GPIO.output(self.trig_pin, GPIO.LOW)
        time.sleep(0.000002)
        GPIO.output(self.trig_pin, GPIO.HIGH)
        time.sleep(0.000015)
        GPIO.output(self.trig_pin, GPIO.LOW)

        timeout_start = time.time()

        while not GPIO.input(self.echo_pin):
            if time.time() - timeout_start > self.timeout:
                return -1  # Timeout error
        pulse_start = time.time()

        while GPIO.input(self.echo_pin):
            if time.time() - pulse_start > self.timeout:
                return -1  # Timeout error
        pulse_end = time.time()

        distance = ((pulse_end - pulse_start) * 340 / 2) * 100  # Convert to cm
        return round(distance, 2)

    def distance_test(self, samples=5):
        """Take multiple distance readings and return the average"""
        distances = []
        for _ in range(samples):
            dist = self.get_distance()
            if dist > 0 and dist < 500:  # Valid range
                distances.append(dist)
            time.sleep(0.01)

        if len(distances) > 2:
            avg_distance = sum(distances[1:4]) / 3
            print(f"Distance: {avg_distance:.2f} cm")
            return avg_distance
        return -1  # Invalid reading

if __name__ == "__main__":
    try:
        sensor = Ultrasonic()
        while True:
            sensor.distance_test()
            time.sleep(1)
    except KeyboardInterrupt:
        print("Ending")
        GPIO.cleanup()
