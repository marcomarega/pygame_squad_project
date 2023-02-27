import pygame

from functions import load_image
from music import MusicController

pygame.init()
FPS = 60
clock = pygame.time.Clock()
SIZE = WIDTH, HEIGHT = 1200, 700
display = pygame.display.set_mode(SIZE)
icon_image = load_image("res\\image\\logo.png")
pygame.display.set_icon(icon_image)
from themes import *

SCROLL_SHIFT = 25

GAME_NAME = "BOXSCRAPPER"
pygame.display.set_caption(GAME_NAME)
LEVEL_EXT = ".lvl"
SAVE_EXT = ".save"
BACKTOGAMESCREEN = pygame.USEREVENT + 1

music_controller = MusicController("res\\music\\Snap! - The Power (dizer.net).mp3", "res\\music\\Herbie Hancock - Rockit (dizer.net).mp3")
