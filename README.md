# Welcome to the InSync app

This is an [Expo](https://expo.dev) project

## How to run the app

1. Install dependencies

   ```bash
   npm install
   ```

2. Start the app

   ```bash
    npx expo start
   ```
   After starting the app, **there should be a QR code in the terminal**. <br /><br />

3. Download the Expo Go app on your phone

   [Android](https://play.google.com/store/apps/details?id=host.exp.exponent&hl=en_AU&pli=1)

   [ios](https://apps.apple.com/us/app/expo-go/id982107779)<br /><br />
   
4. Scan the QR code with your phone, and open the link with the Expo app<br /><br />

**IMPORTANT**: Make sure that your device that hosts the app is connected to the same WiFi as the phone that has the Expo app.


# Insync Photoframe

Insync Photoframe is a python-based digital photoframe application that turns your Raspberry Pi into an interactive photo frame and is designed with features such as adding notes, viewing schedules, and an LED-based status indicator. It also comes with a ultrasonic sensor to interactively respond to proximity

## Prerequisites
1. #### Hardware Requirement:
      - Raspberry Pi with GPIO access
      - Ultrasonic sensor (HC-SR04)
      - RPG LEDs
      - Internet connection
2. #### Software Requirements:
      - Python 3.x
      - Required Python libraries
        ```bash
        sudo pip install RPi.GPIO Pillow requests
        ```

# Setup Instructions

### 1. Clone the Repository

To get started, you must first clone this repository to your Raspberry Pi:
```bash
git clone <https://github.com/JesseChen543/digital_photoframe.git>
cd digital_photoframe
```

### 2. Install Required Dependencies: 
Install the necessary Python libraries (RPi.GPIO, Pillow, requests)
```bash
sudo pip install Rpi.GPIO Pillow requests
```
### 3. Wiring Setup
 - Connect the ultrasonic sensor to GPIO pins 17 (TRIG) and 27 (ECHO)
 - Connect the RGB LED to GPIO pins 12 (Red), 16 (Yellow), and 26 (Green).

# Running the Application
### 1. Run the Python Script:
Execute the main script to start the photoframe application:
```bash
python3 photoframe.py
```
### 2. Functionality:
 - The app will load event-based images and change LED colours based on user status.
 - The ultrasonic sensor will trigger GIF animations when objects are detected within 45cm.

## GPIO Cleanup

To safely shut down the application and clean up the GPIO pins:
```bash
Ctrl + C
```

### Notes
 - Ensure the Raspberry Pi is properly configured with Python and internet access
 - Adjust the script if necessary to match your GPIO wiring.
