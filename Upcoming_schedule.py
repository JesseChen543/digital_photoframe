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
from collections import defaultdict

class ViewSchedulePopup:
    """
    A class to create and manage a popup window displaying upcoming schedule items.

    This class fetches user events and family information from a remote API,
    and displays them in a scrollable window with various details for each event.
    """

    def __init__(self, root, app, user_id):
        """
        Initialize the ViewSchedulePopup.

        Args:
            root (tk.Tk): The root window of the application.
            app: The main application instance.
            user_id (int): The ID of the current user.
        """
        self.root = root
        self.app = app
        self.user_id = user_id
        self.popup_window = None
        self.user_events = {}

    def get_family_icons(self):
        """Fetch family icons from the API."""
        url = f"https://deco3801-foundjesse.uqcloud.net/restapi/family.php?user={self.user_id}"
        try:
            response = requests.get(url)
            response.raise_for_status()
            family_data = response.json()
            
            # Use a set to automatically remove duplicates
            family_icons = set()
            for member in family_data:
                if 'icon' in member and member['icon']:
                    family_icons.add(member['icon'])
            
            # Convert set back to list before returning
            return list(family_icons)
        except requests.RequestException as e:
            print(f"Error fetching family data: {e}")
        except ValueError as e:
            print(f"Error parsing family JSON: {e}")
        
        # Return an empty list if there was an error
        return []

    def get_attendee_info(self, event_id):
        """Fetch attendee information (id and icon) for a specific event."""
        url = f"https://deco3801-foundjesse.uqcloud.net/restapi/special_user.php?special_user={self.user_id}"
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            
            attendee_info = {item['attending_user']: item['icon'] for item in data if item['event_id'] == event_id}
            return attendee_info
        except requests.RequestException as e:
            print(f"Error fetching attendee data: {e}")
        except ValueError as e:
            print(f"Error parsing attendee JSON: {e}")
        except KeyError as e:
            print(f"Missing key in attendee data: {e}")
        return {}

    def get_user_events(self):
        """Fetch user events from the API and populate the user_events dictionary."""
        url = f"https://deco3801-foundjesse.uqcloud.net/restapi/special_user.php?special_user={self.user_id}"
        
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            
            events_dict = defaultdict(lambda: defaultdict(list))
            
            for event in data:
                event_id = event['event_id']
                
                # If event_id not in events_dict, create a new dictionary for the event
                if event_id not in events_dict:
                    events_dict[event_id] = {
                        'event_id': event_id,
                        'event_name': event['event_name'],
                        'location': event['location'],
                        'description': event['description'],
                        'start_time': event['start_time'],
                        'end_time': event['end_time'],
                        'story': event['story'],
                        'privacy': event['privacy'],
                        'family_icons': self.get_family_icons(),
                        'attendees': self.get_attendee_info(event_id)
                    }
            
            self.user_events = dict(events_dict)
            self.populate_schedule_items()
        
        except requests.RequestException as e:
            print(f"Error fetching data: {e}")
        except ValueError as e:
            print(f"Error parsing JSON: {e}")
            
    def populate_schedule_items(self):
        """Create schedule items for each event in user_events."""
        current_time = datetime.now()
        for event_id, item in self.user_events.items():
            # Parse the end time
            end_time = datetime.strptime(item['end_time'], "%Y-%m-%d %H:%M:%S")
            
            # Only create schedule item if privacy is "Not Private" and end time is not earlier than current time
            if item['privacy'] == "Not Private" and end_time >= current_time:
                self.add_schedule_item(
                    event_id,  # Add event_id here
                    item['event_name'],
                    item['start_time'],
                    item['end_time'],
                    item.get('location', 'No location'),
                    item.get('description', ''),
                    item.get('story', ''),
                    item.get('family_icons', []),
                    item.get('attendees', {})
                )

    def show_schedules(self):
        """Create and display the popup window with schedule items."""
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
            self.get_user_events()

    def close_popup(self):
        """Close the popup window."""
        if self.popup_window:
            self.popup_window.destroy()
            self.popup_window = None

    def add_schedule_item(self, event_id, title, start_time, end_time, location, description, story, family_icons, attendees):
        """
        Add a schedule item to the scrollable frame.

        Args:
            title (str): The title of the event.
            start_time (str): The start time of the event.
            end_time (str): The end time of the event.
            location (str): The location of the event.
            description (str): The description of the event.
            story (str): The story or image associated with the event.
            family_icons (list): List of family member icons.
            attendees (list): List of attendee information.
        """
        fixed_width = POPUP_WIDTH - 30  
        item_frame = Frame(
            self.scrollable_frame,
            bg="white",
            width=fixed_width,
            borderwidth=1,
            relief="solid"
        )
        item_frame.pack(fill="x", padx=10, pady=5)
        item_frame.pack_propagate(False)  # Prevent the frame from resizing based on its content

        # Use grid layout for better control
        item_frame.grid_columnconfigure(0, weight=1)
        item_frame.grid_columnconfigure(1, minsize=100)  # Width for the image column

        # Adjust label width to fit within the fixed frame width
        label_wrap_width = fixed_width - 120  # Subtract image and padding widths

        # Add title, start time, end time, location, and description labels
        self._add_event_details(item_frame, title, start_time, end_time, location, description, label_wrap_width)

        # Add attendee icons
        self._add_family_icons(item_frame, family_icons, attendees, event_id)

        # Add event image
        self._add_event_image(item_frame, story)

    def _add_event_details(self, item_frame, title, start_time, end_time, location, description, label_wrap_width):
        """Helper method to add event details to the item frame."""
        # Title
        Label(
            item_frame,
            text=title,
            font=FONT_MEDIUM,
            bg="white",
            anchor="w",
            wraplength=label_wrap_width
        ).grid(row=0, column=0, sticky="w", padx=5, pady=(5, 0))

        # Start Time
        formatted_start_time = self.format_date_time(start_time)
        Label(
            item_frame,
            text=f"Start: {formatted_start_time}",
            font=FONT_SMALL,
            fg="gray",
            bg="white",
            anchor="w",
            wraplength=label_wrap_width
        ).grid(row=1, column=0, sticky="w", padx=5)

        # End Time
        formatted_end_time = self.format_date_time(end_time)
        Label(
            item_frame,
            text=f"End: {formatted_end_time}",
            font=FONT_SMALL,
            fg="gray",
            bg="white",
            anchor="w",
            wraplength=label_wrap_width
        ).grid(row=2, column=0, sticky="w", padx=5)

        # Location
        Label(
            item_frame,
            text=f"Location: {location if location else 'No location'}",
            font=FONT_SMALL,
            fg="gray",
            bg="white",
            anchor="w",
            wraplength=label_wrap_width
        ).grid(row=3, column=0, sticky="w", padx=5)

        # Description
        Label(
            item_frame,
            text=description,
            font=FONT_SMALL,
            bg="white",
            anchor="w",
            wraplength=label_wrap_width,
            justify="left"
        ).grid(row=4, column=0, sticky="w", padx=5, pady=(2, 0))

    def _add_family_icons(self, item_frame, family_icons, attendees, event_id):
        """Helper method to add family icons to the item frame."""
        attendees_frame = Frame(item_frame, bg="white")
        attendees_frame.grid(row=5, column=0, sticky="w", padx=5, pady=(0, 5))

        for icon_url in family_icons:
            try:
                response = requests.get(icon_url)
                img = Image.open(BytesIO(response.content))
                img = img.resize((20, 20), Image.LANCZOS)

                # Check if this icon is in the attendees dictionary values
                is_attendee = icon_url in attendees.values()

                if is_attendee:
                    img = self._add_green_tick(img)
                
                photo = ImageTk.PhotoImage(img)
                label = Label(attendees_frame, image=photo, bg="white")
                label.image = photo
                label.pack(side="left", padx=(0, 1), pady=0)

                # Bind click event to the label
                label.bind("<Button-1>", lambda e, url=icon_url, eid=event_id: self._on_family_icon_click(e, url, eid))
            except Exception as e:
                print(f"Error loading family icon image: {e}")

    def _add_green_tick(self, img):
        """Add green tick to the image."""
        enhancer = ImageEnhance.Brightness(img)
        img = enhancer.enhance(0.5)

        # Open TICK_ICON image
        tick_img = Image.open(TICK_ICON)
        tick_img = tick_img.resize((10, 10), Image.LANCZOS)

        # Calculate center coordinates
        x = (img.width - tick_img.width) // 2
        y = (img.height - tick_img.height) // 2

        # Paste tick_img onto img at center (with transparency mask)
        img.paste(tick_img, (x, y), tick_img)
        return img

    def _on_family_icon_click(self, event, icon_url, event_id):
        """Handle click event on family icons."""
        print(f"Clicked icon URL: {icon_url}")
        print(f"Event ID: {event_id}")
        print(f"Family icons: {self.user_events[event_id]['family_icons']}")
        print(f"Attendees: {self.user_events[event_id]['attendees']}")

        attendees = self.user_events[event_id]['attendees']
        if icon_url in attendees.values():
            # This is an attending family member, remove them from the event
            user_id = next(uid for uid, icon in attendees.items() if icon == icon_url)
            success = self._remove_user_from_event(event_id, user_id)
            
            if success:
                # Remove the green tick from the icon
                img = Image.open(BytesIO(requests.get(icon_url).content))
                img = img.resize((20, 20), Image.LANCZOS)
                photo = ImageTk.PhotoImage(img)
                event.widget.configure(image=photo)
                event.widget.image = photo  # Keep a reference

                # Remove the attendee info from the event's attendees dict
                del self.user_events[event_id]['attendees'][user_id]
                
                print(f"Removed user {user_id} with icon {icon_url} from event {event_id}")
            else:
                print(f"Failed to remove user with icon {icon_url} from event {event_id}")
        else:
            # This is a non-attending family member, add them to the event
            user_id = self.get_user_id_from_icon(icon_url)

            if user_id is not None:
                success = self._add_user_to_event(event_id, user_id)
                
                if success:
                    # Update the icon with green tick
                    img = Image.open(BytesIO(requests.get(icon_url).content))
                    img = img.resize((20, 20), Image.LANCZOS)
                    img = self._add_green_tick(img)
                    photo = ImageTk.PhotoImage(img)
                    event.widget.configure(image=photo)
                    event.widget.image = photo  # Keep a reference

                    # Add the attendee info to the event's attendees dict
                    self.user_events[event_id]['attendees'][user_id] = icon_url
                    
                    print(f"Added user {user_id} with icon {icon_url} to event {event_id}")
                else:
                    print(f"Failed to add user with icon {icon_url} to event {event_id}")
            else:
                print(f"Could not find user ID for icon: {icon_url}")

    def _remove_user_from_event(self, event_id, attending_user):
        """Remove user from the event in the database."""
        url = "https://deco3801-foundjesse.uqcloud.net/restapi/special_user.php"
        data = {
            "event": int(event_id),
            "attending_user": int(attending_user)
        }
        
        try:
            response = requests.delete(url, json=data)
            if response.status_code != 200:
                print(f"Server error occurred: {response.text}")
                return False
            result = response.json()
            print(result['message'])  # Print the message from the API
            return True
        except requests.RequestException as e:
            print(f"Error removing user from event: {e}")
            return False
        except ValueError as e:
            print(f"Error parsing API response: {e}")
            return False

    def _add_user_to_event(self, event_id, attending_user):
        """Add user to the event in the database."""
        url = "https://deco3801-foundjesse.uqcloud.net/restapi/special_user.php"
        data = {
            "event": int(event_id),
            "attending_user": int(attending_user)
        }
        
        try:
            response = requests.post(url, json=data)
            if response.status_code != 201:
                print(f"Server error occurred: {response.text}")
                return False
            result = response.json()
            print(result['message'])  # Print the message from the API
            return True
        except requests.RequestException as e:
            print(f"Error adding user to event: {e}")
            return False
        except ValueError as e:
            print(f"Error parsing API response: {e}")
            return False

    def _add_event_image(self, item_frame, story):
        """Helper method to add event image to the item frame."""
        try:
            if story and isinstance(story, str):
                # if there is an url, fetch the image from the url
                if story.startswith('http'):
                    response = requests.get(story)
                    img = Image.open(BytesIO(response.content))
                # if there is no url, open the image from the local folder
                else:
                    img = Image.open(story)
            #
            else:
                img = Image.open(SCHEDULE_PICTURE)

            # Ensure the image fits within the fixed item_frame width
            img = img.resize((100, 120), Image.LANCZOS)  
            photo = ImageTk.PhotoImage(img)
            image_label = Label(item_frame, image=photo, bg="white")
            image_label.image = photo
            image_label.grid(
                row=0,
                column=1,
                rowspan=6,
                padx=5,
                pady=5,
                sticky="ne"
            )
        except Exception as e:
            print(f"Error loading image: {e}")

    def format_date_time(self, date_time_str):
        # Parse the datetime string
        dt = datetime.strptime(date_time_str, "%Y-%m-%d %H:%M:%S")
        # Format it as desired
        return dt.strftime("%d/%m/%Y %H:%M")

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    def get_user_id_from_icon(self, clicked_icon):
        """Get user_id associated with the clicked icon URL."""
        url = f"https://deco3801-foundjesse.uqcloud.net/restapi/special_user.php?special_user={self.user_id}"
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            
            for event in data:
                if event['icon'] == clicked_icon:
                    return event['attending_user']
            
            print(f"No user found with icon URL: {clicked_icon}")
            return None
        except requests.RequestException as e:
            print(f"Error fetching user data: {e}")
        except ValueError as e:
            print(f"Error parsing user JSON: {e}")
        
        return None

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()  # Hide the main root window if you only want the popup to show
    app = type('', (), {})()
    schedule_popup = ViewSchedulePopup(root, app, 2)
    schedule_popup.show_schedules()
    root.mainloop()