import string
from copy import deepcopy

import pygame

from UserInterfafce.intention import Intent
from UserInterfafce.screen import Screen
from load import SCROLL_SHIFT


class ScreenElement(pygame.Surface):
    def __init__(self, parent_screen, rect, extra_style=None):
        super(ScreenElement, self).__init__(rect.size, pygame.SRCALPHA, 32)
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
        if not self.showing:
            return False
        return self.event_processing(pygame.event.Event(deepcopy(event.type), deepcopy(event.dict)))

    def event_processing(self, event):
        return False

    def draw(self, tick):
        if not self.showing:
            return False
        self.fill((0, 0, 0, 0))
        return True


class Button(ScreenElement):
    def __init__(self, parent_screen: Screen, rect: pygame.Rect, text="", extra_style=None):
        super(Button, self).__init__(parent_screen, rect, extra_style)

        self.text = text
        self.is_pressed = False
        self.args = list()
        self.functions = list()

    def event_processing(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == pygame.BUTTON_LEFT:
            if self.rect.collidepoint(*event.pos):
                self.is_pressed = True
                return True

        if event.type == pygame.MOUSEBUTTONUP and event.button == pygame.BUTTON_LEFT:
            if self.is_pressed and self.rect.collidepoint(*event.pos):
                for func in self.functions:
                    func(*self.args)
                self.is_pressed = False
                return True
            self.is_pressed = False

    def draw(self, tick):
        if self.extra_style is not None:
            style = self.extra_style
        else:
            style = self.parent_screen.theme.data["button"]
        d_color = style.d_color
        if style.background_color is not None:
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
        return True

    def add_args(self, *args):
        self.args.extend(args)
        return self

    def connect(self, function):
        self.functions.append(function)
        return self

    def get_text(self):
        return self.text


class TextPlain(ScreenElement):
    def __init__(self, parent_screen: Screen, rect: pygame.Rect, text, extra_style=None):
        super(TextPlain, self).__init__(parent_screen, rect, extra_style)
        self.text = text

    def set_text(self, text):
        self.text = text

    def get_text(self):
        return self.text

    def draw(self, tick):
        if not super(TextPlain, self).draw(tick):
            return False
        if self.extra_style is not None:
            style = self.extra_style
        else:
            style = self.parent_screen.theme.data["text"]
        font = pygame.font.Font(None, style.font_size)
        text = font.render(self.text, True, style.main_color)
        if style.background_color is not None:
            self.fill(style.background_color)
        self.blit(text,
                  ((self.get_width() - text.get_width()) // 2,
                   (self.get_height() - text.get_height()) // 2))
        self.parent_screen.blit(self, self.rect.topleft)
        return True


class EditText(ScreenElement):
    def __init__(self, parent_screen, rect, text="", extra_style=None):
        super(EditText, self).__init__(parent_screen, rect, extra_style)
        self.selected = False
        self.text = text
        self.functions = list()

    def connect_text_handler(self, functon):
        self.functions.append(functon)
        return self

    def set_text(self, text):
        self.text = text
        return self

    def get_text(self):
        return self.text

    def event_processing(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos):
            self.selected = True
            return True
        if event.type == pygame.MOUSEBUTTONDOWN and not self.rect.collidepoint(event.pos):
            self.selected = False
        if self.selected and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                for function in self.functions:
                    function(self.text)
            elif event.key == pygame.K_BACKSPACE:
                self.text = self.text[0:-1]
            elif event.unicode.upper() in string.ascii_letters:
                self.text += event.unicode.upper()
            return True

    def draw(self, tick):
        if not super(EditText, self).draw(tick):
            return False
        if self.extra_style is not None:
            style = self.extra_style
        else:
            style = self.parent_screen.theme.data["edit_text"]
        if self.selected:
            main_color = style.main_color
            background_color = style.background_color
        else:
            main_color = (max(0, style.main_color[0] - style.d_color),
                          max(0, style.main_color[1] - style.d_color),
                          max(0, style.main_color[2] - style.d_color))
            if style.background_color is not None:
                background_color = (max(0, style.background_color[0] - style.d_color),
                                    max(0, style.background_color[1] - style.d_color),
                                    max(0, style.background_color[2] - style.d_color))
            else:
                background_color = None
        font = pygame.font.Font(None, style.font_size)
        text = font.render(self.text, True, main_color)
        if background_color is not None:
            self.fill(background_color)
        pygame.draw.rect(self, main_color, (0, 0, *self.get_size()), 3)
        if text.get_width() < self.get_width() - 6:
            self.blit(text, (3, 3))
        else:
            self.blit(text, (self.get_width() - text.get_width() - 6, 3))
        self.parent_screen.blit(self, self.rect.topleft)
        return True


class ScrollArea(ScreenElement):
    def __init__(self, parent_screen, rect, extra_theme=None):
        super(ScrollArea, self).__init__(parent_screen, rect, None)
        if extra_theme is None:
            self.theme = self.parent_screen.theme
        else:
            self.theme = extra_theme
        self.elements = list()
        self.dy = 0
        self.lower_y = 0

    def add_element(self, element):
        self.elements.append(element)
        self.lower_y = max(self.lower_y, element.rect.bottom)
        return self

    def event_processing(self, event):
        if event.type == pygame.MOUSEWHEEL and self.rect.collidepoint(*pygame.mouse.get_pos()):
            self.dy += event.y * SCROLL_SHIFT
            if self.dy > 0:
                for element in self.elements:
                    element.move(0, event.y * SCROLL_SHIFT - self.dy)
                self.lower_y += event.y * SCROLL_SHIFT - self.dy
                self.dy = 0
            else:
                for element in self.elements:
                    element.move(0, event.y * SCROLL_SHIFT)
                self.lower_y += event.y * SCROLL_SHIFT
            if self.lower_y < 10:
                for element in self.elements:
                    element.move(0, 10 - self.lower_y)
                self.dy += 10 - self.lower_y
                self.lower_y = 10
        if hasattr(event, "pos"):
            event.pos = (event.pos[0] - self.rect.x, event.pos[1] - self.rect.y)
        for element in self.elements:
            element.push_event(event)

    def draw(self, tick):
        if not super(ScrollArea, self).draw(tick):
            return False
        if self.theme.data["scroll_area_background"] is not None:
            self.blit(self.theme.data["scroll_area_background"], (0, 0))
        for element in self.elements:
            element.draw(tick)
        self.parent_screen.blit(self, self.rect.topleft)
        return True
    
    
class ScreenKeeper(ScreenElement):
    def __init__(self, parent_screen, rect, extra_theme=None):
        super(ScreenKeeper, self).__init__(parent_screen, rect, None)
        if extra_theme is not None:
            self.theme = extra_theme
        else:
            self.theme = self.parent_screen.theme
        self.intent = Intent(self)
        self.current_screen = None

    def set_current_screen(self, screen_class, *args):
        self.current_screen = screen_class(self, self.intent, self.parent_screen.file_base, *args)
        return self

    def push_intent(self):
        self.current_screen = self.intent.get_screen(self)

    def get_parent_screen(self):
        return self.parent_screen

    def draw(self, tick):
        if not super(ScreenKeeper, self).draw(tick):
            return False
        self.current_screen.draw(tick)
        self.parent_screen.blit(self.current_screen, self.rect.topleft)
        return True

    def event_processing(self, event):
        if hasattr(event, "pos"):
            event.pos = (event.pos[0] - self.rect.x, event.pos[1] - self.rect.y)
        if self.current_screen is None:
            return self
        return self.current_screen.push_event(event)

    def push_event_to_parent_screen(self, event):
        self.parent_screen.push_event(event)


# class FeaturesLearning(ScreenElement):
#     def __init__(self, parent_screen, rect, text: TextPlain, extra_theme=None):
#         super(FeaturesLearning, self).__init__(parent_screen, rect, None)
#         if extra_theme is None:
#             self.theme = self.parent_screen.theme
#         else:
#             self.theme = extra_theme
#         self.text = text
#         self.buttons = []
#         self.closing_buttons = {'No': 0, 'Close': 1, 'Got it!': -1}
#
#     def add_element(self, element):
#         self.buttons.append(element)
#
#     def event_processing(self, event):
#         for btn in self.buttons:
#             if event.type == pygame.MOUSEBUTTONDOWN and btn.collidepoint(*pygame.mouse.get_pos()):
#                 if btn.get_text() in self.closing_buttons:
#                     self.close()
#                 else:
#                     btn.push_event()
#                     break
#
#     def close(self):
#         del self
#
#     def draw(self, tick):
#         if not super(FeaturesLearning, self).draw(tick):
#             return False
#         pygame.draw.rect(self.parent_screen, (255, 255, 255), self.rect)
#         self.text.draw(tick)
#         for btn in self.buttons:
#             btn.draw(tick)
#         self.parent_screen.blit(self, self.rect.topleft)
#         return True
