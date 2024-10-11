import RPi.GPIO as GPIO
from time import sleep

# Setup
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

# Define pin numbers
redPin = 12
greenPin = 19
bluePin = 13

# Set pins as outputs
GPIO.setup(redPin, GPIO.OUT)
GPIO.setup(greenPin, GPIO.OUT)
GPIO.setup(bluePin, GPIO.OUT)

# Function to turn off the LED
def turn_off():
    GPIO.output(redPin, GPIO.HIGH)
    GPIO.output(greenPin, GPIO.HIGH)
    GPIO.output(bluePin, GPIO.HIGH)

# Functions to control the LED colors
def red():
    GPIO.output(redPin, GPIO.LOW)
    GPIO.output(greenPin, GPIO.HIGH)
    GPIO.output(bluePin, GPIO.HIGH)

def green():
    GPIO.output(redPin, GPIO.HIGH)
    GPIO.output(greenPin, GPIO.LOW)
    GPIO.output(bluePin, GPIO.HIGH)

def yellow():
    GPIO.output(redPin, GPIO.LOW)
    GPIO.output(greenPin, GPIO.LOW)
    GPIO.output(bluePin, GPIO.HIGH)

# Testing colors
try:
    print("Testing Red...")
    red()
    sleep(2)  # Keep red on for 2 seconds

    print("Testing Green...")
    green()
    sleep(2)  # Keep green on for 2 seconds

    print("Testing Yellow...")
    yellow()
    sleep(2)  # Keep yellow on for 2 seconds

    print("Turning off the LED...")
    turn_off()

except KeyboardInterrupt:
    print("Exiting program...")

finally:
    turn_off()
    GPIO.cleanup()  # Reset all GPIO pins
