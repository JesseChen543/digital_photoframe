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
from constant import *

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
        self.root.title("Image Display with Clickable Icon")

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

        # Center the window on the screen
        center_window_parent(self.root, SCREEN_WIDTH, SCREEN_HEIGHT)
        
        # Bind the Escape key to quit the application
        self.root.bind('<Escape>', self.quit_app)

        # Bind the closing event
        self.root.protocol("WM_DELETE_WINDOW", self.quit_app)

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
                        photo_url = photo_data[0]['url']
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
            else:
                print("\nNo suitable future event photo found. Using fallback URL.")
                try:
                    response = requests.get(fallback_url)
                    response.raise_for_status()
                    fallback_data = response.json()
                    if fallback_data and isinstance(fallback_data, list) and len(fallback_data) > 0:
                        fallback_photo = fallback_data[0]['url']
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

    def load_and_display_image(self, image_url):
        """
        Load and display an image from a given URL.

        Args:
            image_url (str): The URL of the image to be displayed.
        """
        try:
            response = requests.get(image_url)
            response.raise_for_status()
            image_data = BytesIO(response.content)
            image = Image.open(image_data)  # Open the image
            image = image.resize((SCREEN_WIDTH, SCREEN_HEIGHT), Image.LANCZOS)  # Resize
            bg_image = ImageTk.PhotoImage(image)

            self.canvas.create_image(0, 0, anchor='nw', image=bg_image)
            self.canvas.bg_image = bg_image

            # Add buttons after the image is loaded
            self.add_buttons()
        except Exception as e:
            self.display_error(f"Error loading image: {str(e)}")

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

    def register_child_window(self, window):
        """Register a child window."""
        self.child_windows.append(window)

    def unregister_child_window(self, window):
        """Unregister a child window."""
        self.child_windows = [w for w in self.child_windows if w != window and w.winfo_exists()]

if __name__ == "__main__":
    root = tk.Tk()
    app = PhotoFrameApp(root)
    root.mainloop()