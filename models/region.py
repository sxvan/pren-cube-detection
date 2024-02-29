from models.region_position import RegionPosition


class Region:
    def __init__(self, position, coords, width, height):
        self.position = position
        self.cords = tuple(coords)
        self.width = width
        self.height = height
