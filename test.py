#[1] "Load data from php file into python," Stack Overflow. [Online]. Available: https://stackoverflow.com/questions/69581729/load-data-from-php-file-into-python. [Accessed: 08-Oct-2024].
#[2] "Customizing Your Tkinter App's Windows," Python GUIs. [Online]. Available: https://www.pythonguis.com/tutorials/customized-windows-tkinter/. [Accessed: 09-Oct-2024].
#[3] "How to delete and recreate a canvas? (Tkinter / Canvas)," Stack Overflow. [Online]. Available: https://stackoverflow.com/questions/63251775/how-to-delete-and-recreate-a-canvas-tkinter-canvas. [Accessed: 10-Mar-2024].
#[4] "datetime — Basic date and time types," Python Documentation. [Online]. Available: https://docs.python.org/3/library/datetime.html. [Accessed: 11-Oct-2024].
#[5] "When to use raise_for_status vs status_code testing," Stack Overflow. [Online]. Available: https://stackoverflow.com/questions/61463224/when-to-use-raise-for-status-vs-status-code-testing. [Accessed: 11-Oct-2024].
#[6] "Tkinter - how to resize frame," Stack Overflow. [Online]. Available: https://stackoverflow.com/questions/68270730/tkinter-how-to-resize-frame. [Accessed: 11-Oct-2024].
#[7] "Programmatically generate video or animated GIF in Python?" Stack Overflow. [Online]. Available: https://stackoverflow.com/questions/753190/programmatically-generate-video-or-animated-gif-in-python. [Accessed: 11-Oct-2024].

