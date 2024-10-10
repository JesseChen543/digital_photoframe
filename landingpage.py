import tkinter as tk
from tkinter import PhotoImage
from PIL import Image, ImageTk
from constant import *
from QRCodePage import QRCodePage
import time 
import threading
from photoframe import PhotoFrameApp

class SplashScreenApp:
    """
    A class to create and manage the splash screen (landing page) of the InSync application.

    This class sets up the initial screen that users see when launching the app,
    featuring the InSync logo, title, and a prompt to click anywhere to start.
    It also handles the transition to the QR Code page after user interaction.
    """

    def __init__(self, root):
        """
        Initialize the SplashScreenApp.

        Args:
            root (tk.Tk): The root window of the application.
        """
        self.root = root
        self.root.title("InSync")
        
        # Set full screen size and background color
        self.root.geometry(f"{SCREEN_WIDTH}x{SCREEN_HEIGHT}")
        self.root.configure(bg=LANDING_BG_COLOR)

        # Create the main layout
        self._create_layout()

        # Bind click event to the entire window
        self.root.bind("<Button-1>", self.start_action)

    def _create_layout(self):
        """Create and set up the layout for the splash screen."""
        # Create a frame to hold both the logo and the title
        title_frame = tk.Frame(self.root, bg=LANDING_BG_COLOR)
        title_frame.pack(expand=True, anchor="center")  # Center both horizontally and vertically

        # Create an inner frame for horizontal alignment of logo and title
        inner_frame = tk.Frame(title_frame, bg=LANDING_BG_COLOR)
        inner_frame.pack()

        # Add logo to the inner frame
        self._add_logo(inner_frame)

        # Add title to the inner frame
        self._add_title(inner_frame)

        # Add bottom label
        self._add_bottom_label()

    def _add_logo(self, parent_frame):
        """Add the InSync logo to the given frame."""
        # Load and resize logo image
        logo_img = Image.open(LOGO_IMAGE_PATH)
        logo_img = logo_img.resize((84, 88), Image.LANCZOS)
        logo_image = ImageTk.PhotoImage(logo_img)

        # Create a label for the logo image and place it inside the parent frame
        logo_label = tk.Label(parent_frame, image=logo_image, bg=LANDING_BG_COLOR)
        logo_label.image = logo_image  # Keep a reference to prevent garbage collection
        logo_label.pack(side="left", padx=10)

    def _add_title(self, parent_frame):
        """Add the InSync title to the given frame."""
        # Title Label using Pacifico font
        title_label = tk.Label(parent_frame, text="InSync", font=FONT_LOGO, bg=LANDING_BG_COLOR, fg=LANDING_FG_COLOR)
        title_label.pack(side="left", padx=10)

    def _add_bottom_label(self):
        """Add the 'Click anywhere to start' label at the bottom of the window."""
        bottom_label = tk.Label(self.root, text="Click anywhere to start", font=FONT_LANDING, bg=LANDING_BG_COLOR, fg=LANDING_FG_COLOR)
        bottom_label.pack(side="bottom", pady=20)

    def start_action(self, event):
        """
        Handle the click event on the splash screen.

        This method shows a loading label and initiates the transition to the QR Code page.

        Args:
            event: The click event (not used but required for event binding).
        """
        # Show loading label
        loading_label = tk.Label(self.root, text="Loading...", font=FONT_LANDING, bg=LANDING_BG_COLOR, fg=LANDING_FG_COLOR)
        loading_label.pack()

        # Run the API call on a separate thread
        threading.Thread(target=self.load_qr_page).start()

    def load_qr_page(self):
        """
        Simulate an API call and trigger the opening of the QR Code page.

        This method runs in a separate thread to prevent UI freezing.
        """
        # Simulate API call delay
        time.sleep(2)  
        # After the API call is complete, open the QR Code page
        self.root.after(0, self.open_qr_page)

    def open_qr_page(self):
        """
        Open the QR Code page in a new window.
        """
        self.root.destroy()  # Close the current window
        new_root = tk.Tk()  # Create a new root window
        QRCodePage(new_root)  # Create the QRCodePage without passing a callback
        new_root.mainloop()  # Start the main loop for the new window

if __name__ == "__main__":
    root = tk.Tk()
    app = SplashScreenApp(root)
    root.mainloop()
