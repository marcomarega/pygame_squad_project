import pygame


class Screen(pygame.Surface):
    def __init__(self, screen, background):
        super(Screen, self).__init__(screen.get_size())
        self.parent_screen = screen
        self.background = background
        self.elements = list()

    def draw(self, tick):
        self.fill((0, 0, 0))
        self.blit(self.background, (0, 0))
        for element in self.elements:
            element.draw(tick)
        self.parent_screen.blit(self, (0, 0))

    def click(self, pos):
        for element in self.elements:
            element.click(pos)

    def add_element(self, element):
        self.elements.append(element)
