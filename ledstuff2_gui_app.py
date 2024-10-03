import RPi.GPIO as GPIO
from time import sleep
import requests

GPIO.setwarnings(False)

GPIO.setmode(GPIO.BCM)

# Set red, green, and blue pins
redPin = 12
greenPin = 19
bluePin = 13

# Set pins as outputs
GPIO.setup(redPin, GPIO.OUT)
GPIO.setup(greenPin, GPIO.OUT)
GPIO.setup(bluePin, GPIO.OUT)

# Functions to control the LED colors
def turnOff():
    GPIO.output(redPin, GPIO.HIGH)
    GPIO.output(greenPin, GPIO.HIGH)
    GPIO.output(bluePin, GPIO.HIGH)

def white():
    GPIO.output(redPin, GPIO.LOW)
    GPIO.output(greenPin, GPIO.LOW)
    GPIO.output(bluePin, GPIO.LOW)

def red():
    GPIO.output(redPin, GPIO.LOW)
    GPIO.output(greenPin, GPIO.HIGH)
    GPIO.output(bluePin, GPIO.HIGH)

def green():
    GPIO.output(redPin, GPIO.HIGH)
    GPIO.output(greenPin, GPIO.LOW)
    GPIO.output(bluePin, GPIO.HIGH)

def blue():
    GPIO.output(redPin, GPIO.HIGH)
    GPIO.output(greenPin, GPIO.HIGH)
    GPIO.output(bluePin, GPIO.LOW)

def yellow():
    GPIO.output(redPin, GPIO.LOW)
    GPIO.output(greenPin, GPIO.LOW)
    GPIO.output(bluePin, GPIO.HIGH)

def purple():
    GPIO.output(redPin, GPIO.LOW)
    GPIO.output(greenPin, GPIO.HIGH)
    GPIO.output(bluePin, GPIO.LOW)

def lightBlue():
    GPIO.output(redPin, GPIO.HIGH)
    GPIO.output(greenPin, GPIO.LOW)
    GPIO.output(bluePin, GPIO.LOW)

# Function to get the user's status from the REST API
def get_user_status():
    url = 'http://<your-api-endpoint>'  # Replace with your API endpoint
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json().get('status', None)  # Assuming the status is returned in the JSON response
        else:
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error connecting to API: {e}")
        return None

# Map statuses to LED colors
def set_led_color_by_status(status):
    if status == "chilling":
        blue()  # Blue for 'chilling'
    elif status == "not available":
        red()   # Red for 'not available'
    elif status == "busy":
        yellow()  # Yellow for 'busy'
    elif status == "available":
        green()  # Green for 'available'
    else:
        turnOff()  # Turn off if status is unknown

# Main loop to check the status and control LEDs
while True:
    user_status = get_user_status()
    if user_status:
        print(f"User status: {user_status}")
        set_led_color_by_status(user_status)
    else:
        print("Failed to retrieve user status. Turning off LEDs.")
        turnOff()
    
    sleep(5)  # Wait for 5 seconds before checking again
