import cv2

from models.cube_position import CubePosition
from models.orientation import Orientation
from models.region import Region
from services.region_service import RegionService


class CubeService:
    def __init__(self, region_service: RegionService,
                 cube_side_regions: (CubePosition, Region),
                 cube_edge_regions: (CubePosition, Region),
                 colors):
        self._region_service = region_service
        self._cube_side_regions = cube_side_regions
        self._cube_edge_regions = cube_edge_regions
        self._colors = colors
        self.cubes = {position: '?' for position in CubePosition}

    def detect_cubes(self, img, orientation: Orientation):
        if orientation.value % 90 == 0:
            cube_regions = self._cube_side_regions
        else:
            cube_regions = self._cube_edge_regions

        for cube_position, regions in cube_regions.items():
            for region in regions:
                if not self._check_when_missing(orientation, region):
                    continue

                normalized_cube_position = self._get_normalized_cube_position(orientation, cube_position)
                color_name = self._region_service.get_region_color_name(img, region, self._colors)


                print(cube_position)
                if color_name:
                    print(color_name)
                else:
                    print('None')

                x1 = int((region.coord[0] - region.width / 2))
                y1 = int((region.coord[1] - region.height / 2))
                x2 = int(x1 + region.width)
                y2 = int(y1 + region.height)
                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 1)
                cv2.imshow('img', img)
                cv2.waitKey()

                if not self._check_when_different(orientation, region, color_name):
                    continue

                self.cubes[normalized_cube_position] = color_name
                break

    def _check_when_missing(self, orientation, region):
        if not region.when_missing:
            return True

        for cube_position in region.when_missing:
            normalized_cube_position = self._get_normalized_cube_position(orientation, cube_position)
            if self.cubes[normalized_cube_position] != '':
                return False

        return True

    def _check_when_different(self, orientation, region, color_name):
        if not region.when_different:
            return True

        for cube_position in region.when_different:
            normalized_cube_position = self._get_normalized_cube_position(orientation, cube_position)
            other_color_name = self.cubes[normalized_cube_position]
            if other_color_name == '?' or other_color_name == color_name:
                return False

        return True

    @staticmethod
    def _get_normalized_cube_position(orientation: Orientation, cube_position: CubePosition) -> CubePosition:
        if orientation == Orientation.FRONT_EDGE:
            orientation = Orientation.FRONT
        elif orientation == Orientation.RIGHT_EDGE:
            orientation = Orientation.RIGHT
        elif orientation == Orientation.BACK_EDGE:
            orientation = Orientation.BACK
        elif orientation == Orientation.LEFT_EDGE:
            orientation = Orientation.LEFT

        orientation_position_to_normalized_position = {
            (Orientation.FRONT, CubePosition.BOTTOM_FRONT_LEFT): CubePosition.BOTTOM_FRONT_LEFT,
            (Orientation.FRONT, CubePosition.BOTTOM_FRONT_RIGHT): CubePosition.BOTTOM_FRONT_RIGHT,
            (Orientation.FRONT, CubePosition.BOTTOM_BACK_RIGHT): CubePosition.BOTTOM_BACK_RIGHT,
            (Orientation.FRONT, CubePosition.BOTTOM_BACK_LEFT): CubePosition.BOTTOM_BACK_LEFT,
            (Orientation.FRONT, CubePosition.TOP_FRONT_LEFT): CubePosition.TOP_FRONT_LEFT,
            (Orientation.FRONT, CubePosition.TOP_FRONT_RIGHT): CubePosition.TOP_FRONT_RIGHT,
            (Orientation.FRONT, CubePosition.TOP_BACK_RIGHT): CubePosition.TOP_BACK_RIGHT,
            (Orientation.FRONT, CubePosition.TOP_BACK_LEFT): CubePosition.TOP_BACK_LEFT,

            (Orientation.BACK, CubePosition.BOTTOM_FRONT_LEFT): CubePosition.BOTTOM_BACK_RIGHT,
            (Orientation.BACK, CubePosition.BOTTOM_FRONT_RIGHT): CubePosition.BOTTOM_BACK_LEFT,
            (Orientation.BACK, CubePosition.BOTTOM_BACK_RIGHT): CubePosition.BOTTOM_FRONT_LEFT,
            (Orientation.BACK, CubePosition.BOTTOM_BACK_LEFT): CubePosition.BOTTOM_FRONT_RIGHT,
            (Orientation.BACK, CubePosition.TOP_FRONT_LEFT): CubePosition.TOP_BACK_RIGHT,
            (Orientation.BACK, CubePosition.TOP_FRONT_RIGHT): CubePosition.TOP_BACK_LEFT,
            (Orientation.BACK, CubePosition.TOP_BACK_RIGHT): CubePosition.TOP_FRONT_LEFT,
            (Orientation.BACK, CubePosition.TOP_BACK_LEFT): CubePosition.TOP_FRONT_RIGHT,

            (Orientation.RIGHT, CubePosition.BOTTOM_FRONT_LEFT): CubePosition.BOTTOM_FRONT_RIGHT,
            (Orientation.RIGHT, CubePosition.BOTTOM_FRONT_RIGHT): CubePosition.BOTTOM_BACK_RIGHT,
            (Orientation.RIGHT, CubePosition.BOTTOM_BACK_RIGHT): CubePosition.BOTTOM_BACK_LEFT,
            (Orientation.RIGHT, CubePosition.BOTTOM_BACK_LEFT): CubePosition.BOTTOM_FRONT_LEFT,
            (Orientation.RIGHT, CubePosition.TOP_FRONT_LEFT): CubePosition.TOP_FRONT_RIGHT,
            (Orientation.RIGHT, CubePosition.TOP_FRONT_RIGHT): CubePosition.TOP_BACK_RIGHT,
            (Orientation.RIGHT, CubePosition.TOP_BACK_RIGHT): CubePosition.TOP_BACK_LEFT,
            (Orientation.RIGHT, CubePosition.TOP_BACK_LEFT): CubePosition.TOP_FRONT_LEFT,

            (Orientation.LEFT, CubePosition.BOTTOM_FRONT_LEFT): CubePosition.BOTTOM_BACK_LEFT,
            (Orientation.LEFT, CubePosition.BOTTOM_FRONT_RIGHT): CubePosition.BOTTOM_FRONT_LEFT,
            (Orientation.LEFT, CubePosition.BOTTOM_BACK_RIGHT): CubePosition.BOTTOM_FRONT_RIGHT,
            (Orientation.LEFT, CubePosition.BOTTOM_BACK_LEFT): CubePosition.BOTTOM_BACK_RIGHT,
            (Orientation.LEFT, CubePosition.TOP_FRONT_LEFT): CubePosition.TOP_BACK_LEFT,
            (Orientation.LEFT, CubePosition.TOP_FRONT_RIGHT): CubePosition.TOP_FRONT_LEFT,
            (Orientation.LEFT, CubePosition.TOP_BACK_RIGHT): CubePosition.TOP_FRONT_RIGHT,
            (Orientation.LEFT, CubePosition.TOP_BACK_LEFT): CubePosition.TOP_BACK_RIGHT,
        }

        return orientation_position_to_normalized_position.get((orientation, cube_position))
