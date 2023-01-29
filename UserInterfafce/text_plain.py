import pygame
from pygame import Surface

from UserInterfafce.screen import Screen


class Text(Surface):
    def __init__(self, parent_screen: Screen, rect: pygame.Rect, text, extra_style=None):
        super(Text, self).__init__(rect.size)
        self.parent_screen = parent_screen
        self.extra_style = extra_style

        self.rect = rect
        self.text = text
        self.showing = True

    def move(self, x, y):
        self.rect.x = x
        self.rect.y = y
        return self

    def show(self):
        self.showing = True
        return self

    def hide(self):
        self.showing = False
        return self

    def draw(self, tick):
        if not self.showing:
            return
        if self.extra_style is not None:
            style = self.extra_style
        else:
            style = self.parent_screen.theme["text"]
        font = pygame.font.Font(None, style.font_size)
        text = font.render(self.text, True, style.main_color)
        if style.background_color is not None:
            self.fill(style.background_color)
            self.blit(text,
                      ((self.get_width() - text.get_width()) // 2,
                       (self.get_height() - text.get_height()) // 2))
            self.parent_screen.blit(self, self.rect.topleft)
        else:
            self.parent_screen.blit(text,
                                    ((self.get_width() - text.get_width()) // 2,
                                     (self.get_height() - text.get_height()) // 2))
        return self

    def click(self, pos):
        return self
