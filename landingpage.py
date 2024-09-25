import tkinter as tk
from tkinter import PhotoImage
from PIL import Image, ImageTk
from constant import *
from QRCodePage import QRCodePage

class SplashScreenApp:
    def __init__(self, root):
        self.root = root
        self.root.title("InSync")
        
        # Set full screen size and background color
        self.root.geometry(f"{SCREEN_WIDTH}x{SCREEN_HEIGHT}")
        self.root.configure(bg=LANDING_BG_COLOR)

        # Create a frame to hold both the logo and the title
        title_frame = tk.Frame(self.root, bg=LANDING_BG_COLOR)
        title_frame.pack(expand=True, anchor="center")  # Center both horizontally and vertically

        # Create an inner frame for horizontal alignment of logo and title
        inner_frame = tk.Frame(title_frame, bg=LANDING_BG_COLOR)
        inner_frame.pack()

        # Load logo image
        logo_image_path = "pictures/logo1 2.png"
        logo_img = Image.open(logo_image_path)
        logo_img = logo_img.resize((84, 88), Image.LANCZOS)
        logo_image = ImageTk.PhotoImage(logo_img)

        # Create a label for the logo image and place it inside the inner frame
        logo_label = tk.Label(inner_frame, image=logo_image, bg=LANDING_BG_COLOR)
        logo_label.image = logo_image
        logo_label.pack(side="left", padx=10)

        # Title Label using Pacifico font and place it inside the inner frame
        title_label = tk.Label(inner_frame, text="InSync", font=FONT_LOGO, bg=LANDING_BG_COLOR, fg=LANDING_FG_COLOR)
        title_label.pack(side="left", padx=10)

        # Bottom Label using DM Sans font
        bottom_label = tk.Label(self.root, text="Click anywhere to start", font=FONT_LANDING, bg=LANDING_BG_COLOR, fg=LANDING_FG_COLOR)
        bottom_label.pack(side="bottom", pady=20)

        # Create a button event for clicking anywhere on the screen
        self.root.bind("<Button-1>", self.start_action)

    def start_action(self, event):
        # Destroy the current window and open the QR Code page
        self.root.destroy()  # Close current window
        new_root = tk.Tk()  # Create a new root window
        QRCodePage(new_root)  # Call the QRCodePage class
        new_root.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    app = SplashScreenApp(root)
    root.mainloop()