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

        self.fill(self.color)
        font = pygame.font.Font(None, self.font_size)
        text = font.render(self.text, True, self.font_color)
        self.blit(text, ((self.get_width() - text.get_width()) // 2, (self.get_height() - text.get_height()) // 2))
        if not self.showing:
            return

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
            self.parent_screen.blit(self, (self.x_coordinate, self.y_coordinate))
        return self

    def connect(self, function):
        self.functions.append(function)
        return self

    def click(self, pos):
        if pygame.Rect(self.x_coordinate, self.y_coordinate, self.get_width(), self.get_height()).collidepoint(*pos):
            for func in self.functions:
                func()
        return self
