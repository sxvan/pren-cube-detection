from models.color import Color
import json

from models.cube_position import CubePosition
from models.orientation import Orientation
from models.region import Region


class Config:
    def __init__(self,
                 video_source,
                 frame_frequency,
                 start_signal_pin,
                 submission_base_url,
                 team,
                 datetime_format,
                 cube_colors,
                 quadrant_colors,
                 side_regions,
                 edge_regions,
                 quadrant_regions):
        self.video_source = video_source
        self.frame_frequency = frame_frequency
        self.start_signal_pin = start_signal_pin
        self.submission_base_url = submission_base_url
        self.team = team
        self.datetime_format = datetime_format

        self.side_regions: (CubePosition, Region) = {}
        for position, region in side_regions.items():
            self.side_regions[CubePosition[position.upper()]] = Region(**region)

        self.edge_regions: (CubePosition, Region) = {}
        for position, region in edge_regions.items():
            self.edge_regions[CubePosition[position.upper()]] = Region(**region)

        self.quadrant_regions: (Orientation, [Region]) = {}
        for position, regions in quadrant_regions.items():
            self.quadrant_regions[Orientation[position.upper()]] = [Region(**region) for region in regions]

        self.cube_colors = [Color(**color) for color in cube_colors]
        self.quadrant_colors = [Color(**color) for color in quadrant_colors]

    @classmethod
    def from_json(cls, json_file_path):
        with open(json_file_path) as f:
            data = json.load(f)
        return cls(**data)
