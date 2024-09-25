import tkinter as tk
from tkinter import ttk, Frame
from tkinter.simpledialog import askstring
from PIL import Image, ImageTk, ImageDraw
import datetime
from datetime import datetime
from tkcalendar import Calendar  
from tkinter import ttk, messagebox

# Import constants from config.py
from constant import SCREEN_WIDTH, SCREEN_HEIGHT, LOGO_IMAGE_PATH, ICON_IMAGE_PATH, BACKGROUND_IMAGE_PATH, \
                   BACKGROUND_COLOR, BUTTON_COLOR, BUTTON_TEXT_COLOR, FONT_TITLE, FONT_BUTTON, FONT_ENTRY, TIME_OPTIONS

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

        # Set screen dimensions
        self.screen_width = SCREEN_WIDTH
        self.screen_height = SCREEN_HEIGHT

        # Load and display the full-screen image
        image_path = BACKGROUND_IMAGE_PATH
        image = Image.open(image_path)
        image = image.resize((self.screen_width, self.screen_height), Image.LANCZOS)
        bg_image = ImageTk.PhotoImage(image)

        bg_label = tk.Label(self.root, image=bg_image)
        bg_label.image = bg_image
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        icon_image_path = ICON_IMAGE_PATH
        # Make the icon round
        round_icon = self.make_round_image(icon_image_path)
        icon_image = ImageTk.PhotoImage(round_icon)

        icon_button = tk.Button(self.root, image=icon_image, command=self.show_note, borderwidth=0)
        icon_button.image = icon_image
        icon_button.place(x=self.screen_width - 60, y=10)

        # Initialize selected_day_button as None
        self.selected_day_button = None  

        self.root.geometry(f"{self.screen_width}x{self.screen_height}")
        self.root.bind('<Escape>', self.quit_app)

    # Function to make the image round with transparency (not functional yet)
    def make_round_image(self, image_path, size=(30, 30)):
        image = Image.open(image_path).resize(size, Image.LANCZOS)
        image = image.convert("RGBA")
        mask = Image.new('L', size, 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0) + size, fill=255)
        result = Image.new("RGBA", size)
        result.paste(image, (0, 0), mask)
        return result

    def show_note(self):
        if self.popup_window is None or not self.popup_window.winfo_exists():
            self.popup_window = tk.Toplevel(self.root)
            self.popup_window.configure(bg='white')
            popup_width = 290
            popup_height = 390
            self.popup_window.geometry(f"{popup_width}x{popup_height}")

            main_frame = Frame(self.popup_window, bg="white")
            main_frame.pack(fill="both", expand=True)

            title_close_frame = Frame(main_frame, bg="white")
            title_close_frame.pack(fill="x")

            title_label = tk.Label(title_close_frame, text="Write a Note", font=FONT_TITLE, bg="white")
            title_label.pack(side="left", padx=10, fill="x")

            separator = ttk.Separator(main_frame, orient='horizontal')
            separator.pack(fill='x', pady=5)
            
            inner_frame = Frame(main_frame, bg="white")
            inner_frame.pack(fill="both", expand=True, padx=20, pady=20)

            list_name_label = tk.Label(inner_frame, text="Name:", bg="white", font=FONT_ENTRY)
            list_name_label.grid(row=0, column=0, sticky='w', padx=5, pady=5)
            list_name_entry = tk.Entry(inner_frame, font=FONT_ENTRY, relief="solid", bd=1)
            list_name_entry.grid(row=0, column=1, sticky='ew', padx=5, pady=5)
            list_name_entry.insert(0, self.saved_list_name)

            end_label = tk.Label(inner_frame, text="End:", bg="white", font=FONT_ENTRY)
            end_label.grid(row=1, column=0, sticky='w', padx=5, pady=5)
            choose_date_button = tk.Button(inner_frame, text="Choose Date", command=self.pick_date)
            choose_date_button.grid(row=1, column=1, sticky="e", padx=5, pady=0)

            note_label = tk.Label(inner_frame, text="Note:", bg="white", font=FONT_ENTRY)
            note_label.grid(row=2, column=0, sticky='nw', padx=5, pady=5)
            note_entry = tk.Text(inner_frame, font=FONT_ENTRY, relief="solid", bd=1, height=5)
            note_entry.grid(row=2, column=1, sticky='nsew', padx=5, pady=5)
            note_entry.insert("1.0", self.saved_note_value)

            submit_button = tk.Button(self.popup_window, text="Upload", bg=BUTTON_COLOR, fg=BUTTON_TEXT_COLOR, font=FONT_BUTTON, relief="flat")
            submit_button.pack(anchor="e", padx=10, pady=10)

            inner_frame.grid_columnconfigure(1, weight=1)
            inner_frame.grid_rowconfigure(2, weight=1)

    def pick_date(self):
        popup = tk.Toplevel(self.root)
        popup.geometry("270x206")
        popup.configure(bg='white')
        title_label = tk.Label(popup, text="Week", font=("Helvetica", 14), bg="white")
        title_label.pack(pady=5)

        days_frame = tk.Frame(popup, bg="white")
        days_frame.pack()
        days_of_week = ["Su", "Mo", "Tu", "We", "Th", "Fr", "Sa"]
        for i, day in enumerate(days_of_week):
            tk.Label(days_frame, text=day, bg="white", font=("Helvetica", 10)).grid(row=0, column=i, padx=5, pady=5)

        def select_day(button, day):
            if self.selected_day_button:
                self.selected_day_button.config(bg="white")
            button.config(bg=BUTTON_COLOR)
            self.selected_day_button = button
            print(f"Selected day: {day}")

        for i in range(1, 8):
            day_button = tk.Button(days_frame, text=str(i), bg="white", font=("Helvetica", 10), width=2, height=1)
            day_button.grid(row=1, column=i-1, padx=5, pady=5)
            day_button.config(command=lambda b=i, btn=day_button: select_day(btn, b))

        time_frame = tk.Frame(popup, bg="white")
        time_frame.pack(pady=5)

        tk.Label(time_frame, text="Time", bg="white", font=("Helvetica", 10)).grid(row=0, column=0, padx=5)

        start_time_combobox = ttk.Combobox(time_frame, values=TIME_OPTIONS, font=("Helvetica", 10), width=5)
        start_time_combobox.grid(row=0, column=1, padx=5)
        start_time_combobox.set("08:00")

        tk.Label(time_frame, text="to", bg="white", font=("Helvetica", 10)).grid(row=0, column=2, padx=5)

        end_time_combobox = ttk.Combobox(time_frame, values=TIME_OPTIONS, font=("Helvetica", 10), width=5)
        end_time_combobox.grid(row=0, column=3, padx=5)
        end_time_combobox.set("12:00")

        def validate_time():
            start_time = start_time_combobox.get()
            end_time = end_time_combobox.get()
            fmt = "%H:%M"
            try:
                start_dt = datetime.strptime(start_time, fmt)
                end_dt = datetime.strptime(end_time, fmt)
                if start_dt >= end_dt:
                    messagebox.showerror("Invalid Time", "Start time cannot be later than or equal to the end time.")
                else:
                    popup.destroy()
            except ValueError:
                messagebox.showerror("Invalid Input", "Please select valid times.")

        confirm_button = tk.Button(popup, text="Confirm", bg=BUTTON_COLOR, fg=BUTTON_TEXT_COLOR, font=FONT_BUTTON, relief="flat", command=validate_time)
        confirm_button.pack(padx=5, pady=10, anchor="e")

    def quit_app(self, event=None):
        self.root.quit()

if __name__ == "__main__":
    root = tk.Tk()
    app = PhotoFrameApp(root)
    root.mainloop()
