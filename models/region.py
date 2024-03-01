from models.cube_region_position import CubeRegionPosition


class Region:
    def __init__(self, position, coords, width, height):
        self.position = position
        self.cords = tuple(coords)
        self.width = width
        self.height = height
