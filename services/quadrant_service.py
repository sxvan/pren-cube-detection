import cv2

from models.color import Color
from models.orientation import Orientation
from models.region import Region
from services.region_service import RegionService


class QuadrantService:
    def __init__(self, region_service: RegionService, quadrant_regions: (Orientation, [Region]), colors: [Color]):
        self._region_service = region_service
        self._quadrant_regions = quadrant_regions
        self._colors = colors

    def get_orientation(self, img):
        for orientation, regions in self._quadrant_regions.items():
            if all(self._region_service.get_region_color_name(img, region, self._colors) != '' for region in regions):
                return orientation

        return None
