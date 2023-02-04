import pygame

from UserInterfafce.screen import Screen
from load import SCROLL_SHIFT


class ScreenElement(pygame.Surface):
    def __init__(self, parent_screen, rect, extra_style=None):
        super(ScreenElement, self).__init__(rect.size)
        self.extra_style = extra_style
        self.parent_screen = parent_screen
        self.rect = rect
        self.showing = True

    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy
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
        self.args = list()
        self.functions = list()

    def push_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == pygame.BUTTON_LEFT:
            if self.rect.collidepoint(*event.pos):
                self.is_pressed = True

        if event.type == pygame.MOUSEBUTTONUP and event.button == pygame.BUTTON_LEFT:
            if self.is_pressed and self.rect.collidepoint(*event.pos):
                for func in self.functions:
                    func(*self.args)
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

    def add_args(self, *args):
        self.args.extend(args)
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
                                    (self.rect.x + (self.get_width() - text.get_width()) // 2,
                                     self.rect.y + (self.get_height() - text.get_height()) // 2))
        return self


class ScrollArea(ScreenElement):
    def __init__(self, parent_screen, rect, extra_theme=None):
        super(ScrollArea, self).__init__(parent_screen, rect, None)
        if extra_theme is None:
            self.theme = self.parent_screen.theme
        else:
            self.theme = extra_theme
        self.elements = list()
        self.dy = 0

    def add_element(self, element):
        self.elements.append(element)

    def push_event(self, event):
        if event.type == pygame.MOUSEWHEEL and self.rect.collidepoint(*pygame.mouse.get_pos()):
            self.dy += event.y * SCROLL_SHIFT
            if self.dy > 0:
                for element in self.elements:
                    element.move(0, event.y * SCROLL_SHIFT - self.dy)
                self.dy = 0
            else:
                for element in self.elements:
                    element.move(0, event.y * SCROLL_SHIFT)
        if hasattr(event, "pos"):
            event.pos = (event.pos[0] - self.rect.x, event.pos[1] - self.rect.y)
        for element in self.elements:
            element.push_event(event)

    def draw(self, tick):
        self.blit(self.theme["scroll_area_background"], (0, 0))
        for element in self.elements:
            element.draw(tick)
        self.parent_screen.blit(self, self.rect.topleft)
