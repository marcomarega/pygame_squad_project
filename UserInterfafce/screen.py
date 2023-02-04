import pygame

from UserInterfafce.intention import Intent


class Screen(pygame.Surface):
    def __init__(self, display, intent, file_base, theme):
        super(Screen, self).__init__(display.get_size(), pygame.SRCALPHA, 32)
        self.display = display
        self.intent = intent
        self.file_base = file_base
        self.theme = theme
        self.elements = list()

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
