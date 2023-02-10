import os
from datetime import datetime

from pygame import Rect

from UserInterfafce.screen_elements import Button, TextPlain, ScrollArea, EditText, ScreenKeeper
from UserInterfafce.screen import Screen
from UserInterfafce.style import Style
from filework import FileBase
from functions import terminate, hor_center
from load import GAME_NAME
from themes import night_theme, day_theme


class MainMenuScreen(Screen):
    def __init__(self, display, intent, file_base, theme, *args):
        super(MainMenuScreen, self).__init__(display, intent, file_base, theme)

        self.add_element(TextPlain(self, Rect(10, 10, 300, 50), GAME_NAME, self.theme["header"]))
        self.add_element(Button(self, Rect(10, 70, 150, 50), "Начать игру")
                         .connect(lambda: self.intent.set_intent(NewGameScreen, self.file_base, self.theme)))
        self.add_element(Button(self, Rect(10, 130, 150, 50), "Продолжить игру")
                         .connect(lambda: self.intent.set_intent(ChoiceSaveScreen, self.file_base, self.theme)))
        self.add_element(Button(self, Rect(10, 190, 150, 50), "Настройки")
                         .connect((lambda: self.intent.set_intent(SettingsScreen, self.file_base, self.theme,
                                                                  MainMenuScreen))))
        self.add_element(Button(self, Rect(10, 250, 150, 50), "Выйти из игры")
                         .connect(lambda: terminate()))
        self.add_element(Button(self, Rect(10, 310, 150, 50), "Test")
                         .connect(lambda: self.intent.set_intent(PauseMenuScreen, self.file_base, self.theme)))


class NewGameScreen(Screen):
    def __init__(self, display, intent, file_base: FileBase, theme, *args):
        super(NewGameScreen, self).__init__(display, intent, file_base, theme)

        self.add_element(
            TextPlain(self, Rect(10, 10, 330, 50), "Новое сохранение", self.theme["header"])
        )

        self.add_element(
            EditText(self, Rect(20, 70, 300, 50))
            .connect_text_handler(self.start_new_game)
        )

        self.add_element(Button(self, Rect(10, 530, 150, 50), "Назад")
                         .connect(lambda: self.intent.set_intent(MainMenuScreen, self.file_base, self.theme)))

    def start_new_game(self, name):
        self.file_base.new_save(name)
        save = self.file_base.save_base[name]
        self.intent.set_intent(GameScreen, self.file_base, self.theme, save)


class ChoiceSaveScreen(Screen):
    def __init__(self, display, intent, file_base: FileBase, theme, *args):
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
                   Style("white", "black", -50, self.theme["text"].font_size))
            .connect(lambda: self.set_theme(night_theme))
        )
        self.add_element(
            Button(self, Rect(170, 70, 150, 50), "День",
                   Style("black", "white", 50, self.theme["text"].font_size))
            .connect(lambda: self.set_theme(day_theme))
        )
        if self.from_screen == GameScreen:
            self.add_element(
                Button(self, Rect(10, 130, 150, 50), "Назад")
                .connect(lambda: self.intent.set_intent(self.from_screen, self.file_base, self.theme, self.from_save))
            )
        else:
            self.add_element(
                Button(self, Rect(10, 130, 150, 50), "Назад")
                .connect(lambda: self.intent.set_intent(self.from_screen, self.file_base, self.theme))
            )


class GameScreen(Screen):
    def __init__(self, display, intent, file_base, theme, *args):
        super(GameScreen, self).__init__(display, intent, file_base, theme)
        self.args = args

        self.add_element(ScreenKeeper(self, Rect(400, 50, 500, 350)))
        self.add_element(Button(self, Rect(50, 50, 200, 50), "Сохранить и выйти")
                         .connect(lambda: self.saving()))
        self.add_element(
            Button(self, Rect(50, 130, 200, 50), "Перейти в меню настроек")
            .connect(lambda: self.intent.set_intent(SettingsScreen, self.file_base, self.theme,
                                                    GameScreen, self.args[0])))

    def saving(self):
        for save in self.file_base.get_saves():
            if save == self.args[0].get_name():
                os.remove(os.getcwd() + '\\res\\save\\' + save + '.save')
                self.file_base.del_save(save)
                self.file_base.new_save(save)
                break
        self.intent.set_intent(MainMenuScreen, self.file_base, self.theme)


class PauseMenuScreen(Screen):
    def __init__(self, screen, intent, file_base, theme):
        super(PauseMenuScreen, self).__init__(screen, intent, file_base, theme)

        self.add_element(Button(self, Rect(hor_center(screen.get_width(), 200), 215, 200, 50), "Сохранить и выйти")
                         .connect(lambda: self.intent.set_intent(MainMenuScreen, self.file_base, self.theme)))
        self.add_element(Button(self, Rect(hor_center(screen.get_width(), 200), 275, 200, 50), "Перейти в меню настроек")
                         .connect(lambda: self.intent.set_intent(SettingsScreen, self.file_base, self.theme,
                                                                 PauseMenuScreen)))
        self.add_element(Button(self, Rect(hor_center(screen.get_width(), 200), 335, 200, 50), "Продолжить")
                         .connect(lambda: print(1)))
