import pygame

from intention import Intent
from menu_screens import MainMenuScreen

pygame.init()
FPS = 60
clock = pygame.time.Clock()
SIZE = WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode(SIZE)

if __name__ == "__main__":
    intent = Intent()
    cur_screen = MainMenuScreen(screen, intent)

    running = True
    pressed_coordinate = None
    while running:
        if intent.has_intention:
            cur_screen = intent.get_screen(screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                pressed_coordinate = event.pos
            if event.type == pygame.MOUSEBUTTONUP and pressed_coordinate is not None:
                cur_screen.click(pressed_coordinate)
        screen.fill((0, 0, 0))
        cur_screen.draw(clock.tick(FPS))
        pygame.display.flip()