import tkinter as tk
from round_button import CanvasButton
from PIL import Image, ImageTk, ImageSequence
from datetime import datetime
from AddNotePopup import AddNotePopup 
from ViewNotePopup import ViewNotePopup
from Upcoming_schedule import ViewSchedulePopup
from utils import center_window_parent
import requests  
from io import BytesIO  
from datetime import datetime, timedelta
from constant import *
import time
import RPi.GPIO as GPIO
import threading

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
        
        # Remove window decorations
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
        
        # Bind the Escape key to quit the application
        self.root.bind('<Escape>', self.quit_app)

        # Bind the closing event
        self.root.protocol("WM_DELETE_WINDOW", self.quit_app)

        self.current_event = None
        self.update_current_event()

        # GPIO setup for LEDs
        self.LED_RED = 12    # GPIO pin for Red LED
        self.LED_YELLOW = 16  # GPIO pin for Yellow LED
        self.LED_GREEN = 26  # GPIO pin for Green LED

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.LED_RED, GPIO.OUT)
        GPIO.setup(self.LED_YELLOW, GPIO.OUT)
        GPIO.setup(self.LED_GREEN, GPIO.OUT)

        # Initialize LEDs (Turn them off initially)
        GPIO.output(self.LED_RED, GPIO.LOW)
        GPIO.output(self.LED_YELLOW, GPIO.LOW)
        GPIO.output(self.LED_GREEN, GPIO.LOW)

        # Set GPIO pins for ultrasonic sensor
        self.TRIG = 17
        self.ECHO = 27

        # GPIO setup for ultrasonic sensor
        GPIO.setup(self.TRIG, GPIO.OUT)
        GPIO.setup(self.ECHO, GPIO.IN)

        self.is_gif_playing = False  # Initialize GIF playing state
        self.gif_animation_id = None  # Initialize GIF animation ID

        # Start the distance monitoring thread
        threading.Thread(target=self.distance_monitor, daemon=True).start()

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
            self.user_events = response.json()  # Store all events
            
            print("Fetched user events:")
            for event in self.user_events:
                print(f"Event: {event['event_name']}, Start: {event['start_time']}, End: {event['end_time']}, Story: {event['story']}")
            
            # The story will be set in the update_current_event method
            self.story = None

        except requests.RequestException as e:
            print(f"Failed to fetch user events: {str(e)}")
        except ValueError as e:
            print(f"Invalid JSON response for user events: {str(e)}")
        except Exception as e:
            print(f"An unexpected error occurred while fetching user events: {str(e)}")

        if self.story:
            print(f"Story set: {self.story}")
        else:
            print("No story found in user events")
        
        if self.user_status:
            print(f"User status: {self.user_status}")
            # Update LEDs based on the user status
            self.change_led_based_on_status(self.user_status)
        else:
            print("No status found in user events")
            self.change_led_based_on_status("")

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

        try:
            # Update current event before fetching image
            self.update_current_event()
            
            # if there is story and the sensor sense someone use the story
            if self.story and self.current_event and self.measure_distance() <= 45:
                print(f"Using story URL: {self.story}")
                self.load_and_display_image(self.story)
            # or use the photo with attendee
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
                            photo_url = photo_data[0]['filename']
                            time_difference = end_time - current_time
                            print(f"Event ID: {event_id}, Start Time: {start_time}, End Time: {end_time}, Time Difference: {time_difference}, Photo URL: {photo_url}")
                            
                            # Choose the future event with the smallest time difference
                            if time_difference > timedelta() and time_difference < smallest_time_difference:
                                smallest_time_difference = time_difference
                                event_photo = photo_url
                                chosen_event = event
                        else:
                            print(f"Event ID: {event_id}, Start Time: {start_time}, End Time: {end_time}, Photo URL: Not available")

                    except requests.RequestException as e:
                        print(f"Event ID: {event_id}, Start Time: {start_time}, End Time: {end_time}, Error: Failed to fetch photo - {str(e)}")
                    except ValueError as e:
                        print(f"Event ID: {event_id}, Start Time: {start_time}, End Time: {end_time}, Error: Invalid JSON response - {str(e)}")
                    except Exception as e:
                        print(f"Event ID: {event_id}, Start Time: {start_time}, End Time: {end_time}, Error: Unexpected error - {str(e)}")

                if event_photo:
                    print("\nChosen photo:")
                    print(f"Event ID: {chosen_event['event_id']}")
                    print(f"Event Name: {chosen_event['event_name']}")
                    print(f"Start Time: {chosen_event['start_time']}")
                    print(f"End Time: {chosen_event['end_time']}")
                    print(f"Time Difference: {smallest_time_difference}")
                    print(f"Photo URL: {event_photo}")
                    self.load_and_display_image(event_photo)
                # if no photo together with the attendee, use the solo photo of the user
                else:
                    print("\nNo suitable future event photo found. Using fallback URL.")
                    try:
                        response = requests.get(fallback_url)
                        response.raise_for_status()
                        fallback_data = response.json()
                        if fallback_data and isinstance(fallback_data, list) and len(fallback_data) > 0:
                            fallback_photo = fallback_data[0]['filename']
                            print(f"Fallback Photo URL: {fallback_photo}")
                            self.load_and_display_image(fallback_photo)
                        else:
                            print("No fallback photo available")
                            self.display_error("No photo available")
                    except requests.RequestException as e:
                        self.display_error(f"Failed to fetch fallback photo: {str(e)}")
                    except ValueError as e:
                        self.display_error(f"Invalid JSON response for fallback photo: {str(e)}")
                    except Exception as e:
                        self.display_error(f"An unexpected error occurred while fetching fallback photo: {str(e)}")

        except requests.RequestException as e:
            self.display_error(f"Failed to fetch user events: {str(e)}")
        except ValueError as e:
            self.display_error(f"Invalid JSON response for user events: {str(e)}")
        except Exception as e:
            self.display_error(f"An unexpected error occurred while fetching user events: {str(e)}")

    def load_and_display_image(self, image_file_name):
        """
        Load and display an image from a given file name.
        Supports both static images and animated GIFs.

        Args:
            image_file_name (str): The file name of the image to be displayed.
        """
        image_url = BASE_URL + image_file_name  
        try:
            response = requests.get(image_url)
            response.raise_for_status()
            image_data = BytesIO(response.content)
            image = Image.open(image_data)

            if image.format == 'GIF' and image.is_animated:
                self.animate_gif(image)
            else:
                # Handle static images as before
                image = image.resize((SCREEN_WIDTH, SCREEN_HEIGHT), Image.LANCZOS)
                bg_image = ImageTk.PhotoImage(image)
                self.canvas.create_image(0, 0, anchor='nw', image=bg_image)
                self.canvas.bg_image = bg_image

            # Add buttons after the image is loaded
            self.add_buttons()
        except Exception as e:
            self.display_error(f"Error loading image: {str(e)}")

    def update_current_event(self):
        """Update the current_event based on the current time and event times."""
        current_time = datetime.now()
        
        print("\nAll events:")
        for event in self.user_events:
            start_time = datetime.strptime(event['start_time'], "%Y-%m-%d %H:%M:%S")
            end_time = datetime.strptime(event['end_time'], "%Y-%m-%d %H:%M:%S")
            event_id = event['event_id']
            event_url = f"https://deco3801-foundjesse.uqcloud.net/restapi/photo_frame_photos.php?event={event_id}"
            
            print(f"Event: {event['event_name']}")
            print(f"  Start: {start_time}")
            print(f"  End: {end_time}")
            print(f"  URL: {event_url}")
            print(f"  Story: {event['story']}")
            
            if start_time <= current_time <= end_time:
                self.current_event = event
                self.story = event['story']  # Set the story from the current event
                print("  ** This is the current event **")
            print()

        if self.current_event:
            print(f"\nCurrent event: {self.current_event['event_name']}")
            print(f"Current story: {self.story}")
        else:
            print("\nNo current event")
            self.current_event = None
            self.story = None

        print(f"Final story value: {self.story}")

    def animate_gif(self, image):
        """
        Animate a GIF image on the canvas.

        Args:
            image (PIL.Image): The GIF image to animate.
        """
        frames = []
        try:
            for frame in ImageSequence.Iterator(image):
                frame = frame.copy()
                frame = frame.resize((SCREEN_WIDTH, SCREEN_HEIGHT), Image.LANCZOS)
                frames.append(ImageTk.PhotoImage(frame))
        except Exception as e:
            print(f"Error processing GIF frames: {str(e)}")
            return

        def update_frame(frame_num=0):
            if frame_num < len(frames) and self.is_gif_playing:
                self.canvas.delete("all")  # Clear previous frame
                self.canvas.create_image(0, 0, anchor='nw', image=frames[frame_num])
                next_frame = (frame_num + 1) % len(frames)
                self.gif_animation_id = self.root.after(100, update_frame, next_frame)  # Adjust delay as needed
            self.add_buttons()  # Ensure buttons are always on top

        update_frame(0)

    def display_error(self, message):
        """
        Display an error message on the canvas.

        Args:
            message (str): The error message to be displayed.
        """
        print(message)
        error_label = tk.Label(self.root, text=message, bg="white")
        error_label.place(x=0, y=0, relwidth=1, relheight=1)

    def add_buttons(self):
        """Add interactive buttons to the canvas."""
        # Add add-note icon using CanvasButton
        self.add_note_button = CanvasButton(self.canvas, NOTE_ICON_X, NOTE_ICON_Y, 
                     WRITE_NOTE_ICON_IMAGE_PATH, self.add_note_popup.add_note)

        self.view_schedule_button = CanvasButton(self.canvas, CALENDAR_ICON_X, CALENDAR_ICON_Y, 
                     UPCOMING_SCHEDULE_ICON, self.view_schedule_popup.show_schedules)

        # Create the list icon button if self.saved_notes is not empty
        if self.saved_notes:
            self.view_note_button = CanvasButton(self.canvas, LIST_ICON_X, LIST_ICON_Y, 
                         LIST_ICON, self.view_note_popup.show_notes)

    def update_view_note_button(self):
        """Creates the list button if it doesn't exist and there are saved notes."""
        if self.saved_notes and not self.view_note_button:
            print("Creating the list button")
            self.view_note_button = CanvasButton(
                self.canvas,
                LIST_ICON_X,
                LIST_ICON_Y,
                LIST_ICON,
                self.view_note_popup.show_notes
            )

    def quit_app(self, event=None):
        """Quit the application and close all child windows."""
        # Close all child windows
        for child in self.child_windows:
            if child.winfo_exists():
                child.destroy()
        # Close the main window
        self.root.quit()

        # Cleanup GPIO pins
        GPIO.cleanup()

    def register_child_window(self, window):
        """Register a child window."""
        self.child_windows.append(window)

    def unregister_child_window(self, window):
        """Unregister a child window."""
        self.child_windows = [w for w in self.child_windows if w != window and w.winfo_exists()]

    def measure_distance(self):
        """Measure the distance using the ultrasonic sensor."""
        GPIO.output(self.TRIG, False)
        time.sleep(0.2)

        GPIO.output(self.TRIG, True)
        time.sleep(0.00001)
        GPIO.output(self.TRIG, False)

        pulse_start = time.time()
        while GPIO.input(self.ECHO) == 0:
            pulse_start = time.time()

        pulse_end = time.time()
        while GPIO.input(self.ECHO) == 1:
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
                
                # Update icon opacity
                if distance <= 45:
                    self.update_icon_opacity(1.0)  # Fully opaque

                    # If GIF is not playing, start it
                    if not self.is_gif_playing:
                        print("Object detected within 45 cm - Starting GIF")
                        self.is_gif_playing = True
                        self.animate_gif(self.gif_image)  # Start playing the GIF

                else:
                    self.update_icon_opacity(0.0)  # Fully transparent

                    # If GIF is playing, stop it
                    if self.is_gif_playing:
                        print("No object within 45 cm - Pausing GIF")
                        self.is_gif_playing = False
                        self.root.after_cancel(self.gif_animation_id)  # Stop the GIF animation

            time.sleep(0.3)

    def update_icon_opacity(self, opacity):
        """Update the opacity of the icons on the canvas."""
        if self.add_note_button:
            self.add_note_button.set_opacity(opacity)  
        if self.view_schedule_button:
            self.view_schedule_button.set_opacity(opacity)  
        if self.view_note_button:
            self.view_note_button.set_opacity(opacity)

    def change_led_based_on_status(self, status):
        """Change LED color based on the user's status."""
        # Turn off all LEDs first
        GPIO.output(self.LED_RED, GPIO.LOW)
        GPIO.output(self.LED_YELLOW, GPIO.LOW)
        GPIO.output(self.LED_GREEN, GPIO.LOW)

        if status == "Chilling":
            print("Status: Chilling - Turning on Green LED")
            GPIO.output(self.LED_GREEN, GPIO.HIGH)  # Turn on Green LED
        elif status == "Occupied":
            print("Status: Occupied - Turning on Yellow LED")
            GPIO.output(self.LED_YELLOW, GPIO.HIGH)  # Turn on Yellow LED
        elif status == "Do not disturb":
            print("Status: Do not disturb - Turning on Red LED")
            GPIO.output(self.LED_RED, GPIO.HIGH)  # Turn on Red LED



if __name__ == "__main__":
    root = tk.Tk()
    root.overrideredirect(True)  # Remove window decorations
    root.geometry(f"{SCREEN_WIDTH}x{SCREEN_HEIGHT}+0+0")  # Set full screen size
    app = PhotoFrameApp(root)
    root.mainloop()
