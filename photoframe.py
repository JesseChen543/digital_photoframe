import tkinter as tk
from round_button import CanvasButton
from PIL import Image, ImageTk
from datetime import datetime
from NotePopup import NotePopup 
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
        self.note_popup = NotePopup(self.root, self)

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
        icon_button = CanvasButton(self.canvas, SCREEN_WIDTH - 80, 10, WRITE_NOTE_ICON_IMAGE_PATH, self.note_popup.show_note)


        calendar_button = CanvasButton(self.canvas, 80, 10, WRITE_NOTE_ICON_IMAGE_PATH, self.note_popup.show_note)
        
        # Add upcoming schedule icon
        calendar_icon = Image.open(UPCOMING_SCHEDULE_ICON).resize((30, 30), Image.LANCZOS)
        calendar_image = ImageTk.PhotoImage(calendar_icon)
        calendar_button = tk.Button(self.root, image=calendar_image, borderwidth=0)
        calendar_button.image = calendar_image
        calendar_button.place(x=10, y=10)

        # Add list icon
        list_icon = Image.open(LIST_ICON).resize((30, 30), Image.LANCZOS)
        list_image = ImageTk.PhotoImage(list_icon)
        list_button = tk.Button(self.root, image=list_image, borderwidth=0)
        list_button.image = list_image
        list_button.place(x=10, y=60)

        self.root.geometry(f"{SCREEN_WIDTH}x{SCREEN_HEIGHT}")
        self.root.bind('<Escape>', self.quit_app)

    def quit_app(self, event=None):
        self.root.quit()

if __name__ == "__main__":
    root = tk.Tk()
    app = PhotoFrameApp(root)
    root.mainloop()
