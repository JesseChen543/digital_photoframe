import RPi.GPIO as GPIO
import time
import tkinter as tk
from round_button import CanvasButton
from PIL import Image, ImageTk, ImageSequence
from datetime import datetime, timedelta
from AddNotePopup import AddNotePopup
from ViewNotePopup import ViewNotePopup
from Upcoming_schedule import ViewSchedulePopup
from utils import center_window_parent
import requests  
from io import BytesIO  
import threading
from constant import * 

# GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)

# Set GPIO pins
TRIG = 17  # GPIO pin 17 for TRIG
ECHO = 27  # GPIO pin 27 for ECHO

# Set the TRIG and ECHO pins as output and input
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

class PhotoFrameApp:
    """
    A class representing the main photo frame application.
    
    This class manages the display of images, user information, and interactive buttons
    for adding notes, viewing schedules, and displaying saved notes.
    """

    def __init__(self, root):
        """
        Initialize the PhotoFrameApp.

        Args:
            root (tk.Tk): The root window of the application.
        """
        self.root = root

        # Remove the title bar
        self.root.overrideredirect(True)

        # Set full screen size
        self.root.geometry(f"{SCREEN_WIDTH}x{SCREEN_HEIGHT}+0+0")

        # Initialize list to keep track of child windows
        self.child_windows = []

        # Initialize frame_id (assuming it's always 1 for now)
        self.frame_id = 1

        # Get user_id and other user info from database based on frame_id
        self.user_id = self.get_user_id(self.frame_id)
        if self.user_id is None:
            # Handle the case where user_id couldn't be fetched
            self.display_error("Failed to fetch user information")
            return

        # Initialize story property
        self.story = None
        
        # Fetch user events and set the story
        self.fetch_user_events()

        # Initialize saved inputs
        self.saved_notes = []

        # Initialize buttons 
        self.view_note_button = None  
        self.view_schedule_button = None
        self.add_note_button = None
        self.view_schedule_button = None
        self.view_note_button = None

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

        # Initialize a flag to track GIF playback state
        self.gif_playing = False
        
        # Bind the Escape key to quit the application
        self.root.bind('<Escape>', self.quit_app)

        # Bind the closing event
        self.root.protocol("WM_DELETE_WINDOW", self.quit_app)

        # Start the distance measuring thread
        self.distance_thread = threading.Thread(target=self.distance_monitor)
        self.distance_thread.daemon = True  # Ensure the thread exits when the main program exits
        self.distance_thread.start()

    def measure_distance(self):
        """Measure the distance using the ultrasonic sensor."""
        GPIO.output(TRIG, False)
        time.sleep(2)

        GPIO.output(TRIG, True)
        time.sleep(0.00001)
        GPIO.output(TRIG, False)

        pulse_start = time.time()
        while GPIO.input(ECHO) == 0:
            pulse_start = time.time()

        pulse_end = time.time()
        while GPIO.input(ECHO) == 1:
            pulse_end = time.time()

        pulse_duration = pulse_end - pulse_start
        distance = pulse_duration * 17150
        return round(distance, 2)

    def distance_monitor(self):
        """Continuously monitor the distance and update icon opacity."""
        while True:
            distance = self.measure_distance()
            if distance is not None:
                print(f"Distance: {distance} cm")
                # Update icon opacity based on distance
                if distance <= 45:
                    self.update_icon_opacity(1.0)  # Fully opaque
                    if self.story and not self.gif_playing:
                        print(f"Using story URL: {self.story}")
                        self.start_gif_playback()  # Start GIF playback
                else:
                    self.update_icon_opacity(0.0)  # Fully transparent
                    if self.gif_playing:
                        self.stop_gif_playback()  # Stop GIF playback
            time.sleep(0.3)  # Adjust the sleep time as needed

    def update_icon_opacity(self, opacity):
        """Update the opacity of the icons on the canvas."""
        # You can adjust the opacity by changing the alpha channel of the images.
        # Note: Actual implementation will depend on how you have defined and handled the icons.
        # Here, we'll assume you can change their opacity based on some logic.
        if self.add_note_button:
            self.add_note_button.set_opacity(opacity)  # Placeholder function
        if self.view_schedule_button:
            self.view_schedule_button.set_opacity(opacity)  # Placeholder function
        if self.view_note_button:
            self.view_note_button.set_opacity(opacity)  # Placeholder function

    def get_user_id(self, frame_id):
        """
        Fetch user information from the database based on frame_id.
        
        Args:
            frame_id (int): The ID of the frame.
        
        Returns:
            int: The user_id associated with the frame.
            None: If there's an error or no user found.
        """
        api_url = f"https://deco3801-foundjesse.uqcloud.net/restapi/frame_user.php?frame_id={frame_id}"
        
        try:
            response = requests.get(api_url)
            response.raise_for_status()  # Raise an exception for bad status codes
            data = response.json()
            
            if data and isinstance(data, list) and len(data) > 0:
                user_info = data[0]
                self.user_id = user_info['user_id']
                self.user_name = user_info['first_name']
                self.user_status = user_info['status']
                self.user_icon = user_info['icon']
                return self.user_id
            else:
                print(f"No user found for frame_id: {frame_id}")
                return None
        except requests.RequestException as e:
            print(f"Failed to fetch user data: {str(e)}")
            return None
        except ValueError as e:
            print(f"Invalid JSON response: {str(e)}")
            return None

    def fetch_user_events(self):
        """Fetch user events and set the story property."""
        special_user_url = f"https://deco3801-foundjesse.uqcloud.net/restapi/special_user.php?special_user={self.user_id}"
        
        try:
            response = requests.get(special_user_url)
            response.raise_for_status()
            user_events = response.json()
            # Find the first event with a story
            for event in user_events:
                if event['story']:
                    self.story = event['story']
                    break
            if self.story:
                print(f"Story set: {self.story}")
            else:
                print("No story found in user events")
        except requests.RequestException as e:
            print(f"Failed to fetch user events: {str(e)}")
        except ValueError as e:
            print(f"Invalid JSON response for user events: {str(e)}")
        except Exception as e:
            print(f"An unexpected error occurred while fetching user events: {str(e)}")

    def fetch_and_display_image(self):
        """
        Fetch and display an image for the photo frame.
        
        This method attempts to fetch an image from a future event. If no suitable
        future event image is found, it falls back to a default user image.
        """
        base_url = "https://deco3801-foundjesse.uqcloud.net/restapi/photo_frame_photos.php?event="
        special_user_url = f"https://deco3801-foundjesse.uqcloud.net/restapi/special_user.php?special_user={self.user_id}"
        fallback_url = f"https://deco3801-foundjesse.uqcloud.net/restapi/api.php?user_id={self.user_id}"
        event_photo = None
        chosen_event = None
        current_time = datetime.now()
        smallest_time_difference = timedelta.max  # Initialize with maximum possible timedelta

        print(f"Current time: {current_time}")

        try:
            # Use the story URL if available, otherwise proceed with existing logic
            if self.story:
                print(f"Using story URL: {self.story}")
                self.load_and_display_image(self.story)
            else:
                # Fetch user's events
                response = requests.get(special_user_url)
                response.raise_for_status()
                user_events = response.json()

                print("All events:")
                for event in user_events:
                    event_id = event['event_id']
                    start_time = datetime.strptime(event['start_time'], "%Y-%m-%d %H:%M:%S")
                    end_time = datetime.strptime(event['end_time'], "%Y-%m-%d %H:%M:%S")
                    api_url = f"{base_url}{event_id}"
                    try:
                        response = requests.get(api_url)
                        response.raise_for_status()
                        photo_data = response.json()
                        if photo_data and isinstance(photo_data, list) and len(photo_data) > 0:
                            event_photo = photo_data[0]['url']
                            print(f"Event photo fetched: {event_photo}")
                    except requests.RequestException as e:
                        print(f"Error fetching photo for event {event_id}: {str(e)}")
                    except ValueError as e:
                        print(f"Invalid JSON response for event {event_id}: {str(e)}")

                    time_difference = start_time - current_time
                    if time_difference >= timedelta(seconds=0) and time_difference < smallest_time_difference:
                        smallest_time_difference = time_difference
                        chosen_event = event
                        print(f"Chosen event: {chosen_event}")

                # Fallback to user image if no suitable event image is found
                if event_photo is None:
                    response = requests.get(fallback_url)
                    response.raise_for_status()
                    user_data = response.json()
                    event_photo = user_data[0]['url'] if user_data and isinstance(user_data, list) and len(user_data) > 0 else None

                if event_photo:
                    self.load_and_display_image(event_photo)
                else:
                    print("No event photo or user image found.")

        except requests.RequestException as e:
            print(f"Failed to fetch events: {str(e)}")
        except ValueError as e:
            print(f"Invalid JSON response for events: {str(e)}")
        except Exception as e:
            print(f"An unexpected error occurred: {str(e)}")

    def load_and_display_image(self, image_url):
        """Load an image from a URL and display it on the canvas."""
        try:
            response = requests.get(image_url)
            response.raise_for_status()
            image_data = Image.open(BytesIO(response.content))

            if image_data.format == 'GIF':
                self.display_gif(image_data)
            else:
                self.display_image(image_data)
        except requests.RequestException as e:
            print(f"Failed to load image from URL: {str(e)}")
        except IOError as e:
            print(f"Error loading image: {str(e)}")
        except Exception as e:
            print(f"An unexpected error occurred while displaying the image: {str(e)}")

    def display_gif(self, gif_image):
        """Display a GIF image on the canvas."""
        frames = [ImageTk.PhotoImage(frame.copy()) for frame in ImageSequence.Iterator(gif_image)]
        self.gif_frames = frames
        self.current_frame = 0
        self.gif_playing = True
        self.play_gif()

    def play_gif(self):
        """Play the GIF image by cycling through its frames."""
        if self.gif_frames:
            frame = self.gif_frames[self.current_frame]
            self.canvas.create_image(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, image=frame)
            self.current_frame = (self.current_frame + 1) % len(self.gif_frames)
            self.root.after(100, self.play_gif)

    def stop_gif_playback(self):
        """Stop the GIF playback."""
        self.gif_playing = False
        self.canvas.delete("all")

    def display_image(self, image):
        """Display a static image on the canvas."""
        self.tk_image = ImageTk.PhotoImage(image)
        self.canvas.create_image(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, image=self.tk_image)

    def quit_app(self, event=None):
        """Quit the application and cleanup GPIO settings."""
        GPIO.cleanup()
        self.root.destroy()

# Entry point for the application
if __name__ == "__main__":
    root = tk.Tk()
    root.overrideredirect(True)  # Remove window decorations
    root.geometry(f"{SCREEN_WIDTH}x{SCREEN_HEIGHT}+0+0")  # Set full screen size
    app = PhotoFrameApp(root)
    root.mainloop()
