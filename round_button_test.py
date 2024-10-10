import tkinter as tk
from PIL import Image, ImageTk
from constant import *

class CanvasButton:
    """ Create a leftmost mouse button clickable canvas image object. """

    flash_delay = 100  # Milliseconds.

    def __init__(self, canvas, x, y, image_path, command, size=ICON_DIMENSION, state=tk.NORMAL):
        self.canvas = canvas
        self.original_image = Image.open(image_path).resize(size, Image.LANCZOS)
        self.btn_image = ImageTk.PhotoImage(self.original_image)

        self.canvas_btn_img_obj = canvas.create_image(x, y, anchor='nw', state=state,
                                                      image=self.btn_image)
        canvas.tag_bind(self.canvas_btn_img_obj, "<ButtonRelease-1>",
                        lambda event: (self.flash(), command()))

    def flash(self):
        self.set_state(tk.HIDDEN)
        self.canvas.after(self.flash_delay, self.set_state, tk.NORMAL)

    def set_state(self, state):
        """ Change canvas button image's state. """
        self.canvas.itemconfigure(self.canvas_btn_img_obj, state=state)

    def set_opacity(self, opacity):
        """ Set the opacity of the button image. """
        if not (0 <= opacity <= 1):
            raise ValueError("Opacity must be between 0.0 and 1.0.")
        
        alpha_image = self.adjust_image_opacity(self.original_image, opacity)
        self.canvas.itemconfig(self.canvas_btn_img_obj, image=alpha_image)
        self.btn_image = alpha_image  # Update the reference to the new image

    def adjust_image_opacity(self, image, opacity):
        """ Adjust the opacity of an image. """
        # Convert the original image to RGBA format
        pil_image = image.convert("RGBA")
        new_data = []

        for item in pil_image.getdata():
            # Modify the alpha channel based on the desired opacity
            new_data.append((item[0], item[1], item[2], int(item[3] * opacity)))

        pil_image.putdata(new_data)
        return ImageTk.PhotoImage(pil_image)  # Return the new image with adjusted opacity
