from load import *
from UserInterfafce.intention import Intent
from menu_screens import MainMenuScreen

if __name__ == "__main__":
    intent = Intent()
    from themes import day_theme
    cur_screen = MainMenuScreen(display, intent, day_theme)

    running = True
    pressed_coordinate = None
    while running:
        if intent.has_intention:
            cur_screen = intent.get_screen(display)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                pressed_coordinate = event.pos
            if event.type == pygame.MOUSEBUTTONUP and pressed_coordinate is not None:
                cur_screen.click(pressed_coordinate)
        display.fill((0, 0, 0))
        cur_screen.draw(clock.tick(FPS))
        pygame.display.flip()
