from models.color import Color
import json

from models.cube_position import CubePosition
from models.quadrant_region_position import QuadrantRegionPosition
from models.region import Region


class Config:
    def __init__(self, stream_path, min_color_coverage, colors, side_regions, edge_regions, quadrant_regions):
        self.stream_path = stream_path

        self.side_regions = []
        for position, region in side_regions.items():
            self.side_regions.append(Region(position=CubePosition[position.upper()], **region))

        self.edge_regions = []
        for position, region in edge_regions.items():
            self.edge_regions.append(Region(position=CubePosition[position.upper()], **region))

        self.quadrant_regions = []
        for position, region in quadrant_regions.items():
            self.quadrant_regions.append(Region(position=QuadrantRegionPosition[position.upper()], **region))

        self.min_color_coverage = min_color_coverage
        self.colors = [Color(**color) for color in colors]

    @classmethod
    def from_json(cls, json_file_path):
        with open(json_file_path) as f:
            data = json.load(f)
        return cls(**data)
