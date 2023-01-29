import pygame

from UserInterfafce.intention import Intent


class Screen(pygame.Surface):
    def __init__(self, screen, theme):
        super(Screen, self).__init__(screen.get_size())
        self.parent_screen = screen
        self.theme = theme
        self.elements = list()
        self.intent = None

    def draw(self, tick):
        self.blit(self.theme["background"], (0, 0))
        for element in self.elements:
            element.draw(tick)
        self.parent_screen.blit(self, (0, 0))

    def click(self, pos):
        for element in self.elements:
            element.click(pos)

    def add_element(self, element):
        self.elements.append(element)

    def set_theme(self, theme):
        self.theme = theme

    def set_intent(self, intent: Intent):
        self.intent = intent
