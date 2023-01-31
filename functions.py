import sys
import os
import pygame

from load import WIDTH


def load_image(fullname, colorkey=None):
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def hor_center(screen_width, element_width):
    return (screen_width - element_width) // 2


def ver_center(screen_height, element_height):
    return (screen_height - element_height) // 2


def terminate():
    pygame.quit()
    sys.exit()
