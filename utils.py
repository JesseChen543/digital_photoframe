#[1] "Tkinter: update vs update_idletasks," Reddit. [Online]. Available: https://www.reddit.com/r/learnpython/comments/n7v2k4/tkinter_update_vs_update_idletasks/. [Accessed: 11-Oct-2024].

from constant import *

def center_window_parent(window, width, height):
    """Centers a Tkinter window relative to its parent."""
    # Calculate the position to center the window
    window.update_idletasks()
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width // 2) - (POPUP_WIDTH // 2)
    y = (screen_height // 2) - (POPUP_HEIGHT // 2)
    window.geometry(f"{width}x{height}+{x}+{y}")
