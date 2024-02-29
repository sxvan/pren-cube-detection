from models.color_range import ColorRange


class Color:
    def __init__(self, name, color_ranges):
        self.name = name
        self.color_ranges = [ColorRange(**color_range) for color_range in color_ranges]
