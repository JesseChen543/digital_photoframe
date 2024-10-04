import tkinter as tk
from tkinter import Frame, Label, Canvas, Scrollbar
from PIL import Image, ImageTk
from constant import *
from PopupHeader import PopupHeader
from utils import center_window_parent
import requests
import json
from datetime import datetime
from io import BytesIO

class ViewSchedulePopup:
    def __init__(self, root, app):
        self.root = root
        self.app = app
        self.popup_window = None

    def show_schedules(self):
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

            # Create a canvas with scrollbar for the schedule items
            self.canvas = Canvas(self.main_frame, bg=POPUP_BG_COLOR)
            self.scrollbar = Scrollbar(self.main_frame, orient="vertical", command=self.canvas.yview)
            self.scrollable_frame = Frame(self.canvas, bg=POPUP_BG_COLOR)

            self.scrollable_frame.bind(
                "<Configure>",
                lambda e: self.canvas.configure(
                    scrollregion=self.canvas.bbox("all")
                )
            )

            self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
            self.canvas.configure(yscrollcommand=self.scrollbar.set)

            self.canvas.pack(side="left", fill="both", expand=True)
            self.scrollbar.pack(side="right", fill="y")

            # Fetch and add schedule items
            self.fetch_schedule_items()

    def close_popup(self):
        if self.popup_window:
            self.popup_window.destroy()
            self.popup_window = None

    def fetch_schedule_items(self):
        url = "https://deco3801-foundjesse.uqcloud.net/restapi/event.php?user=1"
        try:
            response = requests.get(url)
            data = response.json()
            current_time = datetime.now()
            for item in data:
                # Parse the end time
                end_time = datetime.strptime(item['end_time'], "%Y-%m-%d %H:%M:%S")
                
                # Only create schedule item if privacy is "Not Private" and end time is not earlier than current time
                if item['privacy'] == "Not Private" and end_time <= current_time:
                    self.add_schedule_item(
                        item['event_name'],
                        item['start_time'],
                        item.get('location', 'No location'),
                        item.get('description', ''),
                        item.get('story', ''),
                        [MEMBER_ICON] * 4 
                    )
        except Exception as e:
            print(f"Error fetching schedule data: {e}")

    def add_schedule_item(self, title, date_time, location, description, story, attendees):
        item_frame = Frame(self.scrollable_frame, bg="white", bd=1, relief="solid")
        item_frame.pack(fill="x", padx=5, pady=3)  # Reduced vertical padding

        # Use grid layout for better control
        item_frame.grid_columnconfigure(0, weight=1)
        item_frame.grid_columnconfigure(1, minsize=60)  # Reduced width for image column

        # Title
        Label(item_frame, text=title, font=FONT_SMALL, bg="white", anchor="w").grid(row=0, column=0, sticky="w", padx=5, pady=(5, 0))

        # Date and Time
        formatted_date_time = self.format_date_time(date_time)
        Label(item_frame, text=formatted_date_time, font=FONT_SMALL, fg="gray", bg="white", anchor="w").grid(row=1, column=0, sticky="w", padx=5)

        # Location
        Label(item_frame, text=location if location else "No location", font=FONT_SMALL, fg="gray", bg="white", anchor="w").grid(row=2, column=0, sticky="w", padx=5)

        # Description
        description_label = Label(item_frame, text=description, font=FONT_SMALL, bg="white", anchor="w", wraplength=POPUP_WIDTH-100, justify="left")
        description_label.grid(row=3, column=0, sticky="w", padx=5, pady=(2, 0))

        # Attendees
        attendees_frame = Frame(item_frame, bg="white")
        attendees_frame.grid(row=4, column=0, sticky="w", padx=5, pady=(2, 5))

        for i, attendee in enumerate(attendees):
            try:
                img = Image.open(attendee)
                img = img.resize((20, 20), Image.LANCZOS)  
                photo = ImageTk.PhotoImage(img)
                label = Label(attendees_frame, image=photo, bg="white")
                label.image = photo
                label.pack(side="left", padx=(0, 2))
            except Exception as e:
                print(f"Error loading attendee image: {e}")

        # Handle image loading (both URL and local file)
        try:
            if story.startswith('http'):
                response = requests.get(story)
                img = Image.open(BytesIO(response.content))
            else:
                img = Image.open(story) if story else Image.open(SCHEDULE_PICTURE)
            
            img = img.resize((100, 100), Image.LANCZOS)  # Fixed size for consistency
            photo = ImageTk.PhotoImage(img)
            image_label = Label(item_frame, image=photo, bg="white")
            image_label.image = photo
            image_label.grid(row=0, column=1, rowspan=5, padx=5, pady=5, sticky="ne")
        except Exception as e:
            print(f"Error loading image: {e}")
          

    def format_date_time(self, date_time_str):
        # Parse the datetime string
        dt = datetime.strptime(date_time_str, "%Y-%m-%d %H:%M:%S")
        # Format it as desired
        return dt.strftime("%d/%m/%Y %H:%M")

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()  # Hide the main root window if you only want the popup to show
    app = type('', (), {})()
    schedule_popup = ViewSchedulePopup(root, app)
    schedule_popup.show_schedules()
    root.mainloop()