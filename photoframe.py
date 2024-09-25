import tkinter as tk
from tkinter import ttk, Frame
from tkinter.simpledialog import askstring
from PIL import Image, ImageTk
from datetime import datetime
from NotePopup import NotePopup  # Import the NotePopup class
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

        # Load and display the full-screen image (replace with backend)
        image_path = BACKGROUND_IMAGE_PATH
        image = Image.open(image_path)
        image = image.resize((SCREEN_WIDTH, SCREEN_HEIGHT), Image.LANCZOS)
        bg_image = ImageTk.PhotoImage(image)

        bg_label = tk.Label(self.root, image=bg_image)
        bg_label.image = bg_image
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Make the icon round (not functional yet)
        round_icon = Image.open(WRITE_NOTE_ICON_IMAGE_PATH).resize((30,30), Image.LANCZOS)
        icon_image = ImageTk.PhotoImage(round_icon)

        icon_button = tk.Button(self.root, image=icon_image, command=self.note_popup.show_note, borderwidth=0)
        icon_button.image = icon_image
        icon_button.place(x=SCREEN_WIDTH - 60, y=10)

        self.root.geometry(f"{SCREEN_WIDTH}x{SCREEN_HEIGHT}")
        self.root.bind('<Escape>', self.quit_app)

    def quit_app(self, event=None):
        self.root.quit()

if __name__ == "__main__":
    root = tk.Tk()
    app = PhotoFrameApp(root)
    root.mainloop()
