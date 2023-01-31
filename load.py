import pygame

pygame.init()
FPS = 60
clock = pygame.time.Clock()
SIZE = WIDTH, HEIGHT = 800, 600
display = pygame.display.set_mode(SIZE)
from themes import *

GAME_NAME = "BOXSCRAPPER"
SAVES_COUNT = 3
SAVE_EXT = ".save"
