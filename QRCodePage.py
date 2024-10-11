import tkinter as tk
from PIL import Image, ImageTk
import requests
from io import BytesIO
from constant import *
from photoframe import PhotoFrameApp

class QRCodePage:
    """
    A class to display the QR code page for pairing the InSync application.

    This class creates a window showing a QR code and instructions for pairing.
    Clicking anywhere on this window will simulate a successful QR code scan,
    close this window, and open the main PhotoFrameApp as a new window.
    """

    def __init__(self, root, callback=None):
        """
        Initialize the QRCodePage.

        Args:
            root (tk.Tk): The root window of the application.
            callback (function, optional): A function to call after opening PhotoFrameApp.
        """
        self.root = root
        self.callback = callback
        
        # Remove window decorations
        self.root.overrideredirect(True)
        
        # Set full screen size and background color
        self.root.geometry(f"{SCREEN_WIDTH}x{SCREEN_HEIGHT}+0+0")
        self.root.configure(bg=QR_BG_COLOR)

        # Create the layout
        self._create_layout()

        # Bind click event to the entire window
        self.root.bind("<Button-1>", self._on_click)

        # Bind Escape key to close the application
        self.root.bind("<Escape>", lambda e: self.root.quit())

    def _create_layout(self):
        """Create and set up the layout for the QR code page."""
        # Create a frame for title (logo + text)
        title_frame = tk.Frame(self.root, bg=QR_BG_COLOR)
        title_frame.pack(pady=40)

        # Add logo to the title frame
        self._add_logo(title_frame)

        # Add title to the title frame
        self._add_title(title_frame)

        # Fetch and display QR code
        qr_code = self._generate_qr_code()
        qr_label = tk.Label(self.root, image=qr_code, bg=QR_BG_COLOR)
        qr_label.image = qr_code
        qr_label.pack(pady=20)

        # Add instruction label
        self._add_instruction()

    def _add_logo(self, parent_frame):
        """Add the InSync logo to the given frame."""
        logo_img = Image.open(LOGO_IMAGE_PATH)
        logo_img = logo_img.resize((60, 60), Image.LANCZOS)
        logo_image = ImageTk.PhotoImage(logo_img)

        logo_label = tk.Label(parent_frame, image=logo_image, bg=QR_BG_COLOR)
        logo_label.image = logo_image
        logo_label.pack(side="left", padx=5)

    def _add_title(self, parent_frame):
        """Add the InSync title to the given frame."""
        title_label = tk.Label(parent_frame, text="InSync", font=FONT_LOGO, bg=QR_BG_COLOR, fg=QR_LOGO_COLOR)
        title_label.pack(side="left", padx=10)

    def _add_instruction(self):
        """Add the instruction label below the QR code."""
        instruction_label = tk.Label(self.root, text="Scan the QR Code to pair\n(or click anywhere to continue)", 
                                     font=(FONT_QR_TEXT[0], FONT_QR_TEXT[1], "bold"), 
                                     bg=QR_BG_COLOR, fg=QR_TEXT_COLOR)
        instruction_label.pack(pady=20)

    def _generate_qr_code(self):
        """Fetch the QR code from an online API and return as a PhotoImage."""
        app_url = "myapp://open"  
        qr_api_url = f"https://api.qrserver.com/v1/create-qr-code/?size=200x200&data={app_url}"
        
        try:
            response = requests.get(qr_api_url)
            response.raise_for_status()
            img_data = response.content

            img = Image.open(BytesIO(img_data))
            qr_image = ImageTk.PhotoImage(img)
            return qr_image
        except requests.RequestException as e:
            print(f"Error fetching QR code: {e}")
            return None

    def _on_click(self, event):
        """
        Handle click event on the QR code page.

        This method closes the QR code window and opens the PhotoFrameApp as a new window.
        """
        self.root.destroy()  # Close the QR code window
        new_root = tk.Tk()  # Create a new root window
        new_root.overrideredirect(True)  # Remove window decorations for the new window
        new_root.geometry(f"{SCREEN_WIDTH}x{SCREEN_HEIGHT}+0+0")  # Set full screen size for the new window
        app = PhotoFrameApp(new_root)  # Create the PhotoFrameApp
        if self.callback:
            self.callback()  # Call the callback function if provided
        new_root.mainloop()  # Start the main loop for the new window

if __name__ == "__main__":
    root = tk.Tk()
    root.overrideredirect(True)  # Remove window decorations
    root.geometry(f"{SCREEN_WIDTH}x{SCREEN_HEIGHT}+0+0")  # Set full screen size
    app = QRCodePage(root)
    root.mainloop()
