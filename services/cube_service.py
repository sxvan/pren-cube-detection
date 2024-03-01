from models.orientation import Orientation
from models.cube_region_position import CubeRegionPosition
from services.color_service import ColorService
from services.region_service import RegionService


class CubeService:
    def __init__(self):
        self.result = ['undefined'] * 8

    def get_cubes(self, img, regions, colors, min_color_coverage, orientation: Orientation):
        region_service = RegionService()
        color_service = ColorService()

        if orientation.value % 90 == 0:
            self.get_cubes_side()
        else:
            self.get_cubes_edge()

        for region in regions:
            region_img = region_service.get_img_region(img, region)
            color = color_service.get_color(region_img, colors, min_color_coverage)
            name = ''
            if color:
                name = color.name

            if region.position == CubeRegionPosition.LOWER_LEFT:
                if orientation == Orientation.FRONT:
                    self.result[3] = name
                else:
                    self.result[0] = name
            if region.position == CubeRegionPosition.UPPER_LEFT:
                if orientation == Orientation.FRONT:
                    self.result[7] = name
                else:
                    self.result[4] = name
            if region.position == CubeRegionPosition.LOWER_RIGHT:
                if orientation == Orientation.FRONT:
                    self.result[1] = name
                else:
                    self.result[2] = name
            if region.position == CubeRegionPosition.UPPER_RIGHT:
                if orientation == Orientation.FRONT:
                    self.result[5] = name
                else:
                    self.result[6] = name


    #def get_cubes_side(self):

    #def get_cubes_edge(self):
