from filework import FileBase
from load import *
from UserInterfafce.intention import Intent
from menu_screens import MainMenuScreen

if __name__ == "__main__":
    intent = Intent()
    file_base = FileBase("res")
    from themes import day_theme
    cur_screen = MainMenuScreen(display, intent, file_base, day_theme)

    running = True
    while running:
        if intent.has_intention:
            cur_screen = intent.get_screen(display)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            else:
                cur_screen.push_event(event)
        display.fill((0, 0, 0))
        cur_screen.draw(clock.tick(FPS))
        pygame.display.flip()
