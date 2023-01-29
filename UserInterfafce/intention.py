class Intent:
    def __init__(self,):
        self.to_screen = None
        self.args = None
        self.has_intention = False

    def set_intent(self, to_screen, *args):
        self.to_screen = to_screen
        self.args = args
        self.has_intention = True

    def get_screen(self, screen):
        screen = self.to_screen(screen, self, *self.args)
        self.to_screen = None
        self.args = None
        self.has_intention = False
        return screen
