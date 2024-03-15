from models.color import Color
from models.orientation import Orientation
from models.region import Region


class QuadrantConfig:
    def __init__(self, regions, colors):
        self.regions = {}
        for position, regions in regions.items():
            self.regions[Orientation[position.upper()]] = [Region(**region) for region in regions]

        self.colors = [Color(**color) for color in colors]
