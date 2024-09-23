import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
TRIG = 23
ECHO = 24
print("Distance to nearest object in progress")
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)
GPIO.output(TRIG, False)
print("Waiting for sensor to settle")
time.sleep(2)

# Sending a pulse
GPIO.output(TRIG, True)
time.sleep(0.00001)
GPIO.output(TRIG, False)

# start time when the pulse is sent
while GPIO.input(ECHO) == 0:
    pulse_start = time.time()  # Define pulse_start here

# end time when the echo is received
while GPIO.input(ECHO) == 1:
    pulse_end = time.time()

# Calculate the duration of the pulse
pulse_duration = pulse_end - pulse_start

# Calculate distance (speed of sound is ~34300 cm/s, divided by 2 to account for the pulse traveling to the object and back)
distance = pulse_duration * 17150
distance = round(distance, 2)

print("Distance is", distance, "cm")
