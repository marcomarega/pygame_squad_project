import pygame

from functions import load_image


class Background(pygame.Surface):
    def __init__(self, size, image_filename=None, color=None):
        super(Background, self).__init__(size)
        if image_filename is None and color is None or image_filename is not None and color is not None:
            raise TypeError("There must be or image, or color, not both.")

        if image_filename is not None:
            self.blit(load_image(image_filename))
        if color is not None:
            self.fill(color)
