import pygame
import sys
import os

from UserInterfafce.button import Button
from functions import load_image

pygame.init()
size = WIDTH, HEIGHT = 600, 450
screen = pygame.display.set_mode(size)

FPS = 50
clock = pygame.time.Clock()
btns_coords = {}


def checking_coords(coords):
    for btn in btns_coords.keys():
        if btn[0] <= coords[0] <= btn[0] + btn[2] and btn[1] <= coords[1] <= btn[1] + btn[3]:
            return (True, btns_coords[btn])
    return (False,)


def terminate():
    pygame.quit()
    sys.exit()


def start_screen(k):
    intro_text = ["НАЗВАНИЕ ИГРЫ", "",
                  "Начать игру",
                  "Продолжить игру",
                  "Звук", "Выйти из игры"]

    fon_name_im = os.path.join('..\\res\\image', f"bg{k}.jpg")
    fon = pygame.transform.scale(load_image(fon_name_im), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        if k == 2:
            color = 'white'
        else:
            color = 'black'
        string_rendered = font.render(line, True, color)
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
        if intro_text.index(line) > 1:
            pygame.draw.rect(screen, color, (intro_rect.x - 3, intro_rect.y - 3,
                                             intro_rect.width + 6, intro_rect.height + 6), 2)
            btns_coords[
                (intro_rect.x - 3, intro_rect.y - 3, intro_rect.width + 6, intro_rect.height + 6)] = 3
    a = btns_coords.copy()
    index = 0
    for i in a.keys():
        if index <= 1:
            del btns_coords[i]
            index += 1
        else:
            break

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                k = checking_coords(event.pos)
                if len(k) == 2 and k[1] == 3:
                    return
        pygame.display.flip()
        clock.tick(FPS)


def choice():
    text = "Выберите тему"
    font = pygame.font.Font(None, 30)
    string_rendered = font.render(text, True, pygame.Color('white'))
    text_rect = string_rendered.get_rect()
    text_rect.x = 50
    text_rect.y = 10
    screen.blit(string_rendered, text_rect)

    # text_for_btns = ["Дневная", "Ночная"]
    # text_coord = 40
    # for line in text_for_btns:
    #     string_rendered = font.render(line, True, pygame.Color('white'))
    #     intro_rect = string_rendered.get_rect()
    #     intro_rect.y = 120
    #     intro_rect.x = text_coord
    #     screen.blit(string_rendered, intro_rect)
    #     pygame.draw.rect(screen, 'white', (intro_rect.x - 3, intro_rect.y - 3,
    #                                        intro_rect.width + 6, intro_rect.height + 6), 2)
    #     btns_coords[
    #         (intro_rect.x - 3, intro_rect.y - 3, intro_rect.width + 6, intro_rect.height + 6)] = text_for_btns.index(
    #         line) + 1
    #     text_coord += 100

    buttons = [
        Button(screen, (100, 40), (20, 60), (40, 40, 40,), "Дневная", (225, 225, 225), 30),
        Button(screen, (100, 40), (130, 60), (40, 40, 40,), "Ночная", (225, 225, 225), 30)
    ]
    buttons[0].connect(lambda: start_screen(2))
    buttons[1].connect(lambda: start_screen(3))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for button in buttons:
                    button.click(event.pos)
        for button in buttons:
            button.draw(1)
        pygame.display.flip()
        clock.tick(FPS)


k = choice()
start_screen(k)
