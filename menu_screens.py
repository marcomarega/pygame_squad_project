from pygame import Rect

from UserInterfafce.background import Background
from UserInterfafce.button import Button
from UserInterfafce.screen import Screen
from UserInterfafce.style import Style
from UserInterfafce.text_plain import Text
from functions import load_image, terminate
from themes import night_theme, day_theme


class MainMenuScreen(Screen):
    def __init__(self, screen, intent, theme, *args):
        super(MainMenuScreen, self).__init__(screen, theme)
        self.parent_screen = screen
        self.theme = theme
        self.intent = intent
        self.args = args

        self.add_element(Text(self, Rect(10, 10, 150, 50), "Название игры"))
        self.add_element(Button(self, Rect(10, 70, 150, 50), "Начать игру")
                         .connect(lambda: print(1)))
        self.add_element(Button(self, Rect(10, 130, 150, 50), "Продолжить игру")
                         .connect(lambda: print(2)))
        self.add_element(Button(self, Rect(10, 190, 150, 50), "Настройки")
                         .connect((lambda: self.intent.set_intent(SettingsScreen, self.theme))))
        self.add_element(Button(self, Rect(10, 250, 150, 50), "Выйти из игры")
                         .connect(lambda: terminate()))


class SettingsScreen(Screen):
    def __init__(self, screen, intent, background, *args):
        super(SettingsScreen, self).__init__(screen, background)
        self.parent_screen = screen
        self.intent = intent
        self.args = args

        self.add_element(Text(self, Rect(10, 10, 150, 50), "Параметры"))
        self.add_element(
            Button(self, Rect(10, 70, 150, 50), "Ночь",
                   Style("white", "black", self.theme["text"].font_size))
            .connect(lambda: self.set_theme(night_theme))
        )
        self.add_element(
            Button(self, Rect(170, 70, 150, 50), "День",
                   Style("black", "white", self.theme["text"].font_size))
            .connect(lambda: self.set_theme(day_theme))
        )
        self.add_element(
            Button(self, Rect(10, 130, 150, 50), "Назад")
            .connect(lambda: self.intent.set_intent(MainMenuScreen, self.theme))
        )
