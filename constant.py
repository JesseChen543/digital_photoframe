# Screen dimensions
SCREEN_WIDTH = 480
SCREEN_HEIGHT = 800

#icon and image dimensions 
ICON_DIMENSION = (60, 66)
IMAGE_DIMENSION = (100, 130)

#popup dimensions
POPUP_WIDTH = 290
POPUP_HEIGHT = 390
PICKDATE_WIDTH = 270
PICKDATE_HEIGHT = 206
FRAME_WIDTH = POPUP_WIDTH - 40
FRAME_HEIGHT = 50
FRAME_HEIGHT_COLLAPSED = 50
FRAME_HEIGH_EXPANDED = 80
ICON_SIZE = 40

#input dimensions 
LIST_NAME_WIDTH = 32

#icon margin
NOTE_ICON_X = SCREEN_WIDTH - 70
NOTE_ICON_Y = 17
CALENDAR_ICON_X = 20
CALENDAR_ICON_Y = 17
LIST_ICON_X = 20
LIST_ICON_Y = 82


# File paths
LOGO_IMAGE_PATH = "pictures/logo1 2.png"
WRITE_NOTE_ICON_IMAGE_PATH = "pictures/write_note.png"
UPCOMING_SCHEDULE_ICON = "pictures/upcoming_schedule.png"
LIST_ICON = "pictures/list.png"
DROPDOWN_ICON = "pictures/dropdown.png"
DROPDOWN_ICON_INVERSED = "pictures/dropdownicon_inversed.png"
TIME_ICON = "pictures/time_icon.png"
MEMBER_ICON = "pictures/membericon.png"
SCHEDULE_PICTURE = "pictures/schedule pic.png"

# Colors
LANDING_BG_COLOR = "#5081FF"
LANDING_FG_COLOR = "#FFFFFF"
QR_BG_COLOR = "#FFFFFF"
QR_LOGO_COLOR = "#2C2C2C"
QR_TEXT_COLOR = "#000000"
BUTTON_COLOR = "#5081FF"
BUTTON_TEXT_COLOR = "#FFFFFF"
POPUP_BG_COLOR = "#FFFFFF"
INPUT_COLOR = "#F0F0F0"
CLOSE_COLOR = "#4E4E4E"
PICK_DATE_TEXT_COLOR = "#333333"
PICK_DATE_PREFILLED_COLOR = "#9B9B9B"
CHOOSE_DATE_PREFILLED_COLOR = "#3F3F3F"
PREFILLED_BG_COLOR = "#F1F3F7"



# Font styles
FONT_LOGO = ("Pacifico", 30)
FONT_LANDING = ("DM Sans", 12)
FONT_QR_TEXT = ("Overpass", 12)
FONT_LARGE = ("Inter", 16)
FONT_MEDIUM = ("Inter", 12)
FONT_MEDIUM_BOLD = ("Inter", 12, "bold")
FONT_SMALL = ("Inter", 9)
FONT_SMALL_BOLD = ("Inter", 9, "bold")
FONT_PREFILLED = ("Open Sans", 9)

# Time options
TIME_OPTIONS = [f"{h:02d}:00" for h in range(0, 24)]  # Generates times from 00:00 to 23:00
