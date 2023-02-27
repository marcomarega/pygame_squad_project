import pygame

from UserInterfafce.background import Background
from UserInterfafce.style import Style, Theme
from load import WIDTH, SIZE

night_background = Background("res\\image\\bg_night.jpg")
night_background = pygame.transform.scale(night_background,
                                          (WIDTH, int(night_background.get_height() * WIDTH / night_background.get_width())))

night_theme = Theme(
    background=night_background,
    button=Style((255, 255, 255), (60, 50, 50), 30, 20),
    text=Style((255, 255, 255), None, 30, 20),
    header=Style((255, 255, 255), None, 30, 50),
    edit_text=Style((255, 255, 255), (60, 50, 50), 50, 42),
    scroll_area_background=Background(color=(60, 50, 50, 130)),
    screen_keeper_theme=Theme(
        background=Background(color=(255, 255, 255, 0)),
        button=Style((255, 255, 255), (60, 50, 50), 30, 20),
        text=Style((255, 255, 255), None, 30, 20),
        header=Style((255, 255, 255), None, 30, 50),
        edit_text=Style((255, 255, 255), (60, 50, 50), 50, 42),
        scroll_area_background=Background(color=(60, 50, 50, 130))
    ),
    game_screen_theme=Theme(
        background=pygame.transform.scale(Background("res\\image\\biru_night.png"), SIZE),
        button=Style((255, 255, 255), (60, 50, 50), 30, 20),
        text=Style((0, 0, 0), None, 30, 20),
        header=Style((255, 255, 255), None, 30, 50),
        edit_text=Style((255, 255, 255), (60, 50, 50), 50, 42),
        scroll_area_background=Background(color=(60, 50, 50, 130)),
    )
)

day_background = Background("res\\image\\bg_day.jpg")
day_background = pygame.transform.scale(day_background,
                                        (WIDTH, int(day_background.get_height() * WIDTH / day_background.get_width())))

day_theme = Theme(
    background=day_background,
    button=Style((0, 0, 0), (200, 225, 225), 30, 20),
    text=Style((0, 0, 0), None, 30, 20),
    header=Style((0, 0, 0), None, 30, 50),
    edit_text=Style((0, 0, 0), (200, 225, 225), 50, 42),
    scroll_area_background=Background(color=(200, 225, 225, 130)),
    screen_keeper_theme=Theme(
        background=Background(color=(255, 255, 255, 0)),
        button=Style((0, 0, 0), (200, 225, 225), 30, 20),
        text=Style((0, 0, 0), None, 30, 20),
        header=Style((0, 0, 0), None, 30, 50),
        edit_text=Style((0, 0, 0), (200, 225, 225), 50, 42),
        scroll_area_background=Background(color=(200, 225, 225, 130))
    ),
    game_screen_theme=Theme(
        background=pygame.transform.scale(Background("res\\image\\biru_day.png"), SIZE),
        button=Style((0, 0, 0), (200, 225, 225), 30, 20),
        text=Style((0, 0, 0), None, 30, 20),
        header=Style((0, 0, 0), None, 30, 50),
        edit_text=Style((0, 0, 0), (200, 225, 225), 50, 42),
        scroll_area_background=Background(color=(200, 225, 225, 130))
    )
)
