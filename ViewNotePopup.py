import tkinter as tk
from tkinter import Frame, Label, Button
from PIL import Image, ImageTk
from constant import *  # Import constants

class ViewNotePopup:
    def __init__(self, root, app):
        self.root = root
        self.app = app
        self.popup = None

    def show_list(self):
        # Check if the popup already exists
        if self.popup and self.popup.winfo_exists():
            self.popup.lift()  # Bring the existing popup to the front
            return
        
        # Create a new popup window
        self.popup = tk.Toplevel(self.root)
        self.popup.title("Note")
        self.popup.geometry(f"{POPUP_WIDTH}x{POPUP_HEIGHT}")
        self.popup.configure(bg=POPUP_BG_COLOR)

        # Create the top frame for the title and close button
        top_frame = Frame(self.popup, bg=POPUP_BG_COLOR)
        top_frame.pack(fill="x", pady=10)

        # Title label
        title_label = Label(top_frame, text="Note", font=FONT_LARGE, bg=POPUP_BG_COLOR)
        title_label.pack(side="left", padx=20)

        # Close button
        close_button = Button(top_frame, text="X", command=self.close_popup, 
                              bg="white", fg=CLOSE_COLOR, font=(FONT_SMALL, 12), relief="flat")
        close_button.pack(side="right", padx=10)

        # Separator line
        separator = tk.Frame(self.popup, bg="grey", height=1)
        separator.pack(fill="x", pady=5)

        # Create a note item using the saved values
        self.create_note_item(self.app.saved_list_name, self.app.saved_end_value)

    def close_popup(self):
        if self.popup:
            self.popup.destroy()
            self.popup = None
            

    def create_note_item(self, title, end_time):
        """Function to create a note item with a title, end time, and dropdown arrow."""
        note_frame = Frame(self.popup, bg="#F3F5F8", bd=1, relief="solid")
        note_frame.pack(fill="x", padx=20, pady=10)

        # Note Title
        note_title_label = Label(note_frame, text=title, font=FONT_MEDIUM, bg="#F3F5F8")
        note_title_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")

        # End Time
        end_time_label = Label(note_frame, text=f"End: {end_time}", font=FONT_SMALL, fg="grey", bg="#F3F5F8")
        end_time_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")

        # Load and resize the dropdown icon
        dropdown_icon = Image.open(DROPDOWN_ICON)
        dropdown_icon = dropdown_icon.resize((10, 10), Image.LANCZOS)  
        dropdown_photo = ImageTk.PhotoImage(dropdown_icon)

        # Create a label with the dropdown icon
        arrow_icon = Label(note_frame, image=dropdown_photo, bg="#F3F5F8")
        arrow_icon.image = dropdown_photo  # Keep a reference to prevent garbage collection
        arrow_icon.grid(row=0, column=1, padx=10, pady=5, sticky="e", rowspan=2)

        # Bind click event to toggle note details
        note_frame.bind("<Button-1>", lambda event: self.toggle_note_details(event, note_frame))

    def toggle_note_details(self, event, note_frame):
        """Toggle the visibility of note details."""
        details_frame = note_frame.grid_slaves(row=2, column=0)
        if not details_frame:
            details = Label(note_frame, text=self.app.saved_note_value, 
                            font=FONT_SMALL, bg="#F3F5F8", wraplength=300, justify="left")
            details.grid(row=2, column=0, columnspan=2, padx=10, pady=5, sticky="w")
        else:
            details_frame[0].destroy()

    def quit_app(self):
        self.root.quit()


if __name__ == "__main__":
    root = tk.Tk()
    app = type('', (), {'saved_list_name': 'Sample Note', 'saved_end_value': '01/01/2024', 'saved_note_value': 'This is a sample note.'})()
    note_page = ViewNotePopup(root, app)
    note_page.show_list()
    root.mainloop()
