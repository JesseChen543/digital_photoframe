import tkinter as tk
from tkinter import PhotoImage, Frame
from PIL import Image, ImageTk

class PhotoFrameApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Display with Clickable Icon")

        # Initialize saved inputs
        self.saved_list_name = ""
        self.saved_end_value = ""
        self.saved_note_value = ""

        # Screen dimensions in pixels
        screen_width = 378  # 16.5 cm converted to pixels
        screen_height = 624  # 10 cm converted to pixels

        # Load and display the full-screen image
        image_path = "pictures/photoframe3.png"  # Replace with image from the database  
        image = Image.open(image_path)
        image = image.resize((screen_width, screen_height), Image.LANCZOS)
        bg_image = ImageTk.PhotoImage(image)

        # Create a label to display the background image
        bg_label = tk.Label(self.root, image=bg_image)
        bg_label.image = bg_image  # Keep a reference to avoid garbage collection
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Load the icon image
        icon_image_path = "pictures/detail_icon.png"  # Replace with image from the database  
        icon = Image.open(icon_image_path)
        icon = icon.resize((30, 30), Image.LANCZOS)
        icon_image = ImageTk.PhotoImage(icon)

        # Create a button for the icon and place it at the top right corner
        icon_button = tk.Button(self.root, image=icon_image, command=self.show_popup, borderwidth=0)
        icon_button.image = icon_image  # Keep a reference to avoid garbage collection
        icon_button.place(x=screen_width - 60, y=10)

        # Set window size based on screen dimensions
        self.root.geometry(f"{screen_width}x{screen_height}")
        self.root.bind('<Escape>', self.quit_app)

    def show_popup(self):
        """Display the popup window in the center of the main window."""
        popup = tk.Toplevel(self.root)
        popup.geometry("400x400")
        popup.configure(bg="white")

        # Calculate the center of the main window
        self.root.update_idletasks()
        root_width = self.root.winfo_width()
        root_height = self.root.winfo_height()
        root_x = self.root.winfo_x()
        root_y = self.root.winfo_y()

        # Center the popup window
        popup_width = 400
        popup_height = 400
        new_x = root_x + (root_width // 2) - (popup_width // 2)
        new_y = root_y + (root_height // 2) - (popup_height // 2)
        popup.geometry(f"{popup_width}x{popup_height}+{new_x}+{new_y}")

        # Create the top frame for title and close button
        top_frame = Frame(popup, bg="white", padx=20, pady=10)
        top_frame.pack(fill="x", side="top")

        title_label = tk.Label(top_frame, text="Write a Note", font=("Helvetica", 14), bg="white")
        title_label.grid(row=0, column=0, sticky="w")

        date_label = tk.Label(top_frame, text="20/09/2024", font=("Helvetica", 10), bg="white")
        date_label.grid(row=1, column=0, sticky="w", pady=5)

        close_button = tk.Button(top_frame, text="X", command=popup.destroy, font=("Helvetica", 10), bg="white", bd=0)
        close_button.grid(row=0, column=1, sticky="e")

        # Inner frame for form elements
        inner_frame = Frame(popup, bg="white", padx=20, pady=10)
        inner_frame.pack(fill="both", expand=True)

        # Name label and entry
        list_name_label = tk.Label(inner_frame, text="Name:", bg="white", font=("Helvetica", 10))
        list_name_label.grid(row=0, column=0, sticky='w', pady=10)

        list_name_entry = tk.Entry(inner_frame, width=30, font=("Helvetica", 10), relief="solid", bd=1)
        list_name_entry.grid(row=0, column=1, padx=10, pady=10)
        list_name_entry.insert(0, self.saved_list_name)

        # End label and entry
        end_label = tk.Label(inner_frame, text="End:", bg="white", font=("Helvetica", 10))
        end_label.grid(row=1, column=0, sticky='w', pady=10)

        end_entry = tk.Entry(inner_frame, width=30, font=("Helvetica", 10), relief="solid", bd=1)
        end_entry.grid(row=1, column=1, padx=10, pady=10)
        end_entry.insert(0, self.saved_end_value)

        # Note label and text entry
        note_label = tk.Label(inner_frame, text="Note:", bg="white", font=("Helvetica", 10))
        note_label.grid(row=2, column=0, sticky='nw', pady=10)

        note_entry = tk.Text(inner_frame, width=30, height=5, font=("Helvetica", 10), relief="solid", bd=1)
        note_entry.grid(row=2, column=1, padx=10, pady=10)
        note_entry.insert("1.0", self.saved_note_value)

        # Store input values when pressing Enter
        def store_input(event=None):
            self.saved_list_name = list_name_entry.get()
            self.saved_end_value = end_entry.get()
            self.saved_note_value = note_entry.get("1.0", tk.END)
            print(f"Input stored: Name = {self.saved_list_name}, End Value = {self.saved_end_value}, Note = {self.saved_note_value}")

        # Submit button
        submit_button = tk.Button(popup, text="Upload", command=store_input, bg="#4C9AFF", fg="white", font=("Helvetica", 10), relief="flat", width=10)
        submit_button.pack(pady=10, side="bottom")

        # Bind the Enter key to store input
        list_name_entry.bind("<Return>", store_input)
        end_entry.bind("<Return>", store_input)

    def quit_app(self, event=None):
        """Quit the application."""
        self.root.quit()


if __name__ == "__main__":
    root = tk.Tk()
    app = PhotoFrameApp(root)
    root.mainloop()
