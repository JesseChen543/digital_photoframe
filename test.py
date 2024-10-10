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
from datetime import datetime, timedelta
import RPi.GPIO as GPIO  # Import the GPIO library
import time  # Import time for delays
from constant import *

class PhotoFrameApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Display with Clickable Icon")

        # Initialize list to keep track of child windows
        self.child_windows = []

        # Initialize frame_id (assuming it's always 1 for now)
        self.frame_id = 1

        # Get user_id and other user info from database based on frame_id
        self.user_id = self.get_user_id(self.frame_id)
        if self.user_id is None:
            self.display_error("Failed to fetch user information")
            return

        # Initialize saved inputs
        self.saved_notes = []

        # Initialize buttons 
        self.view_note_button = None  
        self.view_schedule_button = None
        self.add_note_button = None

        self.current_date = datetime.now().strftime("%d/%m/%Y")

        # Initialize popup windows
        self.add_note_popup = AddNotePopup(self.root, self)
        self.view_note_popup = ViewNotePopup(self.root, self)
        self.view_schedule_popup = ViewSchedulePopup(self.root, self, self.user_id)
        
        # Create canvas
        self.canvas = tk.Canvas(self.root, width=SCREEN_WIDTH, height=SCREEN_HEIGHT, bd=0, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        # Fetch and display the image
        self.fetch_and_display_image()

        # Setup ultrasonic sensor
        self.setup_ultrasonic_sensor()

        # Start distance monitoring
        self.monitor_distance()

        # Center the window on the screen
        center_window_parent(self.root, SCREEN_WIDTH, SCREEN_HEIGHT)
        
        # Bind the Escape key to quit the application
        self.root.bind('<Escape>', self.quit_app)

        # Bind the closing event
        self.root.protocol("WM_DELETE_WINDOW", self.quit_app)

    def setup_ultrasonic_sensor(self):
        """Set up the ultrasonic sensor on GPIO pins."""
        self.TRIG = 17  # Define the trigger pin
        self.ECHO = 27  # Define the echo pin
        
        GPIO.setmode(GPIO.BCM)  # Use BCM pin numbering
        GPIO.setup(self.TRIG, GPIO.OUT)  # Set the trigger pin as output
        GPIO.setup(self.ECHO, GPIO.IN)    # Set the echo pin as input

    def get_user_id(self, frame_id):
        # Fetch user ID from database based on frame_id
        # Placeholder for database access logic
        return 1  # Example user ID, replace with actual logic

    def fetch_and_display_image(self):
        # Example URL to fetch an image
        image_url = "http://example.com/image.jpg"  # Replace with your image URL
        self.load_and_display_image(image_url)

    def load_and_display_image(self, image_url):
        try:
            response = requests.get(image_url)
            image_data = Image.open(BytesIO(response.content))

            # Resize image to fit the canvas
            image_data = image_data.resize((SCREEN_WIDTH, SCREEN_HEIGHT), Image.ANTIALIAS)
            self.image = ImageTk.PhotoImage(image_data)

            self.canvas.create_image(0, 0, anchor=tk.NW, image=self.image)
            self.add_buttons()
        except Exception as e:
            self.display_error(f"Failed to load image: {e}")

    def display_error(self, message):
        error_label = tk.Label(self.root, text=message, fg="red")
        error_label.pack()

    def add_buttons(self):
        # Add buttons to the canvas (implement your button logic here)
        # Example:
        self.add_note_button = CanvasButton(self.canvas, text="Add Note", command=self.add_note, x=100, y=100)
        self.view_note_button = CanvasButton(self.canvas, text="View Notes", command=self.view_notes, x=100, y=150)
        self.view_schedule_button = CanvasButton(self.canvas, text="View Schedule", command=self.view_schedule, x=100, y=200)

    def add_note(self):
        self.add_note_popup.open()

    def view_notes(self):
        self.view_note_popup.open()

    def view_schedule(self):
        self.view_schedule_popup.open()

    def quit_app(self, event=None):
        # Close all child windows
        for child in self.child_windows:
            if child.winfo_exists():
                child.destroy()
        # Close the main window
        GPIO.cleanup()  # Clean up GPIO pins
        self.root.quit()

    def monitor_distance(self):
        """Continuously monitor the distance using the ultrasonic sensor."""
        def measure_distance():
            while True:
                GPIO.output(self.TRIG, True)  # Send a 10us pulse to the trigger pin
                time.sleep(0.00001)  # Wait for 10 microseconds
                GPIO.output(self.TRIG, False)  # Stop sending the pulse

                start_time = time.time()
                stop_time = time.time()

                while GPIO.input(self.ECHO) == 0:  # Wait for the echo to start
                    start_time = time.time()

                while GPIO.input(self.ECHO) == 1:  # Wait for the echo to end
                    stop_time = time.time()

                # Calculate the distance in cm
                elapsed_time = stop_time - start_time
                distance = (elapsed_time * 34300) / 2  # Speed of sound = 34300 cm/s

                # Update icon visibility based on distance
                if distance < 45:
                    self.set_icon_opacity(1)  # Fully opaque
                else:
                    self.set_icon_opacity(0)  # Fully transparent

                time.sleep(1)  # Measure every second

        # Start the distance measurement in a new thread
        import threading
        thread = threading.Thread(target=measure_distance)
        thread.daemon = True  # Daemonize thread
        thread.start()

    def set_icon_opacity(self, opacity):
        """Set the icon's opacity based on distance."""
        state = 'normal' if opacity == 1 else 'hidden'
        # Update each button's icon based on the opacity
        if self.add_note_button:
            self.canvas.itemconfig(self.add_note_button.button_id, state=state)
        if self.view_schedule_button:
            self.canvas.itemconfig(self.view_schedule_button.button_id, state=state)
        if self.view_note_button:
            self.canvas.itemconfig(self.view_note_button.button_id, state=state)

    def register_child_window(self, window):
        self.child_windows.append(window)

    def unregister_child_window(self, window):
        self.child_windows.remove(window)

if __name__ == "__main__":
    root = tk.Tk()
    app = PhotoFrameApp(root)
    root.mainloop()
