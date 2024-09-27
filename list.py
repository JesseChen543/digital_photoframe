import tkinter as tk
from tkinter import Frame, PhotoImage, Label, Button
from PIL import Image, ImageTk
from constant import *  # assuming you have a constants file with dimensions and color

class NotePage:
    def __init__(self, root):
        self.root = root
        self.root.title("Note Page")

        # Set the window size and background color
        self.root.geometry(f"{SCREEN_WIDTH}x{SCREEN_HEIGHT}")
        self.root.configure(bg=POPUP_BG_COLOR)

        # Create the top frame for the title and close button
        top_frame = Frame(self.root, bg=POPUP_BG_COLOR)
        top_frame.pack(fill="x", pady=10)

        # Title label
        title_label = Label(top_frame, text="Note", font=FONT_LARGE, bg=POPUP_BG_COLOR)
        title_label.pack(side="left", padx=20)

        # Separator line
        separator = tk.Frame(self.root, bg="grey", height=1)
        separator.pack(fill="x", padx=20, pady=5)

        # Create a list of note items
        for _ in range(2):  # Just add 2 note items for the example
            self.create_note_item("Shopping", "05/09/2024 12:00")

    def create_note_item(self, title, end_time):
        """Function to create a note item with a title, end time, and dropdown arrow."""
        note_frame = Frame(self.root, bg="#F3F5F8", bd=1, relief="solid")
        note_frame.pack(fill="x", padx=20, pady=10)

        # Note Title
        note_title_label = Label(note_frame, text=title, font=FONT_MEDIUM, bg="#F3F5F8")
        note_title_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")

        # End Time
        end_time_label = Label(note_frame, text=f"End: {end_time}", font=FONT_SMALL, fg="grey", bg="#F3F5F8")
        end_time_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")

        # Dropdown arrow (You can replace this with an actual arrow icon)
        arrow_icon = Label(note_frame, image=DROPDOWN_ICON, font=FONT_MEDIUM, bg="#F3F5F8")
        arrow_icon.grid(row=0, column=1, padx=10, pady=5, sticky="e", rowspan=2)

    def quit_app(self):
        self.root.quit()


if __name__ == "__main__":
    root = tk.Tk()
    app = NotePage(root)
    root.mainloop()
