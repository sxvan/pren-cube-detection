from models.cube_position import CubePosition
from models.orientation import Orientation
from services.region_service import RegionService


class CubeService:
    def detect_cubes(self, img, regions, colors, min_color_coverage, orientation: Orientation):
        cube_detection_results = {}
        region_service = RegionService()

        for region in regions:
            if not self.check_preconditions(region, cube_detection_results, orientation):
                break

            color_name = region_service.get_region_color_name(img, region, colors, min_color_coverage)
            cube_position = self.get_normalized_cube_position(orientation, region.position)
            cube_detection_results[cube_position] = color_name

        return cube_detection_results

    def check_preconditions(self, region, cube_detection_results, orientation: Orientation):
        for precondition in region.when_missing:
            normalized_precondition = self.get_normalized_cube_position(orientation, precondition)
            color_name = cube_detection_results[normalized_precondition]
            if color_name is None:
                return False

            if color_name != '':
                return False

        return True

    def get_normalized_cube_position(self, orientation: Orientation, cube_position: CubePosition) -> CubePosition:
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
