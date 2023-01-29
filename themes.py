from UserInterfafce.background import Background
from UserInterfafce.style import Style, Theme

night_theme = Theme(
    background=Background("res\\image\\bg_night.jpg"),
    button=Style((255, 255, 255),  (60, 50, 50), 20),
    text=Style((255, 255, 255),  None,  20)
)

day_theme = Theme(
    background=Background("res\\image\\bg_day.jpg"),
    button=Style((0, 0, 0), (200, 225, 225), 20),
    text=Style((0, 0, 0), None, 20)
)
