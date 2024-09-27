# NotePopup.py
import tkinter as tk
from tkinter import ttk, Frame
from tkinter import messagebox
from datetime import datetime
from PIL import Image, ImageTk
from constant import *

class NotePopup:
    def __init__(self, root, app):
        self.root = root
        self.app = app  # Pass in the main application (PhotoFrameApp)
        self.popup_window = None
        self.selected_day_button = None

    def show_note(self):
        if self.popup_window is None or not self.popup_window.winfo_exists():
            self.popup_window = tk.Toplevel(self.root)
            self.popup_window.configure(bg=POPUP_BG_COLOR)
            self.popup_window.geometry(f"{POPUP_WIDTH}x{POPUP_HEIGHT}")

            main_frame = Frame(self.popup_window, bg=POPUP_BG_COLOR)
            main_frame.pack(fill="both", expand=True)

            title_close_frame = Frame(main_frame, bg=POPUP_BG_COLOR)
            title_close_frame.pack(fill="x")

            title_label = tk.Label(title_close_frame, text="Write a Note", font=FONT_LARGE, bg=POPUP_BG_COLOR)
            title_label.pack(side="left", padx=10, fill="x")

            separator = ttk.Separator(main_frame, orient='horizontal')
            separator.pack(fill='x', pady=5)
            
            inner_frame = Frame(main_frame, bg=POPUP_BG_COLOR)
            inner_frame.pack(fill="both", expand=True, padx=20, pady=20)

            list_name_label = tk.Label(inner_frame, text="Name:", bg=POPUP_BG_COLOR, font=FONT_SMALL)
            list_name_label.grid(row=0, column=0, sticky='w', padx=5, pady=5)
            list_name_entry = tk.Entry(inner_frame, font=FONT_SMALL, relief="solid", bd=1)
            list_name_entry.grid(row=0, column=1, sticky='ew', padx=5, pady=5)
            list_name_entry.insert(0, self.app.saved_list_name)

            end_label = tk.Label(inner_frame, text="End:", bg=POPUP_BG_COLOR, font=FONT_SMALL)
            end_label.grid(row=1, column=0, sticky='w', padx=5, pady=5)
            choose_date_button = tk.Button(inner_frame, text="Choose Date", command=self.pick_date)
            choose_date_button.grid(row=1, column=1, sticky="e", padx=5, pady=0)

            note_label = tk.Label(inner_frame, text="Note:", bg=POPUP_BG_COLOR, font=FONT_SMALL)
            note_label.grid(row=2, column=0, sticky='nw', padx=5, pady=5)
            note_entry = tk.Text(inner_frame, font=FONT_SMALL, relief="solid", bd=1, height=5)
            note_entry.grid(row=2, column=1, sticky='nsew', padx=5, pady=5)
            note_entry.insert("1.0", self.app.saved_note_value)

            submit_button = tk.Button(self.popup_window, text="Upload", bg=BUTTON_COLOR, fg=BUTTON_TEXT_COLOR, font=FONT_MEDIUM, relief="flat")
            submit_button.pack(anchor="e", padx=10, pady=10)

            inner_frame.grid_columnconfigure(1, weight=1)
            inner_frame.grid_rowconfigure(2, weight=1)

    def pick_date(self):
        popup = tk.Toplevel(self.root)
        popup.configure(bg=POPUP_BG_COLOR)

        # Configure the grid for the popup window to align everything to the left
        popup.grid_columnconfigure(0, weight=1)

        # Title Label (Aligned left)
        title_label = tk.Label(popup, text="Week", font=FONT_LARGE, bg=POPUP_BG_COLOR)
        title_label.grid(row=0, column=0, sticky='w', padx=10, pady=5)  # Align to left

        # Days of the week
        days_frame = tk.Frame(popup, bg=POPUP_BG_COLOR)
        days_frame.grid(row=1, column=0, padx=10, pady=5, sticky='w')  # Align left
        days_of_week = ["Su", "Mo", "Tu", "We", "Th", "Fr", "Sa"]
        
        for i, day in enumerate(days_of_week):
            tk.Label(days_frame, text=day, bg="white", font=FONT_MEDIUM).grid(row=0, column=i, padx=5, pady=5, sticky='w')

        def select_day(button, day):
            if self.selected_day_button:
                self.selected_day_button.config(bg=POPUP_BG_COLOR)
            button.config(bg=BUTTON_COLOR)
            self.selected_day_button = button
            print(f"Selected day: {day}")

        for i in range(1, 8):
            day_button = tk.Button(
                days_frame, 
                text=str(i), 
                bg=POPUP_BG_COLOR, 
                font=FONT_MEDIUM, 
                width=2, 
                height=1, 
                borderwidth=0,       
                highlightthickness=0  
            )
            day_button.grid(row=1, column=i-1, padx=5, pady=5)
            day_button.config(command=lambda b=i, btn=day_button: select_day(btn, b))

        # Time selection frame with icon and time dropdown
        time_frame = tk.Frame(popup, bg=POPUP_BG_COLOR)
        time_frame.grid(row=2, column=0, padx=10, pady=5, sticky='w')

        # Custom frame to hold the Combobox and icon together
        combobox_with_icon_frame = tk.Frame(time_frame, bg=POPUP_BG_COLOR)
        combobox_with_icon_frame.grid(row=0, column=2, padx=0, pady=5)

        # Time Combobox
        End_time_combobox = ttk.Combobox(combobox_with_icon_frame, values=TIME_OPTIONS, font=FONT_MEDIUM, width=8)
        End_time_combobox.grid(row=0, column=0, padx=(0, 5))
        End_time_combobox.set("12:00")

        # Time icon (loaded from file)
        time_icon_image = Image.open("pictures/time_logo.png")
        time_icon_image = time_icon_image.resize((20, 20), Image.LANCZOS)
        time_icon_photo = ImageTk.PhotoImage(time_icon_image)

        # Create a button for the time icon and place it next to the combobox
        time_icon_button = tk.Button(combobox_with_icon_frame, image=time_icon_photo, bg=POPUP_BG_COLOR, relief="flat", bd=0)
        time_icon_button.grid(row=0, column=1, padx=(0, 5))

        # Label for the 'End' next to the combobox
        tk.Label(time_frame, text="End", bg=POPUP_BG_COLOR, font=FONT_MEDIUM).grid(row=0, column=0, padx=(5, 0), sticky='w')

        # Confirm Button (use grid)
        confirm_button = tk.Button(popup, text="Confirm", bg=BUTTON_COLOR, fg="white", font=FONT_MEDIUM, relief="flat")
        confirm_button.grid(row=3, column=0, pady=10, padx=10, sticky='e')  

        def validate_time():
            end_time = End_time_combobox.get()
            fmt = "%H:%M"
            try:
                # Get the current system time
                current_time = datetime.now().strftime(fmt)
                current_dt = datetime.strptime(current_time, fmt)
                
                # Convert the selected end time
                end_dt = datetime.strptime(end_time, fmt)
                
                # Validate if the end time is earlier than the current system time
                if end_dt <= current_dt:
                    messagebox.showerror("Invalid Time", "End time cannot be earlier than the current system time.")
                else:
                    popup.destroy()  # Close the popup if valid time
            except ValueError:
                messagebox.showerror("Invalid Input", "Please select valid times.")
