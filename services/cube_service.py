from models.direction import Direction
from models.region_position import RegionPosition
from services.color_service import ColorService
from services.region_service import RegionService


class CubeService:
    def __init__(self):
        self.result = ['undefined'] * 8

    def get_cubes(self, img, regions, colors, min_color_coverage, direction):
        region_service = RegionService()
        color_service = ColorService()

        for region in regions:
            region_img = region_service.get_img_region(img, region)
            color = color_service.get_color(region_img, colors, min_color_coverage)
            name = ''
            if color:
                name = color.name

            if region.position == RegionPosition.LOWER_LEFT:
                if direction == Direction.FRONT:
                    self.result[3] = name
                else:
                    self.result[0] = name
            if region.position == RegionPosition.UPPER_LEFT:
                if direction == Direction.FRONT:
                    self.result[7] = name
                else:
                    self.result[4] = name
            if region.position == RegionPosition.LOWER_RIGHT:
                if direction == Direction.FRONT:
                    self.result[1] = name
                else:
                    self.result[2] = name
            if region.position == RegionPosition.UPPER_RIGHT:
                if direction == Direction.FRONT:
                    self.result[5] = name
                else:
                    self.result[6] = name
