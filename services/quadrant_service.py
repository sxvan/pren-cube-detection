from models.color import Color
from models.orientation import Orientation
from models.region import Region
from services.region_service import RegionService


class QuadrantService:
    def __init__(self, region_service: RegionService):
        self.region_service = region_service

    def get_orientation(self, img, quadrant_regions: (Orientation, [Region]), colors: [Color]):
        for orientation, regions in quadrant_regions.items():
            color_not_found_in_all_regions = False
            for region in regions:
                color_name = self.region_service.get_region_color_name(img, region, colors)
                if color_name == 'X':
                    color_not_found_in_all_regions = True
                    break

            if not color_not_found_in_all_regions:
                return orientation

        return None
