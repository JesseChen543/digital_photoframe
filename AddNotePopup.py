# NotePopup.py
import tkinter as tk
from tkinter import ttk, Frame
from PIL import Image, ImageTk
from constant import *
from tkinter import messagebox
from datetime import datetime
from PopupHeader import PopupHeader
from utils import center_window_parent

class AddNotePopup:
    def __init__(self, root, app=None):
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

    def add_note(self):
        if self.popup_window is None or not self.popup_window.winfo_exists():
            self.popup_window = tk.Toplevel(self.root)
            self.popup_window.configure(bg=POPUP_BG_COLOR)
            self.popup_window.geometry(f"{POPUP_WIDTH}x{POPUP_HEIGHT}")

            # Hide the default title bar
            self.popup_window.overrideredirect(True)

            # Center the popup window relative to the root window
            center_window_parent(self.popup_window, POPUP_WIDTH, POPUP_HEIGHT)

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

            # Label 
            list_name_label = tk.Label(list_name_frame, text="Name:", bg=POPUP_BG_COLOR, font=FONT_SMALL)
            list_name_label.pack(anchor="w", padx=5)

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
            messagebox.showinfo("Success", "Note uploaded successfully!")
            
            # Update the list button after submitting the note
            self.app.update_list_button()
            
            self.close_popup()
        else:
            messagebox.showerror("Error", "Please enter a name for the note.")

    # Method to close the popup
    def close_popup(self):
        if self.popup_window:
            self.popup_window.destroy()
            self.popup_window = None

    def pick_date(self):
        self.pick_date_popup = tk.Toplevel(self.root)
        self.pick_date_popup.configure(bg=POPUP_BG_COLOR)

        # Reset the selected day button reference to None
        self.selected_day_button = None  # Reset to prevent referencing a destroyed button

        # Configure the grid for the popup window to align everything to the left
        self.pick_date_popup.grid_columnconfigure(0, weight=1)

        # Title Label 
        title_label = tk.Label(
            self.pick_date_popup, 
            text="Week", 
            font=FONT_LARGE, 
            bg=POPUP_BG_COLOR, 
            fg=PICK_DATE_TEXT_COLOR
        )
        title_label.grid(row=0, column=0, sticky='w', padx=10, pady=5)  # Align to left

        # Days of the week
        days_frame = tk.Frame(self.pick_date_popup, bg=POPUP_BG_COLOR)
        days_frame.grid(row=1, column=0, padx=10, pady=5, sticky='w')  # Align left
        days_of_week = ["Su", "Mo", "Tu", "We", "Th", "Fr", "Sa"]
        
        for i, day in enumerate(days_of_week):
            tk.Label(
                days_frame, 
                text=day, 
                bg="white", 
                fg=PICK_DATE_TEXT_COLOR, 
                font=FONT_MEDIUM
            ).grid(row=0, column=i, padx=5, pady=5, sticky='w')

        def select_day(button, day):
            if self.selected_day_button:
                self.selected_day_button.config(bg=POPUP_BG_COLOR)
            button.config(bg=BUTTON_COLOR)
            self.selected_day_button = button
            self.selected_day = day
            print(f"Selected day: {day}")

        for i in range(1, 8):
            day_button = tk.Button(
                days_frame, 
                text=str(i), 
                bg=POPUP_BG_COLOR, 
                fg=PICK_DATE_TEXT_COLOR,
                font=FONT_MEDIUM, 
                width=2, 
                height=1, 
                borderwidth=0,       
                highlightthickness=0  
            )
            day_button.grid(row=1, column=i-1, padx=5, pady=5)
            day_button.config(command=lambda b=i, btn=day_button: select_day(btn, b))

        # Time selection frame with icon and time dropdown
        time_frame = tk.Frame(self.pick_date_popup, bg=POPUP_BG_COLOR)
        time_frame.grid(row=2, column=0, padx=10, pady=5, sticky='w')

        # Label for the 'End' next to the combobox
        tk.Label(
            time_frame, 
            text="End", 
            bg=POPUP_BG_COLOR, 
            fg=PICK_DATE_TEXT_COLOR, 
            font=FONT_MEDIUM
        ).grid(row=0, column=0, padx=(5, 0), sticky='w')
        
        # Custom frame to hold the Combobox and icon together
        combobox_with_icon_frame = tk.Frame(time_frame, bg=POPUP_BG_COLOR)
        combobox_with_icon_frame.grid(row=0, column=2, padx=0, pady=5)

        # Time icon (loaded from file)
        time_icon_image = Image.open(TIME_ICON)
        time_icon_image = time_icon_image.resize((20, 20), Image.LANCZOS)
        time_icon_photo = ImageTk.PhotoImage(time_icon_image)
        
        # Create a button for the time icon and place it next to the combobox
        time_icon_button = tk.Button(
            combobox_with_icon_frame, 
            image=time_icon_photo, 
            bg=POPUP_BG_COLOR, 
            relief="flat", 
            bd=0
        )
        time_icon_button.grid(row=0, column=1, padx=(0, 5))

        # Define a custom style for the Combobox
        style = ttk.Style()
        style.configure("TCombobox", foreground=PICK_DATE_PREFILLED_COLOR, background="white")  

        # Create the Combobox with the custom style
        self.End_time_combobox = ttk.Combobox(
            combobox_with_icon_frame, 
            values=TIME_OPTIONS, 
            font=FONT_MEDIUM, 
            width=8, 
            style="TCombobox"
        )
        self.End_time_combobox.grid(row=0, column=0, padx=(10, 5))
        self.End_time_combobox.set("12:00")

        # Keep a reference to the image to prevent garbage collection
        time_icon_button.image = time_icon_photo

        # Confirm Button (use grid)
        confirm_button = tk.Button(
            self.pick_date_popup, 
            text="Confirm", 
            bg=BUTTON_COLOR, 
            fg="white", 
            font=FONT_MEDIUM, 
            relief="flat", 
            command=self.confirm_selection
        )
        confirm_button.grid(row=3, column=0, pady=10, padx=10, sticky='e')  

    def confirm_selection(self):
        # Retrieve the selected time from the Combobox
        self.selected_time = self.End_time_combobox.get()  # Get time from Combobox

        if self.selected_day is not None and self.selected_time:
            # Get the current date and time
            current_time = datetime.now()
            # Get the current day of the week 
            current_day = current_time.weekday()
            
            # Create a datetime object for the selected day and time
            selected_datetime = current_time.replace(hour=int(self.selected_time.split(':')[0]), 
                                                    minute=int(self.selected_time.split(':')[1]), 
                                                    second=0, 
                                                    microsecond=0)

            # Check if the selected day is today
            if self.selected_day == current_day:
                # If it's today, ensure the selected time is later than the current time
                if selected_datetime <= current_time:
                    print(current_time)
                    messagebox.showwarning("Time Error", "Please select a time later than the current time.")
                    return

            # Store or use the selected day and time as needed
            print(f"Selected day: {self.selected_day}, Time: {self.selected_time}")

            # Update the Choose Date button text
            day_names = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
            day_text = day_names[self.selected_day - 1]
            self.choose_date_button.config(text=f"{day_text} {self.selected_time}")
            
            # Optionally, store it in the app or a variable
            self.app.saved_end_value = f"Day: {self.selected_day}, Time: {self.selected_time}" 
            
            self.close_pick_date_popup()  # Close the pick date popup
        else:
            messagebox.showwarning("Selection Error", "Please select both a day and a time.")

    def close_pick_date_popup(self):
        if self.pick_date_popup:
            self.pick_date_popup.destroy()
            self.pick_date_popup = None