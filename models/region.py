from models.cube_position import CubePosition
from models.quadrant_region_position import QuadrantRegionPosition
from typing import Union



class Region:
    def __init__(self, position: Union[CubePosition, QuadrantRegionPosition], coords, width, height, when_missing=[]):
        self.position = position
        self.cords = tuple(coords)
        self.width = width
        self.height = height

        self.when_missing = []
        for position in when_missing:
            self.when_missing.append(CubePosition[position.upper()])
