import tkinter as tk
from tkinter import Frame, Label, Canvas, Scrollbar, ttk
from PIL import Image, ImageTk, ImageEnhance
from constant import *
from PopupHeader import PopupHeader
from utils import center_window_parent
import requests
import json
from datetime import datetime
from io import BytesIO

class ViewSchedulePopup:
    def __init__(self, root, app, user_id):
        self.root = root
        self.app = app
        self.user_id = user_id
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

            # Create a frame to contain the canvas and scrollbar with a fixed height
            HEADER_HEIGHT = 50  # Adjust this value based on your actual header height
            content_height = POPUP_HEIGHT - HEADER_HEIGHT

            content_frame = Frame(self.main_frame, bg=POPUP_BG_COLOR, height=content_height)
            content_frame.pack(fill="both", expand=False)
            content_frame.pack_propagate(False)  # Prevent content_frame from resizing to fit its children

            # Create a canvas with scrollbar for the schedule items
            self.canvas = Canvas(content_frame, bg=POPUP_BG_COLOR)
            self.scrollbar = Scrollbar(content_frame, orient="vertical", command=self.canvas.yview)

            self.canvas.configure(yscrollcommand=self.scrollbar.set)
            self.scrollbar.pack(side="right", fill="y")
            self.canvas.pack(side="left", fill="both", expand=True)

            # Create a frame inside the canvas to hold the schedule items
            self.scrollable_frame = Frame(self.canvas, bg=POPUP_BG_COLOR)
            self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

            self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
            # Update the scroll region when the size of the scrollable_frame changes
            self.scrollable_frame.bind(
                "<Configure>",
                lambda e: self.canvas.configure(
                    scrollregion=self.canvas.bbox("all")
                )
            )

            # Fetch and add schedule items
            self.fetch_schedule_items()

    def close_popup(self):
        if self.popup_window:
            self.popup_window.destroy()
            self.popup_window = None

    def fetch_schedule_items(self):
        url = f"https://deco3801-foundjesse.uqcloud.net/restapi/event.php?user={self.user_id}"
        try:
            response = requests.get(url)
            data = response.json()
            current_time = datetime.now()
            for item in data:
                # Parse the end time
                end_time = datetime.strptime(item['end_time'], "%Y-%m-%d %H:%M:%S")
                
                # Only create schedule item if privacy is "Not Private" and end time is not earlier than current time
                if item['privacy'] == "Not Private" and end_time >= current_time:
                    self.add_schedule_item(
                        item['event_name'],
                        item['start_time'],
                        item['end_time'],
                        item.get('location', 'No location'),
                        item.get('description', ''),
                        item.get('story', ''),
                        [MEMBER_ICON] * 4 
                    )
        except Exception as e:
            print(f"Error fetching schedule data: {e}")

    def add_schedule_item(self, title, start_time, end_time, location, description, story, attendees):
        item_frame = Frame(self.scrollable_frame, bg="white", borderwidth=1, relief="solid")
        item_frame.pack(fill="x", padx=5, pady=5)  # Adjust outer padding as needed

        # Use grid layout for better control
        item_frame.grid_columnconfigure(0, weight=1)
        item_frame.grid_columnconfigure(1, minsize=60) 

        # Title
        Label(item_frame, text=title, font=FONT_MEDIUM, bg="white", anchor="w").grid(row=0, column=0, sticky="w", padx=5, pady=(5, 0))

        # Start Time
        formatted_start_time = self.format_date_time(start_time)
        Label(item_frame, text=f"Start: {formatted_start_time}", font=FONT_SMALL, fg="gray", bg="white", anchor="w").grid(row=1, column=0, sticky="w", padx=5)

        # End Time
        formatted_end_time = self.format_date_time(end_time)
        Label(item_frame, text=f"End: {formatted_end_time}", font=FONT_SMALL, fg="gray", bg="white", anchor="w").grid(row=2, column=0, sticky="w", padx=5)

        # Location
        Label(item_frame, text=f"Location: {location if location else 'No location'}", font=FONT_SMALL, fg="gray", bg="white", anchor="w").grid(row=3, column=0, sticky="w", padx=5)

        # Description
        description_label = Label(item_frame, text=description, font=FONT_SMALL, bg="white", anchor="w", wraplength=POPUP_WIDTH-100, justify="left")
        description_label.grid(row=4, column=0, sticky="e", padx=5, pady=(2, 0))

        # Attendees
        attendees_frame = Frame(item_frame, bg="white")
        attendees_frame.grid(row=4, column=0, sticky="e", padx=5, pady=(0, 5)) 

        for i, attendee in enumerate(attendees):
            try:
                # Load attendee image
                img = Image.open(attendee)
                img = img.resize((20, 20), Image.LANCZOS)

                #replace this with the logic to check if the attendee is in the user's friends list (from api)
                if i == 0:
                    # Darken the image
                    enhancer = ImageEnhance.Brightness(img)
                    img = enhancer.enhance(0.5)  # Reduce brightness by 50%

                    # Open TICK_ICON image
                    tick_img = Image.open(TICK_ICON)
                    tick_img = tick_img.resize((10, 10), Image.LANCZOS)  # Adjust size as needed

                    # Calculate center coordinates
                    x = (img.width - tick_img.width) // 2
                    y = (img.height - tick_img.height) // 2

                    # Paste tick_img onto img at center (with transparency mask)
                    img.paste(tick_img, (x, y), tick_img)

                photo = ImageTk.PhotoImage(img)
                label = Label(attendees_frame, image=photo, bg="white")
                label.image = photo
                label.pack(side="left", padx=(0, 1), pady=0)  # No vertical padding
            except Exception as e:
                print(f"Error loading attendee image: {e}")

        # Handle image loading (both URL and local file)
        try:
            if story.startswith('http'):
                response = requests.get(story)
                img = Image.open(BytesIO(response.content))
            else:
                img = Image.open(story) if story else Image.open(SCHEDULE_PICTURE)
            
            img = img.resize((100, 120), Image.LANCZOS)  
            photo = ImageTk.PhotoImage(img)
            image_label = Label(item_frame, image=photo, bg="white")
            image_label.image = photo
            image_label.grid(row=0, column=1, rowspan=6, padx=5, pady=5, sticky="ne")
        except Exception as e:
            print(f"Error loading image: {e}")
          

    def format_date_time(self, date_time_str):
        # Parse the datetime string
        dt = datetime.strptime(date_time_str, "%Y-%m-%d %H:%M:%S")
        # Format it as desired
        return dt.strftime("%d/%m/%Y %H:%M")

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()  # Hide the main root window if you only want the popup to show
    app = type('', (), {})()
    schedule_popup = ViewSchedulePopup(root, app)
    schedule_popup.show_schedules()
    root.mainloop()