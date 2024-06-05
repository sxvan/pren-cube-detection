from models.color import Color
from models.cube_position import CubePosition
from models.region import Region


class CubeConfig:
    def __init__(self, use_smart_regions: bool, side_regions: (CubePosition, Region), edge_regions: (CubePosition, Region), colors: [Color]):
        self.side_regions = {}
        for position, regions in side_regions.items():
            self.side_regions[CubePosition[position.upper()]] = [Region(**region) for region in regions
                                                                 if not self.is_smart_region(region) or use_smart_regions ]

        self.edge_regions = {}
        for position, regions in edge_regions.items():
            self.edge_regions[CubePosition[position.upper()]] = [Region(**region) for region in regions
                                                                 if not self.is_smart_region(region) or use_smart_regions ]

        self.colors = [Color(**color) for color in colors]

    def is_smart_region(self, region: Region) -> bool:
        if 'when_different' in region or 'when_missing' in region or 'only_missing' in region:
            return True

        return False
        