import tkinter as tk
from round_button import CanvasButton
from PIL import Image, ImageTk
from datetime import datetime
from AddNotePopup import AddNotePopup
from ViewNotePopup import ViewNotePopup
from Upcoming_schedule import ViewSchedulePopup
from utils import center_window_parent
import requests
from io import BytesIO
import RPi.GPIO as GPIO  # Import RPi.GPIO for the ultrasonic sensor
import time  # Import time for sensor timing

from constant import *

# Set GPIO pins for the ultrasonic sensor
TRIG = 17
ECHO = 27

class PhotoFrameApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Display with Clickable Icon")

        # Initialize list to keep track of child windows
        self.child_windows = []

        self.user_id = 1
        self.event_id = 2
        # Initialize saved inputs
        self.saved_notes = []

        # Initialize buttons
        self.view_note_button = None
        self.view_schedule_button = None
        self.add_note_button = None

        self.current_date = datetime.now().strftime("%d/%m/%Y")

        # Initialize NotePopup
        self.add_note_popup = AddNotePopup(self.root, self)
        self.view_note_popup = ViewNotePopup(self.root, self)
        self.view_schedule_popup = ViewSchedulePopup(self.root, self, self.user_id)

        # Create canvas first
        self.canvas = tk.Canvas(self.root, width=SCREEN_WIDTH, height=SCREEN_HEIGHT, bd=0, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        # Set up GPIO for the ultrasonic sensor
        self.setup_gpio()

        # Fetch and display the image
        self.fetch_and_display_image()

        center_window_parent(self.root, SCREEN_WIDTH, SCREEN_HEIGHT)
        self.root.bind('<Escape>', self.quit_app)

        # Bind the closing event
        self.root.protocol("WM_DELETE_WINDOW", self.quit_app)

        # Start checking the sensor in a loop
        self.update_sensor_reading()

    def setup_gpio(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(TRIG, GPIO.OUT)
        GPIO.setup(ECHO, GPIO.IN)
        GPIO.output(TRIG, False)
        print("Waiting for sensor to settle")
        time.sleep(2)

    def read_distance(self):
        # Trigger the ultrasonic pulse
        GPIO.output(TRIG, True)
        time.sleep(0.00001)
        GPIO.output(TRIG, False)

        # Measure the time taken for the echo
        while GPIO.input(ECHO) == 0:
            pulse_start = time.time()

        while GPIO.input(ECHO) == 1:
            pulse_end = time.time()

        pulse_duration = pulse_end - pulse_start
        distance = pulse_duration * 17150  # Calculate distance in cm
        distance = round(distance, 2)
        return distance

    def update_sensor_reading(self):
        distance = self.read_distance()
        print(f"Distance: {distance} cm")

        # Update the GUI based on the distance
        if distance < 45:  # If object is within 45 cm
            self.canvas.itemconfig(self.canvas_image, state='normal')  # Make icon opaque
        else:
            self.canvas.itemconfig(self.canvas_image, state='hidden')  # Make icon transparent

        # Re-check the sensor reading every 500 milliseconds
        self.root.after(500, self.update_sensor_reading)

    def fetch_and_display_image(self):
        api_url = f"https://deco3801-foundjesse.uqcloud.net/restapi/photo_frame_photos.php?event={self.event_id}"
        try:
            response = requests.get(api_url)
            response.raise_for_status()
            data = response.json()

            if data and isinstance(data, list) and len(data) > 0:
                image_url = data[0]['url']
                self.load_and_display_image(image_url)
            else:
                self.display_error("No images found for this user")
        except requests.RequestException as e:
            self.display_error(f"Failed to fetch image URL: {str(e)}")
        except ValueError as e:
            self.display_error(f"Invalid JSON response: {str(e)}")

    def load_and_display_image(self, image_url):
        try:
            response = requests.get(image_url)
            response.raise_for_status()
            image_data = BytesIO(response.content)
            image = Image.open(image_data)
            image = image.resize((SCREEN_WIDTH, SCREEN_HEIGHT), Image.LANCZOS)
            bg_image = ImageTk.PhotoImage(image)

            # Create the image on the canvas and store the reference
            self.canvas_image = self.canvas.create_image(0, 0, anchor='nw', image=bg_image)
            self.canvas.bg_image = bg_image

            # Add buttons after the image is loaded
            self.add_buttons()
        except Exception as e:
            self.display_error(f"Error loading image: {str(e)}")

    def display_error(self, message):
        print(message)
        error_label = tk.Label(self.root, text=message, bg="white")
        error_label.place(x=0, y=0, relwidth=1, relheight=1)

    def add_buttons(self):
        self.add_note_button = CanvasButton(self.canvas, NOTE_ICON_X, NOTE_ICON_Y, 
                                            WRITE_NOTE_ICON_IMAGE_PATH, self.add_note_popup.add_note)
        self.view_schedule_button = CanvasButton(self.canvas, CALENDAR_ICON_X, CALENDAR_ICON_Y, 
                                                 UPCOMING_SCHEDULE_ICON, self.view_schedule_popup.show_schedules)
        if self.saved_notes:
            self.view_note_button = CanvasButton(self.canvas, LIST_ICON_X, LIST_ICON_Y, 
                                                 LIST_ICON, self.view_note_popup.show_notes)

    def quit_app(self, event=None):
        GPIO.cleanup()  # Clean up GPIO pins before exiting
        for child in self.child_windows:
            if child.winfo_exists():
                child.destroy()
        self.root.quit()

if __name__ == "__main__":
    root = tk.Tk()
    app = PhotoFrameApp(root)
    root.mainloop()
