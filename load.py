import pygame

from UserInterfafce.intention import Intent

pygame.init()
FPS = 60
clock = pygame.time.Clock()
SIZE = WIDTH, HEIGHT = 800, 600
display = pygame.display.set_mode(SIZE)
intent = Intent()
from themes import *
