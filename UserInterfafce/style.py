import pygame


class Style:
    def __init__(self, main_color, background_color, d_color, font_size):
        self.main_color = pygame.Color(main_color)
        if background_color is None:
            self.background_color = None
        else:
            self.background_color = pygame.Color(background_color)
        self.d_color = d_color
        self.font_size = font_size


class Theme:
    def __init__(self, **styles):
        self.styles = styles

    def __getitem__(self, item):
        return self.styles[item]
