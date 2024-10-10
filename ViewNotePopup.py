import tkinter as tk
from tkinter import Frame, Label, Button
from PIL import Image, ImageTk
from constant import *  
from PopupHeader import PopupHeader  
from utils import center_window_parent

class NoteItem:
    """
    A class representing a single note item in the ViewNotePopup.

    This class creates and manages the display of individual note items,
    including the title, end time, and expandable note content.
    """

    def __init__(self, parent, title, end_time, note_value):
        """
        Initialize a NoteItem.

        Args:
            parent (tk.Widget): The parent widget to contain this note item.
            title (str): The title of the note.
            end_time (str): The end time or date of the note.
            note_value (str): The content of the note.
        """
        self.parent = parent
        self.title = title
        self.end_time = end_time
        self.note_value = note_value
        self.details_visible = False
        self.time_icon_photo = None
        self.dropdown_photo = None
        self.dropdown_photo_inversed = None
        self.arrow_icon = None
        self.details_label = None
        self.show_note()

    def show_note(self):
        """Create and display the note item in the parent widget."""
        # Create the main frame for the note
        self.note_frame = Frame(self.parent, bg=INPUT_COLOR, bd=1, relief="solid")
        self.note_frame.pack(fill="x", padx=20, pady=10)
        
        # Note Title
        note_title_label = Label(self.note_frame, text=self.title, font=FONT_MEDIUM, bg=INPUT_COLOR)
        note_title_label.pack(anchor="w", padx=10, pady=(5, 0))

        # Frame for time and dropdown icon
        info_frame = Frame(self.note_frame, bg=INPUT_COLOR)
        info_frame.pack(anchor="w", padx=10, pady=(2, 0), fill="x")

        # Load and display End Time Icon
        self._load_time_icon(info_frame)

        # End Time Label
        end_time_label = Label(
            info_frame,
            text=self.end_time,
            font=FONT_SMALL,
            fg=CLOSE_COLOR,
            bg=INPUT_COLOR
        )
        end_time_label.pack(side="left", padx=(5, 0))  

        # Conditionally create the dropdown arrow if note_value exists
        if self.note_value:
            self._create_dropdown_arrow(info_frame)
            self._bind_click_events(note_title_label, end_time_label)

    def _load_time_icon(self, parent_frame):
        """Load and display the time icon."""
        try:
            time_icon_image = Image.open(TIME_ICON)
            time_icon_image = time_icon_image.resize((10, 10), Image.LANCZOS)
            self.time_icon_photo = ImageTk.PhotoImage(time_icon_image)
        except Exception as e:
            print(f"Error loading TIME_ICON: {e}")
            self.time_icon_photo = None

        time_icon_label = Label(parent_frame, image=self.time_icon_photo, bg=INPUT_COLOR)
        time_icon_label.pack(side="left")
        time_icon_label.image = self.time_icon_photo  # Keep a reference

    def _create_dropdown_arrow(self, parent_frame):
        """Create and display the dropdown arrow for expandable notes."""
        try:
            # Load and resize the dropdown icons
            dropdown_icon_image = Image.open(DROPDOWN_ICON)
            dropdown_icon_image = dropdown_icon_image.resize((10, 10), Image.LANCZOS)
            self.dropdown_photo = ImageTk.PhotoImage(dropdown_icon_image)

            dropdown_icon_inversed_image = Image.open(DROPDOWN_ICON_INVERSED)
            dropdown_icon_inversed_image = dropdown_icon_inversed_image.resize((10, 10), Image.LANCZOS)
            self.dropdown_photo_inversed = ImageTk.PhotoImage(dropdown_icon_inversed_image)
        except Exception as e:
            print(f"Error loading dropdown icons: {e}")
            self.dropdown_photo = None
            self.dropdown_photo_inversed = None

        self.arrow_icon = Label(parent_frame, image=self.dropdown_photo, bg=INPUT_COLOR)
        self.arrow_icon.image = self.dropdown_photo  # Keep a reference
        self.arrow_icon.pack(side="right")

    def _bind_click_events(self, title_label, time_label):
        """Bind click events to toggle note details."""
        toggle = self.toggle_note_details
        self.note_frame.bind("<Button-1>", toggle)
        title_label.bind("<Button-1>", toggle)
        time_label.bind("<Button-1>", toggle)
        self.arrow_icon.bind("<Button-1>", toggle)

    def toggle_note_details(self, event=None):
        """Toggle the visibility of note details."""
        if self.details_visible:
            # Hide details
            if self.details_label and self.details_label.winfo_exists():
                self.details_label.destroy()
            self.details_visible = False
            self.arrow_icon.configure(image=self.dropdown_photo)
            self.arrow_icon.image = self.dropdown_photo
        else:
            # Show details
            self.details_label = Label(
                self.note_frame,
                text=self.note_value, 
                font=FONT_SMALL, 
                bg=INPUT_COLOR, 
                wraplength=FRAME_WIDTH - 40,  
                justify="left"
            )
            self.details_label.pack(side="left")

            self.details_visible = True
            self.arrow_icon.configure(image=self.dropdown_photo_inversed)
            self.arrow_icon.image = self.dropdown_photo_inversed

