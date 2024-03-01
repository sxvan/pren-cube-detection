from models.color import Color
import json

from models.quadrant_region_position import QuadrantRegionPosition
from models.region import Region
from models.cube_region_position import CubeRegionPosition


class Config:
    def __init__(self, stream_path, min_color_coverage, colors, side_regions, edge_regions, quadrant_regions):
        self.stream_path = stream_path

        self.side_regions = [Region(position=CubeRegionPosition[position.upper()], **region) for position, region in side_regions.items()]
        self.edge_regions = [Region(position=CubeRegionPosition[position.upper()], **region) for position, region in edge_regions.items()]
        self.quadrant_regions = [Region(position=QuadrantRegionPosition[position.upper()], **region) for position, region in quadrant_regions.items()]

        self.min_color_coverage = min_color_coverage
        self.colors = [Color(**color) for color in colors]

    @classmethod
    def from_json(cls, json_file_path):
        with open(json_file_path) as f:
            data = json.load(f)
        return cls(**data)
