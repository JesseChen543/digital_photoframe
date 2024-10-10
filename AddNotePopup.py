# AddNotePopup.py
import tkinter as tk
from tkinter import ttk, Frame
from PIL import Image, ImageTk
from constant import *
from datetime import datetime
from PopupHeader import PopupHeader
from utils import center_window_parent

class AddNotePopup:
    """
    A class to create and manage a popup window for adding notes.

    This class handles the creation of a popup window where users can input
    a note name, end date/time, and note content. It also manages the date
    selection process and validation of user inputs.
    """

    def __init__(self, root, app):
        """
        Initialize the AddNotePopup instance.

        Args:
            root (tk.Tk): The root window of the application.
            app: The main application instance.
        """
        self.root = root
        self.app = app  
        self.popup_window = None
        self.pick_date_popup = None
        self.selected_day_button = None 
        self.list_name_entry = None
        self.note_entry = None
        self.selected_day = None  
        self.selected_time = None
        self.End_time_combobox = None 
        self.choose_date_button = None
        self.name_error_label = None

    def add_note(self):
        """
        Create and display the main note addition popup window.

        This method sets up the UI for adding a new note, including input fields
        for the note name, end date/time, and note content.
        """
        if self.popup_window is None or not self.popup_window.winfo_exists():
            self.popup_window = tk.Toplevel(self.root)
            self.popup_window.configure(bg=POPUP_BG_COLOR)
            self.popup_window.geometry(f"{POPUP_WIDTH}x{POPUP_HEIGHT}")

            # Hide the default title bar
            self.popup_window.overrideredirect(True)

            # Bind the closing event
            self.popup_window.protocol("WM_DELETE_WINDOW", self.close_popup)

            main_frame = Frame(self.popup_window, bg=POPUP_BG_COLOR)
            main_frame.pack(fill="both", expand=True)

            # Utilize PopupHeader to create the header
            PopupHeader(parent=main_frame, title_text="Write a Note", on_close=self.close_popup)

            # Inner frame for form fields
            inner_frame = Frame(main_frame, bg=POPUP_BG_COLOR)
            inner_frame.pack(fill="both", expand=True, padx=20, pady=20)

            # List Name 
            list_name_frame = Frame(inner_frame, bg=POPUP_BG_COLOR)
            list_name_frame.pack(fill="x", pady=5)

            # Label and error message container
            name_label_frame = Frame(list_name_frame, bg=POPUP_BG_COLOR)
            name_label_frame.pack(fill="x")

            # Label 
            list_name_label = tk.Label(name_label_frame, text="Name:", bg=POPUP_BG_COLOR, font=FONT_SMALL)
            list_name_label.pack(side="left", padx=5)

            # Error message (initially hidden)
            self.name_error_label = tk.Label(name_label_frame, text="Name can't be empty", bg=POPUP_BG_COLOR, fg="red", font=FONT_SMALL)
            self.name_error_label.pack(side="left", padx=5)
            self.name_error_label.pack_forget()  # Hide it initially

            # Entry 
            self.list_name_entry = tk.Entry(
                list_name_frame, 
                font=FONT_SMALL, 
                relief="solid", 
                bd=1, 
                width=LIST_NAME_WIDTH, 
                bg=INPUT_COLOR, 
                borderwidth=0
            )
            self.list_name_entry.pack(fill="x", padx=5, pady=5)

            # Bind the entry to a validation function
            self.list_name_entry.bind("<FocusOut>", self.validate_name)

            # End Date
            end_frame = Frame(inner_frame, bg=POPUP_BG_COLOR)
            end_frame.pack(fill="x", pady=5)

            end_label = tk.Label(end_frame, text="End:", bg=POPUP_BG_COLOR, font=FONT_SMALL)
            end_label.pack(side="left", padx=5)

            # Create a frame for the button with the same background color as end_frame
            date_button_frame = tk.Frame(end_frame, bg=PREFILLED_BG_COLOR)  
            date_button_frame.pack(side="right", padx=5)

            # Load the image for the button 
            date_icon_image = Image.open(UPCOMING_SCHEDULE_ICON)  
            date_icon_image = date_icon_image.resize((20, 20), Image.LANCZOS)  
            date_icon_photo = ImageTk.PhotoImage(date_icon_image)

            # Create an image label and place it in the frame
            image_label = tk.Label(date_button_frame, image=date_icon_photo, bg=date_button_frame.cget("bg"))
            image_label.pack(side="left", padx=(0, 5))  

            # Create the button and place it in the frame
            self.choose_date_button = tk.Button(
                date_button_frame,
                text="Choose Date",
                command=self.pick_date,
                font=FONT_PREFILLED,
                fg=CHOOSE_DATE_PREFILLED_COLOR,
                borderwidth=0
            )
            self.choose_date_button.pack(side="right")  

            # Keep a reference to the image to prevent garbage collection
            image_label.image = date_icon_photo

            # Note
            note_frame = Frame(inner_frame, bg=POPUP_BG_COLOR)
            note_frame.pack(fill="x", pady=5)

            note_label = tk.Label(note_frame, text="Note:", bg=POPUP_BG_COLOR, font=FONT_SMALL)
            note_label.pack(side="top", anchor="w", padx=5)

            self.note_entry = tk.Text(
                note_frame, 
                font=FONT_SMALL, 
                relief="solid", 
                bd=1, 
                height=7, 
                width=LIST_NAME_WIDTH, 
                bg=INPUT_COLOR, 
                borderwidth=0
            )
            self.note_entry.pack(fill="both", padx=5, pady=5, expand=True)

            # Submit button at the bottom
            submit_button = tk.Button(
                self.popup_window, 
                text="Upload", 
                bg=BUTTON_COLOR, 
                fg=BUTTON_TEXT_COLOR, 
                font=FONT_MEDIUM, 
                relief="flat", 
                command=self.submit_note
            )
            submit_button.pack(anchor="e", padx=10, pady=10)

            # Center the popup window after all content has been added
            self.popup_window.update_idletasks()
            center_window_parent(self.popup_window, self.popup_window.winfo_width(), self.popup_window.winfo_height())

            # Register this window with the main app
            self.app.register_child_window(self.popup_window)

    def validate_name(self, event=None):
        if not self.list_name_entry.get().strip():
            self.name_error_label.pack(side="left", padx=5)
        else:
            self.name_error_label.pack_forget()

    def submit_note(self):
        name = self.list_name_entry.get().strip()
        if name:
            end_date = self.choose_date_button.cget("text")
            note = self.note_entry.get("1.0", tk.END).strip()
            
            # Append the note to the app's saved_notes list
            self.app.saved_notes.append({
                "name": name,
                "end_date": end_date,
                "note": note
            })
            
            print(f"Submitted note - Name: {name}, End Date: {end_date}, Note: {note}")
            
            # Update the list button after submitting the note
            self.app.update_view_note_button()
            
            self.close_popup()
        else:
            self.validate_name()  # Show the error message
            print("Error: Please enter a name for the note.")

    # Method to close the popup
    def close_popup(self):
        if self.pick_date_popup and self.pick_date_popup.winfo_exists():
            self.on_window_close(self.pick_date_popup)
            self.pick_date_popup = None
        self.on_window_close(self.popup_window)
        self.popup_window = None

    def pick_date(self):
        self.pick_date_popup = tk.Toplevel(self.root)
        self.pick_date_popup.configure(bg=POPUP_BG_COLOR)

        # Hide the default title bar
        self.pick_date_popup.overrideredirect(True)
        
        # Bind the closing event
        self.pick_date_popup.protocol("WM_DELETE_WINDOW", self.close_pick_date_popup)

        # Center the pick_date_popup
        center_window_parent(self.pick_date_popup, 240, 200) 

        # Reset the selected day button reference to None
        self.selected_day_button = None

        # Configure the grid for the popup window
        self.pick_date_popup.grid_columnconfigure(0, weight=1)

        # Title Label 
        title_label = tk.Label(
            self.pick_date_popup, 
            text="Week", 
            font=FONT_LARGE, 
            bg=POPUP_BG_COLOR, 
            fg=PICK_DATE_TEXT_COLOR
        )
        title_label.grid(row=0, column=0, sticky='w', padx=15, pady=10)

        # Days of the week
        days_frame = tk.Frame(self.pick_date_popup, bg=POPUP_BG_COLOR)
        days_frame.grid(row=1, column=0, padx=15, pady=5, sticky='w')
        days_of_week = ["Mo", "Tu", "We", "Th", "Fr", "Sa", "Su"]
        
        for i, day in enumerate(days_of_week):
            tk.Label(
                days_frame, 
                text=day, 
                bg=POPUP_BG_COLOR, 
                fg=PICK_DATE_TEXT_COLOR, 
                font=FONT_SMALL
            ).grid(row=0, column=i, padx=2, pady=2)

        def select_day(button, day):
            if self.selected_day_button:
                self.selected_day_button.config(bg=POPUP_BG_COLOR)
            button.config(bg=BUTTON_COLOR)
            self.selected_day_button = button
            self.selected_day = day

        for i in range(1, 8):
            day_button = tk.Button(
                days_frame, 
                text=str(i), 
                bg=POPUP_BG_COLOR, 
                fg=PICK_DATE_TEXT_COLOR,
                font=FONT_SMALL, 
                width=2, 
                height=1, 
                borderwidth=0,       
                highlightthickness=0  
            )
            day_button.grid(row=1, column=i-1, padx=2, pady=2)
            day_button.config(command=lambda b=i, btn=day_button: select_day(btn, b))

        # Time selection frame
        time_frame = tk.Frame(self.pick_date_popup, bg=POPUP_BG_COLOR)
        time_frame.grid(row=2, column=0, padx=15, pady=10, sticky='w')

        tk.Label(
            time_frame, 
            text="End", 
            bg=POPUP_BG_COLOR, 
            fg=PICK_DATE_TEXT_COLOR, 
            font=FONT_SMALL
        ).pack(side='left', padx=(0, 5))

        # Create a frame for the combobox with icon and border
        combobox_frame = tk.Frame(time_frame, bg="white", bd=1, relief="solid")
        combobox_frame.pack(side='left')

        # Time icon
        time_icon_image = Image.open(TIME_ICON)
        time_icon_image = time_icon_image.resize((16, 16), Image.LANCZOS)
        time_icon_photo = ImageTk.PhotoImage(time_icon_image)
        
        time_icon_label = tk.Label(
            combobox_frame, 
            image=time_icon_photo, 
            bg="white"
        )
        time_icon_label.pack(side='left', padx=(2, 0))
        time_icon_label.image = time_icon_photo

        # Combobox style
        style = ttk.Style()
        style.layout('Borderless.TCombobox', [
            ('Combobox.padding', {'children': [
                ('Combobox.background', {'children': [
                    ('Combobox.dropdownarrow', {'side': 'right', 'sticky': 'ns'}),
                    ('Combobox.textarea', {'sticky': 'nswe'})
                ]})
            ]})
        ])
        style.configure("Borderless.TCombobox", 
                        foreground=PICK_DATE_PREFILLED_COLOR,
                        background="white",
                        fieldbackground="white",
                        borderwidth=0,
                        highlightthickness=0,
                        arrowsize=12)
        style.map('Borderless.TCombobox', 
                  fieldbackground=[('readonly', 'white')],
                  selectbackground=[('readonly', 'white')],
                  selectforeground=[('readonly', PICK_DATE_PREFILLED_COLOR)])

        self.End_time_combobox = ttk.Combobox(
            combobox_frame, 
            values=TIME_OPTIONS, 
            font=FONT_SMALL, 
            width=5,  # Keep this width for the combobox itself
            style="Borderless.TCombobox",
            state="readonly"
        )
        self.End_time_combobox.pack(side='left', padx=(0, 2))
        self.End_time_combobox.set("12:00")

        # Function to adjust dropdown width
        def adjust_dropdown_width():
            self.End_time_combobox.config(width=8)  # Adjust this value to make the dropdown wider
            self.End_time_combobox.after(10, lambda: self.End_time_combobox.config(width=5))  # Reset width after dropdown opens

        # Set the postcommand to adjust the width
        self.End_time_combobox.config(postcommand=adjust_dropdown_width)

        # Bind event to change border color on focus
        combobox_frame.bind("<FocusIn>", lambda e: combobox_frame.config(highlightbackground="blue", highlightthickness=2))
        combobox_frame.bind("<FocusOut>", lambda e: combobox_frame.config(highlightbackground="gray75", highlightthickness=1))
        self.End_time_combobox.bind("<FocusIn>", lambda e: combobox_frame.focus_set())

        # Confirm Button
        confirm_button = tk.Button(
            self.pick_date_popup, 
            text="Confirm", 
            bg=BUTTON_COLOR, 
            fg="white", 
            font=FONT_SMALL, 
            relief="flat", 
            command=self.confirm_selection
        )
        confirm_button.grid(row=3, column=0, pady=10, padx=15, sticky='e')

        # Force focus and lift the window
        self.pick_date_popup.focus_force()
        self.pick_date_popup.update()
        self.pick_date_popup.lift()

        # Register this window with the main app
        self.app.register_child_window(self.pick_date_popup)

    def confirm_selection(self):
        # Retrieve the selected time from the Combobox
        self.selected_time = self.End_time_combobox.get()

        if self.selected_day is not None and self.selected_time:
            # Get the current date and time
            current_time = datetime.now()
            # Get the current day of the week (0 = Monday, 6 = Sunday)
            current_day = current_time.weekday()
            
            # Convert selected_day to match current_day format (0 = Monday, 6 = Sunday)
            selected_day_adjusted = (self.selected_day - 1) % 7

            # Create a datetime object for the selected time
            selected_time = datetime.strptime(self.selected_time, "%H:%M").time()
            selected_datetime = datetime.combine(current_time.date(), selected_time)

            # Check if the selected day is today
            if selected_day_adjusted == current_day:
                # If it's today, ensure the selected time is later than the current time
                if selected_datetime <= current_time:
                    print("Time Error: Please select a time later than the current time.")
                    self.pick_date_popup.focus_force()
                    return
            elif selected_day_adjusted < current_day:
                # If the selected day is earlier in the week, assume it's for next week
                print("Date Info: The selected day is in the next week.")
                self.pick_date_popup.focus_force()

            # Update the Choose Date button text
            day_names = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
            day_text = day_names[selected_day_adjusted]
            self.choose_date_button.config(text=f"{day_text} {self.selected_time}")
            
            # Optionally, store it in the app or a variable
            self.app.saved_end_value = f"Day: {day_text}, Time: {self.selected_time}" 
            
            self.close_pick_date_popup()  # Close the pick date popup
            self.popup_window.focus_force()  # Ensure focus returns to the main AddNotePopup window
        else:
            print("Selection Error: Please select both a day and a time.")
            self.pick_date_popup.focus_force()

    def close_pick_date_popup(self):
        self.on_window_close(self.pick_date_popup)
        self.pick_date_popup = None
        self.popup_window.focus_force()  # Ensure focus returns to the main AddNotePopup window

    def on_window_close(self, window):
        """Generic method to handle window closing"""
        if window:
            self.app.unregister_child_window(window)
            window.destroy()