class ViewNotePopup:
    """
    A class to create and manage the popup window for viewing notes.

    This class handles the creation of the popup window and the display
    of all saved notes using NoteItem instances.
    """

    def __init__(self, root, app):
        """
        Initialize the ViewNotePopup.

        Args:
            root (tk.Tk): The root window of the application.
            app: The main application instance containing saved notes.
        """
        self.root = root
        self.app = app
        self.popup_window = None

    def show_notes(self):
        """Create and display the popup window with all saved notes."""
        if self.popup_window is None or not self.popup_window.winfo_exists():
            self._create_popup_window()
            self._add_header()
            self._display_notes()

    def _create_popup_window(self):
        """Create the main popup window."""
        self.popup_window = tk.Toplevel(self.root)
        self.popup_window.configure(bg=POPUP_BG_COLOR)
        self.popup_window.geometry(f"{POPUP_WIDTH}x{POPUP_HEIGHT}")
        self.popup_window.overrideredirect(True)  # Hide the default title bar
        center_window_parent(self.popup_window, POPUP_WIDTH, POPUP_HEIGHT)

        self.main_frame = Frame(self.popup_window, bg=POPUP_BG_COLOR)
        self.main_frame.pack(fill="both", expand=True)

    def _add_header(self):
        """Add the header to the popup window."""
        PopupHeader(parent=self.main_frame, title_text="View Notes", on_close=self.close_popup)

    def _display_notes(self):
        """Display all saved notes or a message if no notes are available."""
        if not hasattr(self.app, 'saved_notes') or not self.app.saved_notes:
            self._display_no_notes_message()
        else:
            self._create_note_items()

    def _display_no_notes_message(self):
        """Display a message when no notes are available."""
        no_notes_label = Label(
            self.main_frame,
            text="No notes available.",
            font=FONT_MEDIUM,
            bg=POPUP_BG_COLOR
        )
        no_notes_label.pack(pady=20)

    def _create_note_items(self):
        """Create NoteItem instances for each saved note."""
        for note in self.app.saved_notes:
            NoteItem(
                parent=self.main_frame, 
                title=note.get('name', 'Untitled'), 
                end_time=note.get('end_date', 'No Date'), 
                note_value=note.get('note', '')
            )

    def close_popup(self):
        """Close the popup window."""
        if self.popup_window:
            self.popup_window.destroy()
            self.popup_window = None

    def quit_app(self):
        """Quit the entire application."""
        self.root.quit()


if __name__ == "__main__":
    # Test code for the ViewNotePopup
    root = tk.Tk()
    root.withdraw()  # Hide the main root window
    app = type('', (), {
        'saved_notes': [
            {
                'name': 'Sample Note 1',
                'end_date': 'Friday 13:00',
                'note': 'This is the first sample note description. It is concise.'
            },
            {
                'name': 'Sample Note 2',
                'end_date': 'Saturday 14:00',
                'note': 'This is the second sample note description. It is a bit longer to demonstrate dynamic expansion based on content length.'
            },
            {
                'name': 'Sample Note 3',
                'end_date': 'Sunday 15:00',
                'note': 'Short note.'
            },
            {
                'name': 'Sample Note 4',
                'end_date': 'Monday 16:00',
                'note': ''  # This note has no content and should not show toggle
            }
        ]
    })()
    note_page = ViewNotePopup(root, app)
    note_page.show_notes()
    root.mainloop()