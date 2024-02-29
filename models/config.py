from models.color import Color
import json

from models.region import Region
from models.region_position import RegionPosition


class Config:
    def __init__(self, stream_path, regions, min_color_coverage, colors):
        self.stream_path = stream_path
        self.regions = [Region(position=RegionPosition[position.upper()], **region) for position, region in regions.items()]
        self.min_color_coverage = min_color_coverage
        self.colors = [Color(**color) for color in colors]

    @classmethod
    def from_json(cls, json_file_path):
        with open(json_file_path) as f:
            data = json.load(f)
        return cls(**data)
