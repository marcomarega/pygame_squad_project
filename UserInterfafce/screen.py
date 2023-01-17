import pygame


class Screen(pygame.Surface):
    def __init__(self, screen_size, background):
        super(Screen, self).__init__(screen_size)
        self.background = background

    def draw(self, tick):
        self.blit(self.background, (0, 0))
