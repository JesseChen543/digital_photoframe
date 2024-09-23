import tkinter as tk
from tkinter import PhotoImage, Frame
from PIL import Image, ImageTk

# Variables to store user inputs
saved_list_name = ""
saved_end_value = ""

# Function to handle icon click and open new window
def on_icon_click():
    global saved_list_name, saved_end_value
    # Create a new window (Toplevel is a separate window)
    new_window = tk.Toplevel(root)
    new_window.overrideredirect(True)  # Remove window border and title bar

    # Get the size and position of the main window
    root.update_idletasks()  # Ensure the geometry information is up to date
    root_width = root.winfo_width()
    root_height = root.winfo_height()
    root_x = root.winfo_x()
    root_y = root.winfo_y()

    # Set the width and height of the new window
    new_window_width = 300
    new_window_height = 200

    # Calculate the top-right position
    new_x = root_x + root_width - new_window_width
    new_y = root_y  # Top of the main window

    # Position the new window at the top right of the existing window
    new_window.geometry(f"{new_window_width}x{new_window_height}+{new_x}+{new_y}")

    # Function to store the input and hide the new window when Enter is pressed
    def store_input(event=None):
        global saved_list_name, saved_end_value  # Use global here
        saved_list_name = list_name_entry.get()
        saved_end_value = end_entry.get()
        # Just store the input, do NOT hide the window
        print(f"Input stored: List Name = {saved_list_name}, End Value = {saved_end_value}")

    # Function to hide the new window when clicked outside
    def hide_window(event):
        if event.widget != new_window:
            store_input()  # Save input before hiding
            new_window.withdraw()

    # Set the overall frame with padding and border
    outer_frame = Frame(new_window, bg="orange", padx=10, pady=10, bd=5, relief="ridge")
    outer_frame.pack(fill="both", expand=True, padx=20, pady=20)

    # Inner frame to hold the elements inside the outer frame
    inner_frame = Frame(outer_frame, bg="white", padx=10, pady=10, bd=2, relief="solid")
    inner_frame.pack(fill="both", expand=True)

    # Note Name Label and Entry
    list_name_label = tk.Label(inner_frame, text="Note Name:", bg="white", anchor='w')
    list_name_label.grid(row=0, column=0, sticky='w', pady=10)
    
    list_name_entry = tk.Entry(inner_frame, width=15)
    list_name_entry.grid(row=0, column=1, padx=10, pady=10)
    list_name_entry.insert(0, saved_list_name)  # Restore previous value

    # End Label and Entry
    end_label = tk.Label(inner_frame, text="End:", bg="white", anchor='w')
    end_label.grid(row=1, column=0, sticky='w', pady=10)
    
    end_entry = tk.Entry(inner_frame, width=15)
    end_entry.grid(row=1, column=1, padx=10, pady=10)
    end_entry.insert(0, saved_end_value)  # Restore previous value

    # note Label and entry
    note_label = tk.Label(inner_frame, text="Note", bg="white", anchor='w')
    note_label.grid(row=2, column=0, sticky='nw', pady=10)

    note_entry = tk.Text(inner_frame, width=15, height=100)
    note_entry.grid(row=2, column=1, padx=10, pady=10)
    note_entry.insert(0, saved_end_value)  # Restore previous value

    # Bind the Enter key to store input
    list_name_entry.bind("<Return>", store_input)
    end_entry.bind("<Return>", store_input)
    note_entry.bind("<Return>", store_input)

    # Bind the click event to hide the popup when clicked outside
    root.bind("<Button-1>", hide_window)

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
