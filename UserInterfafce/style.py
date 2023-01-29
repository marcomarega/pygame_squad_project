class Style:
    def __init__(self, main_color, background_color, font_size):
        self.main_color = main_color
        self.background_color = background_color
        self.font_size = font_size


class Theme:
    def __init__(self, **styles):
        self.styles = styles

    def __getitem__(self, item):
        return self.styles[item]
