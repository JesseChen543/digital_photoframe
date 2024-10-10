import tkinter as tk
from PIL import Image, ImageTk
from constant import *

class CanvasButton:
    """ Create a leftmost mouse button clickable canvas image object.

    The x, y coordinates are relative to the top-left corner of the canvas.
    """
    flash_delay = 100  # Milliseconds.

    def __init__(self, canvas, x, y, image_path, command, size=ICON_DIMENSION, state=tk.NORMAL):
        self.canvas = canvas
        # Resize the image using PIL and convert to PhotoImage
        image = Image.open(image_path).resize(size, Image.LANCZOS)
        self.btn_image = ImageTk.PhotoImage(image)

        self.canvas_btn_img_obj = canvas.create_image(x, y, anchor='nw', state=state,
                                                      image=self.btn_image)
        canvas.tag_bind(self.canvas_btn_img_obj, "<ButtonRelease-1>",
                        lambda event: (self.flash(), command()))

    def flash(self):
        self.set_state(tk.HIDDEN)
        self.canvas.after(self.flash_delay, self.set_state, tk.NORMAL)

    def set_state(self, state):
        """ Change canvas button image's state.

        Normally, image objects are created in state tk.NORMAL. Use value
        tk.DISABLED to make it unresponsive to the mouse, or use tk.HIDDEN to
        make it invisible.
        """
        self.canvas.itemconfigure(self.canvas_btn_img_obj, state=state)

    def set_opacity(self, opacity):
        """Set the opacity of the button image."""
        alpha_image = self.adjust_image_opacity(self.btn_image, opacity)
        self.canvas.itemconfig(self.canvas_btn_img_obj, image=alpha_image)
        self.btn_image = alpha_image  # Update the reference to the new image

    def adjust_image_opacity(self, image, opacity):
        """Adjust the opacity of an image."""
        # Convert the image to RGBA format
        image = image._PhotoImage__photo.zoom(1, 1)  # Get the raw image
        image = image.convert("RGBA")
        new_data = []
        for item in image.getdata():
            new_data.append((item[0], item[1], item[2], int(item[3] * opacity)))  # Modify alpha channel
        image.putdata(new_data)
        return ImageTk.PhotoImage(image)  # Return the new image with adjusted opacity

