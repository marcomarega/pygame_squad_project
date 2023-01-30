import pygame

from UserInterfafce.intention import Intent


class Screen(pygame.Surface):
    def __init__(self, display, theme):
        super(Screen, self).__init__(display.get_size())
        self.display = display
        self.theme = theme
        self.elements = list()
        self.intent = None

    def draw(self, tick):
        self.blit(self.theme["background"], (0, 0))
        for element in self.elements:
            element.draw(tick)
        self.display.blit(self, (0, 0))

    def push_event(self, event):
        for element in self.elements:
            element.push_event(event)

    def add_element(self, element):
        self.elements.append(element)

    def set_theme(self, theme):
        self.theme = theme

    def set_intent(self, intent: Intent):
        self.intent = intent
