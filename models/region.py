from models.cube_position import CubePosition


class Region:
    def __init__(self, position: CubePosition, coords, width, height, when_missing=[]):
        self.position = position
        self.cords = tuple(coords)
        self.width = width
        self.height = height

        self.when_missing = []
        for position in when_missing:
            self.when_missing.append(CubePosition[position.upper()])
