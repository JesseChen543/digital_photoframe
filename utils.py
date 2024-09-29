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
