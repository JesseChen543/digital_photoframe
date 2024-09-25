import tkinter as tk
from PIL import Image, ImageTk
import requests
from io import BytesIO
from constant import *

class QRCodePage:
    def __init__(self, root):
        self.root = root
        self.root.title("Pairing via QR Code")

        # Set full screen size and background color
        self.root.geometry(f"{SCREEN_WIDTH}x{SCREEN_HEIGHT}")
        self.root.configure(bg=QR_BG_COLOR)

        # Create a frame for title (logo + text)
        title_frame = tk.Frame(self.root, bg=QR_BG_COLOR)
        title_frame.pack(pady=40)

        # Load the logo image
        logo_img = Image.open(LOGO_IMAGE_PATH)
        logo_img = logo_img.resize((60, 60), Image.LANCZOS)
        logo_image = ImageTk.PhotoImage(logo_img)

        # Logo Label
        logo_label = tk.Label(title_frame, image=logo_image, bg=QR_BG_COLOR)
        logo_label.image = logo_image
        logo_label.pack(side="left", padx=5)

        # Title Label using Pacifico font
        title_label = tk.Label(title_frame, text="InSync", font=FONT_LOGO, bg=QR_BG_COLOR, fg=QR_LOGO_COLOR)
        title_label.pack(side="left", padx=10)

        # Fetch QR code using API
        qr_code = self.generate_qr_code()

        # Display the QR code
        qr_label = tk.Label(self.root, image=qr_code, bg=QR_BG_COLOR)
        qr_label.image = qr_code
        qr_label.pack(pady=20)

        # Instruction Label 
        instruction_label = tk.Label(self.root, text="Scan the QR Code to pair", font=(FONT_QR_TEXT[0], FONT_QR_TEXT[1], "bold"), bg=QR_BG_COLOR, fg=QR_TEXT_COLOR)
        instruction_label.pack(pady=20)

    def generate_qr_code(self):
        """Fetch the QR code from an online API and return as a PhotoImage."""
        # Replace 'myapp' with your app's URL scheme or direct app store URL
        app_url = "myapp://open"  
        # app_url = "https://play.google.com/store/apps/details?id=com.example.myapp"  # Example Play Store URL

        # Generate QR code with the app URL
        qr_api_url = f"https://api.qrserver.com/v1/create-qr-code/?size=200x200&data={app_url}"
        response = requests.get(qr_api_url)
        img_data = response.content

        # Convert image data into a PhotoImage object
        img = Image.open(BytesIO(img_data))
        qr_image = ImageTk.PhotoImage(img)

        return qr_image


if __name__ == "__main__":
    root = tk.Tk()
    app = QRCodePage(root)
    root.mainloop()
