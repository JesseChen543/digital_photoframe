import RPi.GPIO as GPIO
import time

# GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)

# Set GPIO pins
TRIG = 17  # GPIO pin 17 for TRIG
ECHO = 27  # GPIO pin 27 for ECHO

# Set the TRIG and ECHO pins as output and input
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

def measure_distance():
    # Ensure the TRIG pin is low
    GPIO.output(TRIG, False)
    time.sleep(2)

    # Send a short 10µs pulse to TRIG to start the measurement
    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)

    # Wait for the ECHO pin to go high and start the timer
    while GPIO.input(ECHO) == 0:
        pulse_start = time.time()

    # Wait for the ECHO pin to go low and stop the timer
    while GPIO.input(ECHO) == 1:
        pulse_end = time.time()

    # Calculate the duration of the pulse
    pulse_duration = pulse_end - pulse_start

    # Calculate the distance (speed of sound is 34300 cm/s)
    distance = pulse_duration * 17150
    distance = round(distance, 2)

    return distance

try:
    while True:
        distance = measure_distance()
        print(f"Distance: {distance} cm")
        time.sleep(1)

except KeyboardInterrupt:
    print("Measurement stopped by user")
    GPIO.cleanup()
