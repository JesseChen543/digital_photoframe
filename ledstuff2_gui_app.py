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

# Function to turn off the LED
def turn_off():
    GPIO.output(redPin, GPIO.HIGH)
    GPIO.output(greenPin, GPIO.HIGH)
    GPIO.output(bluePin, GPIO.HIGH)

# Function to turn on red
def red():
    GPIO.output(redPin, GPIO.LOW)    # Red ON
    GPIO.output(greenPin, GPIO.HIGH)  # Green OFF
    GPIO.output(bluePin, GPIO.HIGH)   # Blue OFF

# Function to turn on green
def green():
    GPIO.output(redPin, GPIO.HIGH)    # Red OFF
    GPIO.output(greenPin, GPIO.LOW)   # Green ON
    GPIO.output(bluePin, GPIO.HIGH)   # Blue OFF

# Function to turn on yellow
def yellow():
    GPIO.output(redPin, GPIO.LOW)     # Red ON
    GPIO.output(greenPin, GPIO.LOW)   # Green ON
    GPIO.output(bluePin, GPIO.HIGH)   # Blue OFF

# Function to get the user's status from the REST API
def get_user_status():
    url = 'https://deco3801-foundjesse.uqcloud.net/restapi/api.php?user_id=1'  # Replace with your API endpoint
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json().get('status', None)  # Assuming the status is returned in the JSON response
        else:
            print(f"Error: Received status code {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error connecting to API: {e}")
        return None

# Map statuses to LED colors
def set_led_color_by_status(status):
    if status == "Chilling":
        green()  # Green for 'Chilling'
    elif status == "Occupied":
        yellow()  # Yellow for 'Occupied'
    elif status == "Do not disturb":
        red()  # Red for 'Do not disturb'
    else:
        print(f"Unknown status: {status}. Turning off LEDs.")
        turn_off()  # Turn off if status is unknown

# Main loop to check the status and control LEDs
try:
    while True:
        user_status = get_user_status()
        if user_status:
            print(f"User status: {user_status}")
            set_led_color_by_status(user_status)
        else:
            print("Failed to retrieve user status. Turning off LEDs.")
            turn_off()
        
        sleep(5)  # Wait for 5 seconds before checking again
except KeyboardInterrupt:
    print("Exiting program...")
finally:
    turn_off()
    GPIO.cleanup()  # Reset all GPIO pins
