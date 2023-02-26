import pygame
from pygame import Rect

from UserInterfafce.screen import Screen
from UserInterfafce.screen_elements import Button, TextPlain, ScrollArea, EditText, ScreenKeeper
from UserInterfafce.style import Style
from filework import FileBase
from functions import terminate, hor_center
from load import GAME_NAME, BACKTOGAMESCREEN
from themes import night_theme, day_theme
from game.elements import Board


class MainMenuScreen(Screen):
    def __init__(self, display, intent, file_base, theme):
        super(MainMenuScreen, self).__init__(display, intent, file_base, theme)

        self.add_element(TextPlain(self, Rect(10, 10, 300, 50), GAME_NAME, self.theme.data["header"]))
        self.add_element(Button(self, Rect(10, 70, 150, 50), "Новая игра")
                         .connect(lambda: self.intent.set_intent(NewGameScreen, self.file_base, self.theme)))
        self.add_element(Button(self, Rect(10, 130, 150, 50), "Продолжить игру")
                         .connect(lambda: self.intent.set_intent(ChoiceSaveScreen, self.file_base, self.theme)))
        self.add_element(Button(self, Rect(10, 190, 150, 50), "Настройки")
                         .connect((lambda: self.intent.set_intent(SettingsScreen, self.file_base, self.theme,
                                                                  MainMenuScreen))))
        self.add_element(Button(self, Rect(10, 250, 150, 50), "Выйти из игры")
                         .connect(lambda: terminate()))
        self.add_element(Button(self, Rect(10, 310, 150, 50), "Test")
                         .connect(lambda: self.intent.set_intent(LevelPlaying, self.file_base, self.theme)))


class NewGameScreen(Screen):
    def __init__(self, display, intent, file_base: FileBase, theme):
        super(NewGameScreen, self).__init__(display, intent, file_base, theme)

        self.add_element(
            TextPlain(self, Rect(10, 10, 330, 50), "Новое сохранение", self.theme.data["header"])
        )

        self.add_element(
            EditText(self, Rect(20, 70, 300, 50))
            .connect_text_handler(self.start_new_game)
        )

        self.add_element(Button(self, Rect(10, 530, 150, 50), "Назад")
                         .connect(lambda: self.intent.set_intent(MainMenuScreen, self.file_base, self.theme)))

    def start_new_game(self, name):
        if name.strip() == "":
            return
        self.file_base.new_save(name)
        save = self.file_base.save_base[name]
        self.intent.set_intent(GameScreen, self.file_base, self.theme, save)


class ChoiceSaveScreen(Screen):
    def __init__(self, display, intent, file_base: FileBase, theme):
        super(ChoiceSaveScreen, self).__init__(display, intent, file_base, theme)

        self.add_element(
            scroll_area := ScrollArea(self, Rect(10, 10, 500, 500))
        )
        save_button_dh = 60
        for i, save_name in enumerate(self.file_base.get_saves()):
            scroll_area.add_element(
                button := Button(scroll_area, Rect(10, 10 + i * save_button_dh, 480, 50), save_name)
                .add_args(self.file_base.save_base[save_name])
                .connect(lambda save: self.intent.set_intent(GameScreen, self.file_base, self.theme, save))
            )
            button.save_name = save_name

        self.add_element(
            Button(self, Rect(10, scroll_area.rect.height + 20, 150, 50), "Назад")
            .connect(lambda: self.intent.set_intent(MainMenuScreen, self.file_base, self.theme))
        )


class SettingsScreen(Screen):
    def __init__(self, display, intent, file_base, theme, from_screen, from_save=None):
        super(SettingsScreen, self).__init__(display, intent, file_base, theme)
        self.from_screen = from_screen
        self.from_save = from_save

        self.add_element(TextPlain(self, Rect(10, 10, 150, 50), "Параметры"))
        self.add_element(
            Button(self, Rect(10, 70, 150, 50), "Ночь",
                   Style("white", "black", -50, self.theme.data["text"].font_size))
            .connect(lambda: self.set_theme(night_theme))
        )
        self.add_element(
            Button(self, Rect(170, 70, 150, 50), "День",
                   Style("black", "white", 50, self.theme.data["text"].font_size))
            .connect(lambda: self.set_theme(day_theme))
        )
        if self.from_screen == GameScreen:
            self.add_element(
                Button(self, Rect(10, 130, 150, 50), "Назад")
                .connect(
                    lambda: self.display.push_event_to_parent_screen(
                        pygame.event.Event(BACKTOGAMESCREEN, theme=self.theme)))
            )
        else:
            self.add_element(
                Button(self, Rect(10, 130, 150, 50), "Назад")
                .connect(lambda: self.intent.set_intent(self.from_screen, self.file_base, self.theme))
            )


