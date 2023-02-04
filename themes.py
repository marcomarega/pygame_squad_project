from UserInterfafce.background import Background
from UserInterfafce.style import Style, Theme

night_theme = Theme(
    background=Background("res\\image\\bg_night.jpg"),
    button=Style((255, 255, 255),  (60, 50, 50), 30, 20),
    text=Style((255, 255, 255),  None, 30, 20),
    header=Style((255, 255, 255), None, 30, 50),
    scroll_area_background=Background(color="black")
)

day_theme = Theme(
    background=Background("res\\image\\bg_day.jpg"),
    button=Style((0, 0, 0), (200, 225, 225), 30, 20),
    text=Style((0, 0, 0), None, 30, 20),
    header=Style((0, 0, 0), None, 30, 50),
    scroll_area_background=Background(color="white")
)
