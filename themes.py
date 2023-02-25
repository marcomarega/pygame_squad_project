from UserInterfafce.background import Background
from UserInterfafce.style import Style, Theme

night_theme = Theme(
    background=Background("res\\image\\bg_night.jpg"),
    button=Style((255, 255, 255),  (60, 50, 50), 30, 20),
    text=Style((255, 255, 255),  None, 30, 20),
    header=Style((255, 255, 255), None, 30, 50),
    edit_text=Style((255, 255, 255), (60, 50, 50), 50, 42),
    scroll_area_background=Background(color=(60, 50, 50, 130)),
    screen_keeper_theme=Theme(
        background=Background(color=(0, 0, 0)),
        button=Style((255, 255, 255),  (60, 50, 50), 30, 20),
        text=Style((255, 255, 255),  None, 30, 20),
        header=Style((255, 255, 255), None, 30, 50),
        edit_text=Style((255, 255, 255), (60, 50, 50), 50, 42),
        scroll_area_background=Background(color=(60, 50, 50, 130))
    ),
    level_playing_theme=Theme(
        background=Background("res\\image\\biru1.jpg"),
        button=Style((255, 255, 255),  (60, 50, 50), 30, 20),
        text=Style((255, 255, 255),  None, 30, 20),
        header=Style((255, 255, 255), None, 30, 50),
        edit_text=Style((255, 255, 255), (60, 50, 50), 50, 42),
        scroll_area_background=Background(color=(60, 50, 50, 130)),
    )
)

day_theme = Theme(
    background=Background("res\\image\\bg_day.jpg"),
    button=Style((0, 0, 0), (200, 225, 225), 30, 20),
    text=Style((0, 0, 0), None, 30, 20),
    header=Style((0, 0, 0), None, 30, 50),
    edit_text=Style((0, 0, 0), (200, 225, 225), 50, 42),
    scroll_area_background=Background(color=(200, 225, 225, 130)),
    screen_keeper_theme=Theme(
        background=Background(color=(255, 255, 255)),
        button=Style((0, 0, 0), (200, 225, 225), 30, 20),
        text=Style((0, 0, 0), None, 30, 20),
        header=Style((0, 0, 0), None, 30, 50),
        edit_text=Style((0, 0, 0), (200, 225, 225), 50, 42),
        scroll_area_background=Background(color=(200, 225, 225, 130))
    ),
    level_playing_theme=Theme(
        background=Background("res\\image\\biru1.jpg"),
        button=Style((0, 0, 0), (200, 225, 225), 30, 20),
        text=Style((0, 0, 0), None, 30, 20),
        header=Style((0, 0, 0), None, 30, 50),
        edit_text=Style((0, 0, 0), (200, 225, 225), 50, 42),
        scroll_area_background=Background(color=(200, 225, 225, 130))
    )
)
