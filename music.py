import pygame


class MusicController:

    def __init__(self, menu_music, game_music):
        self.menu = menu_music
        self.game = game_music
        self.volume = 1
        pygame.mixer.music.load(self.menu)

    def main_menu_music_on(self):
        pygame.mixer.music.stop()
        pygame.mixer.music.load(self.menu)
        pygame.mixer.music.play(-1)

    def game_music_on(self):
        pygame.mixer.music.stop()
        pygame.mixer.music.load(self.game)
        pygame.mixer.music.play(-1)

    def volume_change(self, increasing):
        if increasing:
            if self.volume != 1:
                self.volume += 0.05
        else:
            if self.volume != 0:
                self.volume -= 0.05
        pygame.mixer.music.set_volume(self.volume)

