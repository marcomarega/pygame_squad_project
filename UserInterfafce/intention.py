class Intent:
    def __init__(self, parent=None):
        self.to_screen = None
        self.args = None
        self.has_intention = False
        self.parent = parent

    def set_intent(self, to_screen, *args):
        self.to_screen = to_screen
        self.args = args
        self.has_intention = True
        if self.parent is not None:
            self.parent.push_intent()

    def get_screen(self, screen):
        screen = self.to_screen(screen, self, *self.args)
        self.to_screen = None
        self.args = None
        self.has_intention = False
        return screen
