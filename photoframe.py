import tkinter as tk
from tkinter import PhotoImage
from PIL import Image, ImageTk

# Function to handle icon click
def on_icon_click():
    print("Icon clicked!")

# Function to quit the application (remove in production)
def quit_app(event=None):
    root.quit()

# Create the main window
root = tk.Tk()
root.title("Image Display with Clickable Icon")

# Bind the Esc key to quit the application (remove in production)
root.bind('<Escape>', quit_app)

# Screen dimensions in pixels (based on 96 DPI)
screen_width = 624  # 16.5 cm converted to pixels
screen_height = 378  # 10 cm converted to pixels

# Load and display the full-screen image
image_path = "pictures/family photo.webp"  # Replace with image from the database  
image = Image.open(image_path)
image = image.resize((screen_width, screen_height), Image.LANCZOS)  
bg_image = ImageTk.PhotoImage(image)

# Create a label to display the background image
bg_label = tk.Label(root, image=bg_image)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)

# Load the icon image
icon_image_path = "pictures/collect_5.png"  # Replace with image from the database  
icon = Image.open(icon_image_path)
icon = icon.resize((30, 30), Image.LANCZOS)  # Resize the icon to 50x50 pixels
icon_image = ImageTk.PhotoImage(icon)

# Create a button for the icon and place it at the top right corner
icon_button = tk.Button(root, image=icon_image, command=on_icon_click, borderwidth=0)
icon_button.place(x=screen_width - 60, y=10)  # Position icon button relative to screen size

root.geometry(f"{screen_width}x{screen_height}")  # Set window size based on screen dimensions
root.mainloop()
