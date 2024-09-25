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

        # Add add-note icon 
        round_icon = Image.open(WRITE_NOTE_ICON_IMAGE_PATH).resize((30, 30), Image.LANCZOS)
        icon_image = ImageTk.PhotoImage(round_icon)
        icon_button = tk.Button(self.root, image=icon_image, command=self.note_popup.show_note, borderwidth=0)
        icon_button.image = icon_image
        icon_button.place(x=SCREEN_WIDTH - 60, y=10)

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
