from random import choice

import pygame

from UserInterfafce.screen_elements import ScreenElement
from filework import Level
from functions import load_image

PLAYER = "@"
BOX = "#"
WALL = "X"
FINISH = "0"
CELL = "."
VOID = " "

PLAYER_IMG_SRC = load_image("res\\image\\player.png")
BOX_IMG_SRC = load_image("res\\image\\box.png")
WALL_IMGS_SRC = [load_image("res\\image\\wall1.png"), load_image("res\\image\\wall2.png")]
FINISH_IMG_SRC = load_image("res\\image\\finish.png")

PLAYER_IMG = PLAYER_IMG_SRC
BOX_IMG = BOX_IMG_SRC
WALL_IMGS = WALL_IMGS_SRC
FINISH_IMG = FINISH_IMG_SRC


def get_pos_by_direction(pos0, direction):
    pos = list(pos0)
    if direction == "d":
        pos[1] = pos0[1] + 1
    if direction == "u":
        pos[1] = pos0[1] - 1
    if direction == "r":
        pos[0] = pos0[0] + 1
    if direction == "l":
        pos[0] = pos0[0] - 1
    return tuple(pos)


class GameElement(pygame.Surface):
    def __init__(self, image, board, pos=(0, 0)):
        super(GameElement, self).__init__(image.get_size(), pygame.SRCALPHA, 32)
        self.blit(image, (0, 0))
        self.board = board
        self.pos = pos

    def move(self, direction, d=0):
        pass

    def can_move(self, direction, d=0):
        pass

    def can_move_on_empty_board(self, direction):
        pos = get_pos_by_direction(self.pos, direction)
        return 0 <= pos[0] < self.board.get_width() and 0 <= pos[1] < self.board.get_height()

    def draw(self, tick):
        self.board.blit(self, (self.pos[0] * self.board.cell_size, self.pos[1] * self.board.cell_size))


class VoidElement(GameElement):
    def __init__(self, board, pos=(0, 0)):
        super(VoidElement, self).__init__(pygame.Surface((1, 1)), board, pos)

    def can_move(self, *args, **kwargs):
        return True


class Player(GameElement):
    def __init__(self, board, pos=(0, 0)):
        super(Player, self).__init__(PLAYER_IMG, board, pos)

    def move(self, direction, d=0):
        if not self.board.going:
            return
        pos = get_pos_by_direction(self.pos, direction)
        if self.can_move(direction, d):
            self.board.get_upper(pos).move(direction)
            self.board.set_upper(self.pos, VoidElement(self.board, self.pos))
            self.board.set_upper(pos, self)
            self.pos = pos
        return self

    def can_move(self, direction, d=0):
        if d > 0:
            return False
        pos = get_pos_by_direction(self.pos, direction)
        return self.can_move_on_empty_board(direction) and self.board.get_upper(pos).can_move(direction, d + 1)


class Box(GameElement):
    def __init__(self, board, pos=(0, 0)):
        super(Box, self).__init__(BOX_IMG, board, pos)

    def move(self, direction, d=0):
        pos = get_pos_by_direction(self.pos, direction)
        if self.can_move(direction, d):
            self.board.get_upper(pos).move(direction)
            self.board.get_lower(self.pos).deactivate()
            self.board.set_upper(self.pos, VoidElement(self.board, self.pos))
            self.board.get_lower(pos).activate()
            self.board.set_upper(pos, self)
            self.pos = pos
        return self

    def can_move(self, direction, d=0):
        if d > 1:
            return False
        pos = get_pos_by_direction(self.pos, direction)
        return self.can_move_on_empty_board(direction) and self.board.get_upper(pos).can_move(direction, d + 1)


class Wall(GameElement):
    def __init__(self, board, pos=(0, 0)):
        super(Wall, self).__init__(choice(WALL_IMGS), board, pos)

    def can_move(self, direction, d=0):
        return False


