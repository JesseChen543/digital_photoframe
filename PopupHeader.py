import tkinter as tk
from tkinter import Frame, Label, Button
from constant import *


class PopupHeader:
    def __init__(self, parent, title_text, on_close):
        """
        Initializes the popup header.
        Args:
        parent (tk.Toplevel or tk.Frame): The parent window or frame.
        title_text (str): The text to display as the title.
        on_close (callable): The function to call when the close button is clicked.
        """
        self.parent = parent
        self.title_text = title_text
        self.on_close = on_close
        self.setup_header()

    def setup_header(self):
        """Creates and packs the header components."""
        # Title frame
        title_close_frame = Frame(self.parent, bg=POPUP_BG_COLOR)
        title_close_frame.pack(fill="x", pady=10)
        # Title label
        title_label = Label(
        title_close_frame,
        text=self.title_text,
        font=FONT_LARGE,
        bg=POPUP_BG_COLOR
        )
        title_label.pack(side="left", padx=20, fill="x", expand=True)

        # Close button
        close_button = Button(
        title_close_frame,
        text="X",
        command=self.on_close,
        bg="white",
        fg=CLOSE_COLOR,
        font=(FONT_SMALL, 12),
        relief="flat"
        )
        close_button.pack(side="right", padx=10)
        
        # Separator line
        separator = tk.Frame(self.parent, bg="grey", height=1)
        separator.pack(fill="x", pady=5)