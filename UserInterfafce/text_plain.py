import pygame
from pygame import Surface

from UserInterfafce.screen import Screen


class Text(Surface):
    def __init__(self, parent_screen: Screen, plain_size, coordinates, color,
                 text, font_size=20, background_color=None):
        super(Text, self).__init__(plain_size)
        self.parent_screen = parent_screen

        self.x_coordinate, self.y_coordinate = coordinates
        self.background_color = background_color
        self.text = text
        self.color = color
        self.font_size = font_size
        self.showing = True

        if background_color is not None:
            return
        font = pygame.font.Font(None, self.font_size)
        text = font.render(self.text, True, self.color)
        self.blit(text, ((self.get_width() - text.get_width()) // 2, (self.get_height() - text.get_height()) // 2))

    def move(self, x, y):
        self.x_coordinate = x
        self.y_coordinate = y
        return self

    def show(self):
        self.showing = True
        return self

    def hide(self):
        self.showing = False
        return self

    def draw(self, tick):
        if self.showing:
            if self.background_color is not None:
                self.parent_screen.blit(self, (self.x_coordinate, self.y_coordinate))
            else:
                font = pygame.font.Font(None, self.font_size)
                text = font.render(self.text, True, self.color)
                self.parent_screen.blit(text,
                                        ((self.get_width() - text.get_width()) // 2,
                                         (self.get_height() - text.get_height()) // 2))
        return self

    def click(self, pos):
        return self