class Finish(pygame.Surface):
    def __init__(self, board, pos=(0, 0)):
        image = FINISH_IMG
        super(Finish, self).__init__(image.get_size(), pygame.SRCALPHA, 32)
        self.blit(image, (0, 0))
        self.board = board
        self.pos = pos
        self.activated = False

    def activate(self):
        self.activated = True

    def deactivate(self):
        self.activated = False

    def draw(self, tick):
        self.board.blit(self, (self.pos[0] * self.board.cell_size, self.pos[1] * self.board.cell_size))


class VoidFinish(pygame.Surface):
    def __init__(self, board, pos=(0, 0)):
        super(VoidFinish, self).__init__((1, 1), pygame.SRCALPHA, 32)
        self.activated = False

    def activate(self):
        self.activated = True

    def deactivate(self):
        self.activated = True

    def draw(self, tick):
        pass


class Board(ScreenElement):
    def __init__(self, parent_screen, rect, level: Level):
        global PLAYER_IMG, BOX_IMG, WALL_IMGS, FINISH_IMG
        super(Board, self).__init__(parent_screen, rect)
        self.level = level
        self.player = VoidElement(self)
        self.width = len(self.level.get_map()[0])
        self.height = len(self.level.get_map())
        self.map_upper = [[None for j in range(self.height)] for i in range(self.width)]
        self.map_lower = [[None for j in range(self.height)] for i in range(self.width)]
        self.finishes = list()
        self.cell_size = min(self.rect.width, self.rect.height) // max(self.width, self.height)
        PLAYER_IMG = pygame.transform.scale(PLAYER_IMG_SRC, (self.cell_size, self.cell_size))
        BOX_IMG = pygame.transform.scale(BOX_IMG_SRC, (self.cell_size, self.cell_size))
        WALL_IMGS = [pygame.transform.scale(WALL_IMG_SRC, (self.cell_size, self.cell_size)) for WALL_IMG_SRC in WALL_IMGS_SRC]
        FINISH_IMG = pygame.transform.scale(FINISH_IMG_SRC, (self.cell_size, self.cell_size))
        for j, row in enumerate(level.get_map()):
            for i, chr_element in enumerate(row):
                upper_element = VoidElement(self, (i, j))
                lower_element = VoidFinish(self, (i, j))
                if chr_element == PLAYER:
                    upper_element = self.player = Player(self, (i, j))
                if chr_element == BOX:
                    upper_element = Box(self, (i, j))
                if chr_element == WALL:
                    upper_element = Wall(self, (i, j))
                if chr_element == FINISH:
                    self.finishes.append(lower_element := Finish(self, (i, j)))
                self.map_upper[i][j] = upper_element
                self.map_lower[i][j] = lower_element
        self.going = True

    def refresh_going(self):
        self.going = False
        for finish in self.finishes:
            self.going = self.going or not finish.activated

    def get_upper(self, pos):
        return self.map_upper[pos[0]][pos[1]]

    def get_lower(self, pos):
        return self.map_lower[pos[0]][pos[1]]

    def set_upper(self, pos, element: GameElement):
        self.map_upper[pos[0]][pos[1]] = element
        self.refresh_going()

    def set_lower(self, pos, element: GameElement):
        self.map_lower[pos[0]][pos[1]] = element
        self.refresh_going()

    def get_width(self):
        return self.width

    def get_height(self):
        return self.height

    def push_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.player.move("u")
            if event.key == pygame.K_DOWN:
                self.player.move("d")
            if event.key == pygame.K_LEFT:
                self.player.move("l")
            if event.key == pygame.K_RIGHT:
                self.player.move("r")

    def draw(self, tick):
        if not super(Board, self).draw(tick):
            return False
        for i in range(self.width):
            for j in range(self.height):
                self.map_lower[i][j].draw(tick)
                self.map_upper[i][j].draw(tick)
        self.parent_screen.blit(self, self.rect.topleft)
        return True
