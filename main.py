import pygame

from menu_screens import MainMenuScreen

pygame.init()
FPS = 60
clock = pygame.time.Clock()
SIZE = WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode(SIZE)

if __name__ == "__main__":
    main_menu_screen = MainMenuScreen(screen)

    running = True
    pressed_coordinate = None
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                pressed_coordinate = event.pos
            if event.type == pygame.MOUSEBUTTONUP and pressed_coordinate is not None:
                main_menu_screen.click(pressed_coordinate)
        screen.fill((0, 0, 0))
        main_menu_screen.draw(clock.tick(FPS))
        pygame.display.flip()
