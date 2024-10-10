import RPi.GPIO as GPIO
import time
import threading

# GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)

# Set GPIO pins
TRIG = 17  # GPIO pin 17 for TRIG
ECHO = 27  # GPIO pin 27 for ECHO

# Set the TRIG and ECHO pins as output and input
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

def measure_distance():
    GPIO.output(TRIG, False)
    time.sleep(2)  # Initial delay to stabilize the sensor

    GPIO.output(TRIG, True)
    time.sleep(0.00001)  # Short pulse
    GPIO.output(TRIG, False)

    pulse_start = time.time()
    
    # Wait for the ECHO pin to go high
    while GPIO.input(ECHO) == 0:
        if (time.time() - pulse_start) > 0.05:  # Timeout of 50 ms
            print("Error: Timeout waiting for ECHO to go high")
            return None

    pulse_end = time.time()
    
    # Wait for the ECHO pin to go low
    while GPIO.input(ECHO) == 1:
        if (time.time() - pulse_end) > 0.05:  # Timeout of 50 ms
            print("Error: Timeout waiting for ECHO to go low")
            return None

    # Calculate the duration of the pulse and the distance
    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17150
    distance = round(distance, 2)

    return distance

# Function to continuously measure distance
def measure_loop():
    while True:
        distance = measure_distance()
        if distance is not None and distance >= 0:
            print(f"Distance: {distance} cm")
        time.sleep(0.5)  # Reduced sleep for more frequent updates

# Start the measurement loop in a separate thread
measurement_thread = threading.Thread(target=measure_loop)
measurement_thread.daemon = True  # Daemon thread will exit when the main program exits
measurement_thread.start()

try:
    while True:
        time.sleep(1)  # Main thread can perform other tasks or just sleep

except KeyboardInterrupt:
    print("Measurement stopped by user")
    GPIO.cleanup()
