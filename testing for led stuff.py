import RPi.GPIO as GPIO
from flask import Flask, request, jsonify

# GPIO setup
GPIO.setmode(GPIO.BCM)

# Define pins for each LED color
LED_PINS = {
    "occupied": 17,   # Orange/Yellow LED
    "do not disturb": 27,    # Red LED
    "chilling": 22,       # Green LED
}

# Set all LED pins to output
for pin in LED_PINS.values():
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)  # Turn off all LEDs initially

# Flask app setup
app = Flask(__name__)

@app.route('/update_status', methods=['POST'])
def update_status():
    data = request.json
    activity = data.get('activity')

    # Turn off all LEDs first
    for pin in LED_PINS.values():
        GPIO.output(pin, GPIO.LOW)

    # Turn on the corresponding LED for the activity
    if activity in LED_PINS:
        GPIO.output(LED_PINS[activity], GPIO.HIGH)
        return jsonify({"message": f"{activity} LED turned ON"}), 200
    else:
        return jsonify({"error": "Invalid activity"}), 400

if __name__ == '__main__':
    try:
        app.run(host='0.0.0.0', port=5000)
    except KeyboardInterrupt:
        GPIO.cleanup()
