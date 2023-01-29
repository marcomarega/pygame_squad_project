from UserInterfafce.button import Button
from UserInterfafce.screen import Screen
from UserInterfafce.text_plain import Text
from functions import load_image, terminate


class MainMenuScreen(Screen):
    def __init__(self, screen, intent, *args):
        background = load_image("res\\image\\bg_main.jpg")
        super(MainMenuScreen, self).__init__(screen, background)
        self.parent_screen = screen
        self.intent = intent
        self.args = args

        self.add_element(Text(self, (150, 50), (10, 10), (255, 255, 255),
                              "Название игры"))
        self.add_element(Button(self, (150, 50), (10, 70), (100, 20, 45),
                                "Начать игру", (255, 255, 255))
                         .connect(lambda: print(1)))
        self.add_element(Button(self, (150, 50), (10, 130), (100, 20, 45),
                                "Продолжить игру", (255, 255, 255))
                         .connect(lambda: print(2)))
        self.add_element(Button(self, (150, 50), (10, 190), (100, 20, 45),
                                "Настройки", (255, 255, 255))
                         .connect((lambda: self.intent.set_intent(SettingsScreen))))
        self.add_element(Button(self, (150, 50), (10, 250), (100, 20, 45),
                                "Выйти из игры", (255, 255, 255))
                         .connect(lambda: terminate()))


class SettingsScreen(Screen):
    def __init__(self, screen, intent, *args):
        background = load_image("res\\image\\bg_main.jpg")
        super(SettingsScreen, self).__init__(screen, background)
        self.parent_screen = screen
        self.intent = intent
        self.args = args

        self.add_element(
            Text(self, (150, 50), (10, 10), (255, 255, 255),
                 "Параметры")
        )
        self.add_element(
            Button(self, (150, 50), (10, 70), (0, 0, 200),
                   "Назад", "white")
            .connect(lambda: self.intent.set_intent(MainMenuScreen))
        )
