import cv2

from models.color import Color
from models.orientation import Orientation
from models.region import Region
from services.region_service import RegionService


class QuadrantService:
    def __init__(self, region_service: RegionService, quadrant_regions: (Orientation, [Region]), colors: [Color]):
        self.__region_service = region_service
        self.__quadrant_regions = quadrant_regions
        self.__colors = colors

    def get_orientation(self, img):
        for orientation, regions in self.__quadrant_regions.items():
            color_not_found_in_all_regions = False
            for region in regions:
                color_name = self.__region_service.get_region_color_name(img, region, self.__colors)
                if color_name == '':
                    color_not_found_in_all_regions = True
                    break

            if not color_not_found_in_all_regions:
                return orientation

        return None
