import json

from models.config.camera_profile_config import CameraProfileConfig
from models.config.control_unit_config import ControlUnitConfig
from models.config.cube_config import CubeConfig
from models.config.pren_api_config import PrenApiConfig
from models.config.quadrant_config import QuadrantConfig


class Config:
    def __init__(self, frame_frequency, fetch_delay_ms, max_consecutive_fails, camera_profile, pren_api, control_unit, cubes, quadrant):
        self.frame_frequency = frame_frequency
        self.fetch_delay_ms = fetch_delay_ms
        self.max_consecutive_fails = max_consecutive_fails
        self.camera_profile = CameraProfileConfig(**camera_profile)
        self.pren_api = PrenApiConfig(**pren_api)
        self.control_unit = ControlUnitConfig(**control_unit)
        self.cubes = CubeConfig(**cubes)
        self.quadrant = QuadrantConfig(**quadrant)

    @classmethod
    def from_json(cls, json_file_path):
        with open(json_file_path) as f:
            data = json.load(f)
        return cls(**data)