class GameScreen(Screen):
    def __init__(self, display, intent, file_base, theme, save):
        super(GameScreen, self).__init__(display, intent, file_base, theme)
        self.save = save

        self.add_element(Button(self, Rect(20, 50, 200, 50), "Сохранить и выйти")
                         .connect(lambda: self.saving()))
        self.add_element(
            Button(self, Rect(20, 130, 200, 50), "Перейти в меню настроек")
            .connect(lambda: self.screen_keeper1.show()))
        self.add_element(ScreenKeeper(self, Rect(250, 50, 500, 500))
                         .set_current_screen(LevelMenuScreen, self.theme, self.save))
        self.add_element(screen_keeper1 := ScreenKeeper(self, self.get_rect())
                         .set_current_screen(SettingsScreen, self.theme, GameScreen, self.save).hide())
        self.screen_keeper1 = screen_keeper1

    def saving(self):
        with open(self.save.filename, mode="w", encoding="utf-8") as file:
            file.write(" ".join(self.save.passed_levels))
        self.intent.set_intent(MainMenuScreen, self.file_base, self.theme)

    def get_screen_keeper1(self):
        return self.screen_keeper1

    def push_event(self, event):
        if event.type == BACKTOGAMESCREEN:
            self.screen_keeper1.hide()
            self.theme.data = event.theme.data
        else:
            super().push_event(event)


class LevelMenuScreen(Screen):
    def __init__(self, screen, intent, file_base, theme, save):
        super(LevelMenuScreen, self).__init__(screen, intent, file_base, theme)
        self.save = save

        self.add_element(
            scroll_area := ScrollArea(self, screen.get_rect())
        )

        save_button_dh = 60
        for i, level in enumerate(self.file_base.get_levels()):
            scroll_area.add_element(
                button := Button(scroll_area, Rect(10, 10 + i * save_button_dh, 480, 50), level.get_name(),
                                 self.checking_passing_levels(level))
                .add_args(self.file_base.level_base[i])
                .connect(lambda level1: self.display.set_current_screen(LevelPlaying,
                                                                        self.display.get_parent_screen().theme.data[
                                                                                "level_playing_theme"],
                                                                        self.save, level1))
            )
            button.level_name = level

    def checking_passing_levels(self, level):
        if self.save.is_passed(level):
            return Style((255, 255, 255), (0, 255, 0), 30, 20)
        return Style((255, 255, 255), (255, 0, 0), 30, 20)


class LevelPlaying(Screen):
    def __init__(self, screen, intent, file_base, theme, save, level):
        super(LevelPlaying, self).__init__(screen, intent, file_base, theme)
        self.level = level
        self.save = save

        self.add_element(board := Board(self, Rect(190, 120, 500, 500), self.level, 25))
        self.board = board

    def push_event(self, event):
        super().push_event(event)
        if not self.board.going:
            self.display.set_current_screen(FinishScreen, self.display.get_parent_screen().theme.data["screen_keeper_theme"],
                                            self.save, self.level)


class FinishScreen(Screen):
    def __init__(self, screen, intent, file_base, theme, save, level):
        super(FinishScreen, self).__init__(screen, intent, file_base, theme)
        self.level = level
        self.save = save

        self.add_element(TextPlain(self, Rect(10, 10, 480, 50), "Вы победили", self.theme.data["header"]))
        self.add_element(Button(self, Rect(175, 310, 200, 50), "Выбрать новый уровень")
                         .connect(lambda: self.display.set_current_screen(LevelMenuScreen,
                                                                          self.display.get_parent_screen().theme.data[
                                                                              "screen_keeper_theme"],
                                                                          self.save)))
        self.save.new_passed_level(self.level)


class PauseMenuScreen(Screen):
    def __init__(self, screen, intent, file_base, theme):
        super(PauseMenuScreen, self).__init__(screen, intent, file_base, theme)
        self.add_element(Button(self, Rect(hor_center(screen.get_width(), 200), 215, 200, 50), "Сохранить и выйти")
                         .connect(lambda: self.intent.set_intent(MainMenuScreen, self.file_base, self.theme)))
        self.add_element(
            Button(self, Rect(hor_center(screen.get_width(), 200), 275, 200, 50), "Перейти в меню настроек")
            .connect(lambda: self.intent.set_intent(SettingsScreen, self.file_base, self.theme,
                                                    PauseMenuScreen)))
        self.add_element(Button(self, Rect(hor_center(screen.get_width(), 200), 335, 200, 50), "Продолжить")
                         .connect(lambda: print(1)))
