import pygame

from UserInterfafce.screen import Screen


class Button(pygame.Surface):
    def __init__(self, parent_screen: Screen, rect: pygame.Rect, text="", extra_style=None):
        super(Button, self).__init__(rect.size)
        self.parent_screen = parent_screen
        self.extra_style = extra_style

        self.rect = rect
        self.text = text
        self.showing = True

        self.functions = list()

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
            return self
        if self.extra_style is not None:
            style = self.extra_style
        else:
            style = self.parent_screen.theme["button"]
        self.fill(style.background_color)
        font = pygame.font.Font(None, style.font_size)
        text = font.render(self.text, True, style.main_color)
        self.blit(text, ((self.get_width() - text.get_width()) // 2, (self.get_height() - text.get_height()) // 2))
        if self.showing:
            self.parent_screen.blit(self, (self.rect.x, self.rect.y))
        return self

    def connect(self, function):
        self.functions.append(function)
        return self

    def click(self, pos):
        if self.rect.collidepoint(*pos):
            for func in self.functions:
                func()
        return self
