import tkinter as tk
from tkinter import ttk, Frame
from tkinter.simpledialog import askstring
from PIL import Image, ImageTk
import datetime
from datetime import datetime
from tkcalendar import Calendar  
from tkinter import ttk, messagebox

class PhotoFrameApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Display with Clickable Icon")

        # Initialize saved inputs
        self.saved_list_name = ""
        self.saved_end_value = ""
        self.saved_note_value = ""
        self.current_date = datetime.now().strftime("%d/%m/%Y")

        # Keep track of the popup window
        self.popup_window = None

        # Screen dimensions in pixels
        self.screen_width = 378
        self.screen_height = 624

        # Load and display the full-screen image
        image_path = "pictures/photoframe3.png"
        image = Image.open(image_path)
        image = image.resize((self.screen_width, self.screen_height), Image.LANCZOS)
        bg_image = ImageTk.PhotoImage(image)

        bg_label = tk.Label(self.root, image=bg_image)
        bg_label.image = bg_image
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        icon_image_path = "pictures/detail_icon.png"
        icon = Image.open(icon_image_path)
        icon = icon.resize((30, 30), Image.LANCZOS)
        icon_image = ImageTk.PhotoImage(icon)

        icon_button = tk.Button(self.root, image=icon_image, command=self.show_popup, borderwidth=0)
        icon_button.image = icon_image
        icon_button.place(x=self.screen_width - 60, y=10)

        # Initialize selected_day_button as None
        self.selected_day_button = None  

        self.root.geometry(f"{self.screen_width}x{self.screen_height}")
        self.root.bind('<Escape>', self.quit_app)

    def show_popup(self):
        if self.popup_window is None or not self.popup_window.winfo_exists():
            self.popup_window = tk.Toplevel(self.root)
            self.popup_window.configure(bg='white')
            popup_width = int(self.screen_width * 0.66)
            popup_height = int(self.screen_height * 0.66)
            self.popup_window.geometry(f"{popup_width}x{popup_height}")

            title_close_frame = Frame(self.popup_window, bg="white")
            title_close_frame.pack(fill="x")

            title_label = tk.Label(title_close_frame, text="Write a Note", font=("Helvetica", 14), bg="white")
            title_label.pack(side="left", padx=10)

            inner_frame = Frame(self.popup_window, bg="white")
            inner_frame.pack(fill="both", expand=True, padx=20, pady=20)

            list_name_label = tk.Label(inner_frame, text="Name:", bg="white", font=("Helvetica", 10))
            list_name_label.grid(row=0, column=0, sticky='w', padx=5, pady=5)
            list_name_entry = tk.Entry(inner_frame, font=("Helvetica", 10), relief="solid", bd=1)
            list_name_entry.grid(row=0, column=1, sticky='ew', padx=5, pady=5)
            list_name_entry.insert(0, self.saved_list_name)

            # Remove end_entry and just use the Choose Date button
            end_label = tk.Label(inner_frame, text="End:", bg="white", font=("Helvetica", 10))
            end_label.grid(row=1, column=0, sticky='w', padx=5, pady=5)
            # Remove the entry and only have the button
            choose_date_button = tk.Button(inner_frame, text="Choose Date", command=self.pick_date)
            choose_date_button.grid(row=1, column=1, sticky="e", padx=5, pady=0)

            note_label = tk.Label(inner_frame, text="Note:", bg="white", font=("Helvetica", 10))
            note_label.grid(row=2, column=0, sticky='nw', padx=5, pady=5)
            note_entry = tk.Text(inner_frame, font=("Helvetica", 10), relief="solid", bd=1, height=5)
            note_entry.grid(row=2, column=1, sticky='nsew', padx=5, pady=5)
            note_entry.insert("1.0", self.saved_note_value)

            submit_button = tk.Button(self.popup_window, text="Upload", bg="#5081FF", fg="white", font=("Helvetica", 10), relief="flat")
            submit_button.pack(pady=10)

            inner_frame.grid_columnconfigure(1, weight=1)
            inner_frame.grid_rowconfigure(2, weight=1)

    # Modify the pick_date function to update the label
    def pick_date(self):
        """Display the date and time picker popup similar to the provided screenshot."""
        popup = tk.Toplevel(self.root)
        popup.geometry("300x250")
        popup.configure(bg='white')

        # Title Label
        title_label = tk.Label(popup, text="Week", font=("Helvetica", 14), bg="white")
        title_label.pack(pady=10)

        # Days of the week grid
        days_frame = tk.Frame(popup, bg="white")
        days_frame.pack()

        days_of_week = ["Su", "Mo", "Tu", "We", "Th", "Fr", "Sa"]
        for i, day in enumerate(days_of_week):
            tk.Label(days_frame, text=day, bg="white", font=("Helvetica", 10)).grid(row=0, column=i, padx=5, pady=5)

        # Function to select the day and change its background color
        def select_day(button, day):
            # Reset the background of the previously selected button
            if self.selected_day_button:
                self.selected_day_button.config(bg="white")

            # Set the new selected day (only changing the background color)
            button.config(bg="#5081FF")  # Keep the text color as default (black)
            self.selected_day_button = button

            # Store the selected day (you can use this variable in your logic)
            print(f"Selected day: {day}")

        # Create buttons for the days of the week (1-7) with click functionality
        for i in range(1, 8):
            day_button = tk.Button(days_frame, text=str(i), bg="white", font=("Helvetica", 10), width=2, height=1)
            day_button.grid(row=1, column=i-1, padx=5, pady=5)
            
            # Correctly bind the day_button in lambda
            day_button.config(command=lambda b=i, btn=day_button: select_day(btn, b))


        # Time selection area
        time_frame = tk.Frame(popup, bg="white")
        time_frame.pack(pady=10)

        # Create a list of times (you can adjust the range as needed)
        time_options = [f"{h:02d}:00" for h in range(0, 24)]  # Generates times from 00:00 to 23:00

        # Time selection area
        time_frame = tk.Frame(popup, bg="white")
        time_frame.pack(pady=10)

        tk.Label(time_frame, text="Time", bg="white", font=("Helvetica", 10)).grid(row=0, column=0, padx=5)

        # Start time combobox
        start_time_combobox = ttk.Combobox(time_frame, values=time_options, font=("Helvetica", 10), width=5)
        start_time_combobox.grid(row=0, column=1, padx=5)
        start_time_combobox.set("08:00")  # Default start time

        # "to" label
        tk.Label(time_frame, text="to", bg="white", font=("Helvetica", 10)).grid(row=0, column=2, padx=5)

        # End time combobox
        end_time_combobox = ttk.Combobox(time_frame, values=time_options, font=("Helvetica", 10), width=5)
        end_time_combobox.grid(row=0, column=3, padx=5)
        end_time_combobox.set("12:00")  # Default end time

        # Time validation function
        def validate_time():
            start_time = start_time_combobox.get()
            end_time = end_time_combobox.get()

            # Convert the time strings into datetime objects for comparison
            fmt = "%H:%M"  # Time format
            try:
                start_dt = datetime.strptime(start_time, fmt)
                end_dt = datetime.strptime(end_time, fmt)

                # Check if start time is later than end time
                if start_dt >= end_dt:
                    # Show an error popup
                    messagebox.showerror("Invalid Time", "Start time cannot be later than or equal to the end time.")
                else:
                    # If valid, show a success message (optional)
                    messagebox.showinfo("Valid Time", "The selected times are valid.")
            except ValueError:
                # Handle the case where the input is not a valid time format
                messagebox.showerror("Invalid Input", "Please select valid times.")

        # Confirm button
        confirm_button = tk.Button(popup, text="Confirm", bg="#5081FF", fg="white", font=("Helvetica", 10), relief="flat", command=validate_time)
        confirm_button.pack(pady=10)

    def quit_app(self, event=None):
        self.root.quit()

if __name__ == "__main__":
    root = tk.Tk()
    app = PhotoFrameApp(root)
    root.mainloop()
