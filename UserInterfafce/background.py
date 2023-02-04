import pygame

from functions import load_image


class Background(pygame.Surface):
    def __init__(self, image_filename=None, color=None):
        if image_filename is None and color is None or image_filename is not None and color is not None:
            raise TypeError("There must be or image, or color, not both.")
        if image_filename is not None:
            image = load_image(image_filename)
            super(Background, self).__init__(image.get_size(), pygame.SRCALPHA, 32)
            self.blit(image, (0, 0))
        else:
            super(Background, self).__init__((3000, 3000), pygame.SRCALPHA, 32)
            self.fill(color)
