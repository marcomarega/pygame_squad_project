from pygame import Rect

from UserInterfafce.background import Background
from UserInterfafce.screen_elements import Button, TextPlain
from UserInterfafce.screen import Screen
from UserInterfafce.style import Style
from functions import terminate
from load import SAVES_COUNT, GAME_NAME
from themes import night_theme, day_theme


class MainMenuScreen(Screen):
    def __init__(self, display, intent, theme, *args):
        super(MainMenuScreen, self).__init__(display, theme)
        self.intent = intent

        self.add_element(TextPlain(self, Rect(10, 10, 300, 50), GAME_NAME, self.theme["header"]))
        self.add_element(Button(self, Rect(10, 70, 150, 50), "Начать игру")
                         .connect(lambda: print(1)))
        self.add_element(Button(self, Rect(10, 130, 150, 50), "Продолжить игру")
                         .connect(lambda: print(2)))
        self.add_element(Button(self, Rect(10, 190, 150, 50), "Настройки")
                         .connect((lambda: self.intent.set_intent(SettingsScreen, self.theme))))
        self.add_element(Button(self, Rect(10, 250, 150, 50), "Выйти из игры")
                         .connect(lambda: terminate()))
        self.add_element(Button(self, Rect(10, 310, 150, 50), "Test")
                         .connect(lambda: self.intent.set_intent(PauseMenuScreen, self.theme)))


class SettingsScreen(Screen):
    def __init__(self, display, intent, theme, *args):
        super(SettingsScreen, self).__init__(display, theme)
        self.intent = intent

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
        self.add_element(
            Button(self, Rect(10, 130, 150, 50), "Назад")
            .connect(lambda: self.intent.set_intent(MainMenuScreen, self.theme))
        )


class PauseMenuScreen(Screen):
    def __init__(self, screen, intent, theme, *args):
        super(PauseMenuScreen, self).__init__(screen, theme)
        self.intent = intent
        self.args = args

        self.add_element(Button(self, Rect((self.display.get_width() - 200)//2, 215, 200, 50), "Сохранить и выйти")
                         .connect(lambda: self.intent.set_intent(MainMenuScreen, self.theme)))
        self.add_element(Button(self, Rect((self.display.get_width() - 200)//2, 275, 200, 50), "Перейти в меню настроек")
                         .connect(lambda: self.intent.set_intent(SettingsScreen, self.theme)))
        self.add_element(Button(self, Rect((self.display.get_width() - 200)//2, 335, 200, 50), "Продолжить")
                         .connect(lambda: print(9)))
