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



# BGR_IMG_PATH = "pictures/photoframe3.png"
# BUTTON_IMG_PATH = "pictures/write_note.png"

# def btn_clicked():
#     """ Prints to console a message every time the button is clicked """
#     print("Button Clicked")

# root = tk.Tk()

# background_img = tk.PhotoImage(file=BGR_IMG_PATH)
# bgr_width, bgr_height = background_img.width(), background_img.height()

# root.geometry(f'{bgr_width}x{bgr_height}')
# root.title("TKinter button over transparent background")
# root.configure(bg="white")

# canvas = tk.Canvas(root, bg="white", height=bgr_height, width=bgr_width, bd=0,
#                    highlightthickness=0, relief="ridge")
# canvas.place(x=0, y=0)

# background = canvas.create_image(0, 0, anchor='nw', image=background_img)

# canvas_btn1 = CanvasButton(canvas, 0, 128, BUTTON_IMG_PATH, btn_clicked)
# canvas_btn2 = CanvasButton(canvas, 0, 256, BUTTON_IMG_PATH, btn_clicked)

# root.resizable(False, False)
# root.mainloop()