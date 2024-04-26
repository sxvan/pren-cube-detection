from models.color import Color
from models.cube_position import CubePosition
from models.region import Region


class CubeConfig:
    def __init__(self, side_regions: (CubePosition, Region), edge_regions: (CubePosition, Region), colors: [Color]):
        self.side_regions = {}
        for position, regions in side_regions.items():
            self.side_regions[CubePosition[position.upper()]] = [Region(**region) for region in regions]

        self.edge_regions = {}
        for position, regions in edge_regions.items():
            self.edge_regions[CubePosition[position.upper()]] = [Region(**region) for region in regions]

        self.colors = [Color(**color) for color in colors]
        