import pygame

pygame.init()
FPS = 60
clock = pygame.time.Clock()
SIZE = WIDTH, HEIGHT = 1200, 700
display = pygame.display.set_mode(SIZE)
from themes import *

SCROLL_SHIFT = 25

GAME_NAME = "BOXSCRAPPER"
LEVEL_EXT = ".lvl"
SAVE_EXT = ".save"
BACKTOGAMESCREEN = pygame.USEREVENT + 1
