import pygame

from UserInterfafce.screen import Screen


class ScreenElement(pygame.Surface):
    def __init__(self, parent_screen, rect, extra_style=None):
        super(ScreenElement, self).__init__(rect.size)
        self.extra_style = extra_style
        self.parent_screen = parent_screen
        self.rect = rect
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

    def push_event(self, event):
        return self

    def draw(self, tick):
        return self


class Button(ScreenElement):
    def __init__(self, parent_screen: Screen, rect: pygame.Rect, text="", extra_style=None):
        super(Button, self).__init__(parent_screen, rect, extra_style)

        self.text = text
        self.is_pressed = False
        self.functions = list()

    def push_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(*event.pos):
                self.is_pressed = True

        if event.type == pygame.MOUSEBUTTONUP:
            if self.is_pressed and self.rect.collidepoint(*event.pos):
                for func in self.functions:
                    func()
            self.is_pressed = False
            return self

    def draw(self, tick):
        if not self.showing:
            return self
        if self.extra_style is not None:
            style = self.extra_style
        else:
            style = self.parent_screen.theme["button"]
        d_color = style.d_color
        if self.is_pressed:
            self.fill((max(0, style.background_color[0] - d_color),
                       max(0, style.background_color[1] - d_color),
                       max(0, style.background_color[2] - d_color)))
        else:
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


class TextPlain(ScreenElement):
    def __init__(self, parent_screen: Screen, rect: pygame.Rect, text, extra_style=None):
        super(TextPlain, self).__init__(parent_screen, rect, extra_style)
        self.text = text

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
