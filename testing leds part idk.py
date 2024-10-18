import RPi.GPIO as GPIO
import time

class LEDTest:
    def __init__(self):
        # GPIO setup for LEDs
        self.LED_RED = 12    # GPIO pin for Red LED
        self.LED_YELLOW = 16  # GPIO pin for Yellow LED
        self.LED_GREEN = 26  # GPIO pin for Green LED

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.LED_RED, GPIO.OUT)
        GPIO.setup(self.LED_YELLOW, GPIO.OUT)
        GPIO.setup(self.LED_GREEN, GPIO.OUT)

        # Initialize LEDs (Turn them off initially)
        GPIO.output(self.LED_RED, GPIO.LOW)
        GPIO.output(self.LED_YELLOW, GPIO.LOW)  
        GPIO.output(self.LED_GREEN, GPIO.LOW)

    def test_leds(self):
        try:
            while True:
                print("Turning on Red LED")
                GPIO.output(self.LED_RED, GPIO.HIGH)
                time.sleep(1)  # Keep Red LED on for 1 second
                print("Turning off Red LED")
                GPIO.output(self.LED_RED, GPIO.LOW)

                print("Turning on Yellow LED")
                GPIO.output(self.LED_YELLOW, GPIO.HIGH)
                time.sleep(1)  # Keep Yellow LED on for 1 second
                print("Turning off Yellow LED")
                GPIO.output(self.LED_YELLOW, GPIO.LOW)

                print("Turning on Green LED")
                GPIO.output(self.LED_GREEN, GPIO.HIGH)
                time.sleep(1)  # Keep Green LED on for 1 second
                print("Turning off Green LED")
                GPIO.output(self.LED_GREEN, GPIO.LOW)

        except KeyboardInterrupt:
            print("Exiting program")
        finally:
            GPIO.cleanup()  # Clean up GPIO resources when exiting

# Create an instance of the class and run the LED test
if __name__ == "__main__":
    led_test = LEDTest()
    led_test.test_leds()
