import tkinter as tk
from round_button import CanvasButton
from PIL import Image, ImageTk
from datetime import datetime
from AddNotePopup import AddNotePopup 
from ViewNotePopup import ViewNotePopup
from Upcoming_schedule import ViewSchedulePopup
from utils import center_window_parent
import requests  # To fetch the image from the URL
from io import BytesIO  # To convert the image data into a usable format

from constant import *

class PhotoFrameApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Display with Clickable Icon")

        # Initialize list to keep track of child windows
        self.child_windows = []

        self.userid = 2  # Set the user ID (you might want to make this configurable)
        # Initialize saved inputs
        self.saved_notes = []
        self.list_button = None  # Initialize list_button as None
        self.current_date = datetime.now().strftime("%d/%m/%Y")

        # Initialize NotePopup
        self.add_note_popup = AddNotePopup(self.root, self)
        self.view_note_popup = ViewNotePopup(self.root, self)
        self.view_schedule_popup = ViewSchedulePopup(self.root, self)
        

        # Fetch and display the image
        self.fetch_and_display_image()

        # Add add-note icon using CanvasButton
        CanvasButton(self.canvas, NOTE_ICON_X, NOTE_ICON_Y, 
                                   WRITE_NOTE_ICON_IMAGE_PATH, self.add_note_popup.add_note)

        CanvasButton(self.canvas, CALENDAR_ICON_X, CALENDAR_ICON_Y, 
                                       UPCOMING_SCHEDULE_ICON, self.view_schedule_popup.show_schedules)

        # Create the list icon button if self.saved_notes is not None
        if self.saved_notes:
            CanvasButton(self.canvas, LIST_ICON_X, LIST_ICON_Y, 
                                       LIST_ICON, self.view_note_popup.show_notes)

        center_window_parent(self.root, SCREEN_WIDTH, SCREEN_HEIGHT)
        self.root.bind('<Escape>', self.quit_app)

        # Bind the closing event
        self.root.protocol("WM_DELETE_WINDOW", self.quit_app)

    def fetch_and_display_image(self):
        # Fetch image URL from API
        api_url = f"https://deco3801-foundjesse.uqcloud.net/restapi/photo_frame_photos.php?uploader={self.userid}"
        try:
            response = requests.get(api_url)
            response.raise_for_status()  # Raise an exception for bad status codes
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
            image = Image.open(image_data)  # Open the image
            image = image.resize((SCREEN_WIDTH, SCREEN_HEIGHT), Image.LANCZOS)  # Resize
            bg_image = ImageTk.PhotoImage(image)

            self.canvas = tk.Canvas(self.root, width=SCREEN_WIDTH, height=SCREEN_HEIGHT, bd=0, highlightthickness=0)
            self.canvas.pack(fill="both", expand=True)
            self.canvas.create_image(0, 0, anchor='nw', image=bg_image)
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
        # Add add-note icon using CanvasButton
        CanvasButton(self.canvas, NOTE_ICON_X, NOTE_ICON_Y, 
                     WRITE_NOTE_ICON_IMAGE_PATH, self.add_note_popup.add_note)

        CanvasButton(self.canvas, CALENDAR_ICON_X, CALENDAR_ICON_Y, 
                     UPCOMING_SCHEDULE_ICON, self.add_note_popup.add_note)

        # Create the list icon button if self.saved_notes is not None
        if self.saved_notes:
            CanvasButton(self.canvas, LIST_ICON_X, LIST_ICON_Y, 
                         LIST_ICON, self.view_note_popup.show_notes)

    def update_list_button(self):
        """Creates the list button if it doesn't exist and there are saved notes."""
        if self.saved_notes and not self.list_button:
            print("Creating the list button")
            self.list_button = CanvasButton(
                self.canvas,
                LIST_ICON_X,
                LIST_ICON_Y,
                LIST_ICON,
                self.view_note_popup.show_notes
            )


    def quit_app(self, event=None):
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
