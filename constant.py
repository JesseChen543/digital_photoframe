# config.py (or constants.py)

# Screen dimensions
SCREEN_WIDTH = 378
SCREEN_HEIGHT = 624

# File paths
LOGO_IMAGE_PATH = "pictures/logo1 2.png"
ICON_IMAGE_PATH = "pictures/detail_icon.png"
BACKGROUND_IMAGE_PATH = "pictures/photoframe3.png"

# Colors
BACKGROUND_COLOR = "#5081FF"
BUTTON_COLOR = "#5081FF"
BUTTON_TEXT_COLOR = "white"

# Font styles
FONT_TITLE = ("Helvetica", 14)
FONT_BUTTON = ("Helvetica", 10)
FONT_ENTRY = ("Helvetica", 10)

# Time options
TIME_OPTIONS = [f"{h:02d}:00" for h in range(0, 24)]  # Generates times from 00:00 to 23:00
