import tkinter as tk
from tkinter import Frame, Label, Button
from PIL import Image, ImageTk
from constant import *  
from PopupHeader import PopupHeader  
from utils import center_window_parent

class ViewNotePopup:
    def __init__(self, root, app):
        self.root = root
        self.app = app
        self.popup_window = None  

    def show_list(self):
        if self.popup_window is None or not self.popup_window.winfo_exists():
            self.popup_window = tk.Toplevel(self.root)
            self.popup_window.configure(bg=POPUP_BG_COLOR)
            self.popup_window.geometry(f"{POPUP_WIDTH}x{POPUP_HEIGHT}")

            # Hide the default title bar
            self.popup_window.overrideredirect(True)

            # Center the popup window relative to the root window
            center_window_parent(self.popup_window, POPUP_WIDTH, POPUP_HEIGHT)

            self.main_frame = Frame(self.popup_window, bg=POPUP_BG_COLOR)
            self.main_frame.pack(fill="both", expand=True)

            # Utilize PopupHeader to create the header
            PopupHeader(parent=self.main_frame, title_text="Upcoming Schedule", on_close=self.close_popup)

            # Create a note item using the saved values
            self.create_note_item(self.app.saved_list_name, self.app.saved_end_value)

    def close_popup(self):
        if self.popup_window:
            self.popup_window.destroy()
            self.popup_window = None

    def create_note_item(self, title, end_time):
        """Function to create a note item with a title, end time, and dropdown arrow using place."""
        self.note_frame = Frame(self.main_frame, bg=INPUT_COLOR, bd=1, relief="solid")
        self.note_frame.pack(fill="x", padx=20, pady=10)
        self.note_frame.update_idletasks()  # Ensure frame dimensions are updated

        self.note_frame.config(width=FRAME_WIDTH, height=FRAME_HEIGHT_COLLAPSED)

        # Note Title
        note_title_label = Label(self.note_frame, text=title, font=FONT_MEDIUM, bg=INPUT_COLOR)
        note_title_label.place(x=10, y=5)

        # End Time Icon
        try:
            time_icon_image = Image.open(TIME_ICON)
            time_icon_image = time_icon_image.resize((10, 10), Image.LANCZOS)
            self.time_icon_photo = ImageTk.PhotoImage(time_icon_image)
        except Exception as e:
            print(f"Error loading TIME_ICON: {e}")
            self.time_icon_photo = None

        if self.time_icon_photo:
            time_icon_label = Label(self.note_frame, image=self.time_icon_photo, bg=INPUT_COLOR)
            time_icon_label.place(x=10, y=28)  # Adjusted y from 30 to 25
        else:
            # If the icon fails to load, use a smaller placeholder
            time_icon_label = Label(self.note_frame, text="⌚", font=FONT_SMALL, bg=INPUT_COLOR)
            time_icon_label.place(x=10, y=25)  # Adjusted y from 30 to 25

        # End Time Label
        end_time_label = Label(
            self.note_frame,
            text=end_time,
            font=FONT_SMALL,
            fg=CLOSE_COLOR,
            bg=INPUT_COLOR
        )
        # Position end_time_label right next to the icon with adjusted y
        end_time_label.place(x=25, y=25)  

        # Load and resize the dropdown icon
        try:
            dropdown_icon_image = Image.open(DROPDOWN_ICON)
            dropdown_icon_image = dropdown_icon_image.resize((10, 10), Image.LANCZOS)
            self.dropdown_photo = ImageTk.PhotoImage(dropdown_icon_image)
        except Exception as e:
            print(f"Error loading DROPDOWN_ICON: {e}")
            self.dropdown_photo = None

        # Create a label with the dropdown icon
        if self.dropdown_photo:
            arrow_icon = Label(self.note_frame, image=self.dropdown_photo, bg=INPUT_COLOR)
            arrow_icon.image = self.dropdown_photo  # Keep a reference to prevent garbage collection
            arrow_icon.place(x=FRAME_WIDTH - 20, y=20)
        else:
            arrow_icon = Label(self.note_frame, text="▼", font=FONT_SMALL, bg=INPUT_COLOR)
            arrow_icon.place(x=FRAME_WIDTH - 20, y=20)

        # Bind click event to toggle note details
        # Use a consistent method reference to avoid creating multiple instances
        toggle = lambda event: self.toggle_note_details()
        self.note_frame.bind("<Button-1>", toggle)
        note_title_label.bind("<Button-1>", toggle)
        time_icon_label.bind("<Button-1>", toggle)
        end_time_label.bind("<Button-1>", toggle)
        arrow_icon.bind("<Button-1>", toggle)

    def toggle_note_details(self):
        """Toggle the visibility of note details."""
        if self.details_label and self.details_label.winfo_exists():
            # Details are visible; destroy them and collapse the frame
            self.details_label.destroy()
            self.details_label = None
            self.note_frame.config(height=50)  # Collapse back to original height
        else:
            # Details are not visible; create them and expand the frame
            self.details_label = Label(
                self.note_frame,
                text=self.app.saved_note_value, 
                font=FONT_SMALL, 
                bg=INPUT_COLOR, 
                wraplength=FRAME_WIDTH - 20, 
                justify="left"
            )
            self.details_label.place(x=10, y=45)  

            self.note_frame.config(height=100)  

    def quit_app(self):
        self.root.quit()


if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()  # Hide the main root window if you only want the popup to show
    app = type('', (), {
        'saved_list_name': 'Sample Note', 
        'saved_end_value': 'Friday 13:00', 
        'saved_note_value': 'This is a sample note description that appears when the dropdown is clicked.'
    })()
    note_page = ViewNotePopup(root, app)
    note_page.show_list()
    root.mainloop()