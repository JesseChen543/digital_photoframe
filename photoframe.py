import tkinter as tk
from round_button import CanvasButton
from PIL import Image, ImageTk
from datetime import datetime
from AddNotePopup import AddNotePopup 
from ViewNotePopup import ViewNotePopup
import requests  # To fetch the image from the URL
from io import BytesIO  # To convert the image data into a usable format

from constant import *

class PhotoFrameApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Display with Clickable Icon")

        # Initialize saved inputs
        self.saved_list_name = ""
        self.saved_end_value = ""
        self.saved_note_value = ""
        self.current_date = datetime.now().strftime("%d/%m/%Y")

        # Initialize NotePopup
        self.add_note_popup = AddNotePopup(self.root, self)

        self.view_note_popup = ViewNotePopup(self.root, self)
        

        # initialize ListPopup
        # Load and display the full-screen image from URL 
        image_url = "https://deco3801-foundjesse.uqcloud.net/IMG_6423.jpg"
        response = requests.get(image_url)
        # Check if the request was successful
        if response.status_code == 200:
            try:
                image_data = BytesIO(response.content)
                image = Image.open(image_data)  # Open the image
                image = image.resize((SCREEN_WIDTH, SCREEN_HEIGHT), Image.LANCZOS)  # Resize
                bg_image = ImageTk.PhotoImage(image)

                # Set the background canvas and image
                self.canvas = tk.Canvas(self.root, width=SCREEN_WIDTH, height=SCREEN_HEIGHT, bd=0, highlightthickness=0)
                self.canvas.pack(fill="both", expand=True)
                self.canvas.create_image(0, 0, anchor='nw', image=bg_image)
                self.canvas.bg_image = bg_image

                # Hide the default title bar
                # self.root.overrideredirect(True)

            except Exception as e:
                print(f"Error loading image: {e}")
                # Handle the error by showing a default image or error message
                error_label = tk.Label(self.root, text="Failed to load image", bg="white")
                error_label.place(x=0, y=0, relwidth=1, relheight=1)
        else:
            print(f"Failed to fetch image. Status code: {response.status_code}")
            # Handle the error by showing a default image or error message
            error_label = tk.Label(self.root, text="Failed to load image", bg="white")
            error_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Add add-note icon using CanvasButton
        CanvasButton(self.canvas, NOTE_ICON_X, NOTE_ICON_Y, 
                                   WRITE_NOTE_ICON_IMAGE_PATH, self.add_note_popup.show_note)


        CanvasButton(self.canvas, CALENDAR_ICON_X, CALENDAR_ICON_Y, 
                                       UPCOMING_SCHEDULE_ICON, self.add_note_popup.show_note)

        CanvasButton(self.canvas, LIST_ICON_X, LIST_ICON_Y, 
                                       LIST_ICON, self.view_note_popup.show_list)

        self.root.geometry(f"{SCREEN_WIDTH}x{SCREEN_HEIGHT}")
        self.root.bind('<Escape>', self.quit_app)

    def update_saved_values(self, list_name, end_value, note_value):
        self.saved_list_name = list_name
        self.saved_end_value = end_value
        self.saved_note_value = note_value
        print(f"Updated values in PhotoFrameApp - Name: {list_name}, End: {end_value}, Note: {note_value}")

    def quit_app(self, event=None):
        self.root.quit()

if __name__ == "__main__":
    root = tk.Tk()
    app = PhotoFrameApp(root)
    root.mainloop()
