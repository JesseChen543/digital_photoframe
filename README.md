# Insync Photoframe

Insync Photoframe is a python-based digital photoframe application that is designed for a Raspberry Pi using Tkinter GUI framework. The application displays event-based images or GIFs based on detecting user proximity using an ultrasonic sensor and integrates RGB LEDs to show the user's status

# Requirements
 - **Hardware:**
   - Raspberry Pi with GPIO support
   - RGB LED
   - Ultrasonic sensor (TRIG on GPIO 17, ECHO on GPIO 27)

 - **Software:**
   - Python 3.x
   - Required Python libraries:
     - `RPi.GPIO` (GPIO handling)
     - `Pillow` (image and GIF handling)
     - `Requests` (API calls)
    

 # Installation and Setup
 
1. **Install Dependencies:** Ensure Python is installed, then install the required Python libraries using `pip`:
