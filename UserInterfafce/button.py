import pygame

from UserInterfafce.screen import Screen


class Button(pygame.Surface):
    def __init__(self, parent_screen: Screen, button_size, coordinates, color,
                 text="", font_color=(0, 0, 0), font_size=20):
        super(Button, self).__init__(button_size)
        self.parent_screen = parent_screen

        self.x_coordinate, self.y_coordinate = coordinates
        self.color = color
        self.text = text
        self.font_color = font_color
        self.font_size = font_size
        self.showing = True

        self.functions = list()

    def move(self, x, y):
        self.x_coordinate = x
        self.y_coordinate = y

    def show(self):
        self.showing = True

    def hide(self):
        self.showing = False

    def draw(self, tick):
        font = pygame.font.Font(None, self.font_size)
        text = font.render(self.text, True, self.font_color)
        self.blit(text, ((self.get_width() - text.get_width()) // 2, (self.get_height() - text.get_height()) // 2))
        if not self.showing:
            return
        self.parent_screen.blit(self, (self.x_coordinate, self.y_coordinate))

    def connect(self, function):
        self.functions.append(function)
