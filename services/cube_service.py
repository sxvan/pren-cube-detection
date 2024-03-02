from models.cube_detection_result import CubeDetectionResult
from models.cube_position import CubePosition
from models.orientation import Orientation
from models.cube_region_position import CubeRegionPosition
from services.color_service import ColorService
from services.region_service import RegionService


class CubeService:
    def detect_cubes(self, img, regions, colors, min_color_coverage, orientation: Orientation):
        cube_detection_results = []
        region_service = RegionService()

        for region in regions:
            color_name = region_service.get_region_color_name(img, region, colors, min_color_coverage)
            cube_position = self.get_cube_position(orientation, region.position)
            cube_detection_results.append(CubeDetectionResult(cube_position, color_name))

        return cube_detection_results
    def get_cube_position(self, orientation, position):
        orientation_region_to_cube_position = {
            (Orientation.FRONT, CubeRegionPosition.LOWER_LEFT): CubePosition.BOTTOM_FRONT_LEFT,
            (Orientation.FRONT, CubeRegionPosition.LOWER_RIGHT): CubePosition.BOTTOM_FRONT_RIGHT,
            (Orientation.FRONT, CubeRegionPosition.UPPER_LEFT): CubePosition.TOP_BACK_LEFT,
            (Orientation.FRONT, CubeRegionPosition.UPPER_RIGHT): CubePosition.TOP_BACK_RIGHT,

            (Orientation.BACK, CubeRegionPosition.LOWER_LEFT): CubePosition.BOTTOM_BACK_RIGHT,
            (Orientation.BACK, CubeRegionPosition.LOWER_RIGHT): CubePosition.BOTTOM_BACK_LEFT,
            (Orientation.BACK, CubeRegionPosition.UPPER_LEFT): CubePosition.TOP_FRONT_LEFT,
            (Orientation.BACK, CubeRegionPosition.UPPER_RIGHT): CubePosition.TOP_FRONT_RIGHT,

            (Orientation.LEFT, CubeRegionPosition.LOWER_LEFT): CubePosition.BOTTOM_BACK_LEFT,
            (Orientation.LEFT, CubeRegionPosition.LOWER_RIGHT): CubePosition.BOTTOM_FRONT_LEFT,
            (Orientation.LEFT, CubeRegionPosition.UPPER_LEFT): CubePosition.TOP_BACK_RIGHT,
            (Orientation.LEFT, CubeRegionPosition.UPPER_RIGHT): CubePosition.TOP_FRONT_RIGHT,

            (Orientation.RIGHT, CubeRegionPosition.LOWER_LEFT): CubePosition.BOTTOM_FRONT_RIGHT,
            (Orientation.RIGHT, CubeRegionPosition.LOWER_RIGHT): CubePosition.BOTTOM_BACK_RIGHT,
            (Orientation.RIGHT, CubeRegionPosition.UPPER_LEFT): CubePosition.TOP_FRONT_LEFT,
            (Orientation.RIGHT, CubeRegionPosition.UPPER_RIGHT): CubePosition.TOP_BACK_LEFT,

            (Orientation.FRONT_EDGE, CubeRegionPosition.LOWER_LEFT): CubePosition.BOTTOM_FRONT_LEFT,
            (Orientation.FRONT_EDGE, CubeRegionPosition.UPPER_LEFT): CubePosition.TOP_FRONT_LEFT,
            (Orientation.FRONT_EDGE, CubeRegionPosition.LOWER_RIGHT): CubePosition.BOTTOM_BACK_RIGHT,
            (Orientation.FRONT_EDGE, CubeRegionPosition.UPPER_RIGHT): CubePosition.TOP_BACK_RIGHT,

            (Orientation.BACK_EDGE, CubeRegionPosition.LOWER_LEFT): CubePosition.BOTTOM_BACK_RIGHT,
            (Orientation.BACK_EDGE, CubeRegionPosition.UPPER_LEFT): CubePosition.TOP_BACK_RIGHT,
            (Orientation.BACK_EDGE, CubeRegionPosition.LOWER_RIGHT): CubePosition.BOTTOM_FRONT_LEFT,
            (Orientation.BACK_EDGE, CubeRegionPosition.UPPER_RIGHT): CubePosition.TOP_FRONT_LEFT,

            (Orientation.RIGHT_EDGE, CubeRegionPosition.LOWER_LEFT): CubePosition.BOTTOM_FRONT_RIGHT,
            (Orientation.RIGHT_EDGE, CubeRegionPosition.UPPER_LEFT): CubePosition.TOP_FRONT_RIGHT,
            (Orientation.RIGHT_EDGE, CubeRegionPosition.LOWER_RIGHT): CubePosition.BOTTOM_BACK_LEFT,
            (Orientation.RIGHT_EDGE, CubeRegionPosition.UPPER_RIGHT): CubePosition.TOP_BACK_LEFT,

            (Orientation.LEFT_EDGE, CubeRegionPosition.LOWER_LEFT): CubePosition.BOTTOM_BACK_LEFT,
            (Orientation.LEFT_EDGE, CubeRegionPosition.UPPER_LEFT): CubePosition.TOP_BACK_LEFT,
            (Orientation.LEFT_EDGE, CubeRegionPosition.LOWER_RIGHT): CubePosition.BOTTOM_FRONT_RIGHT,
            (Orientation.LEFT_EDGE, CubeRegionPosition.UPPER_RIGHT): CubePosition.TOP_FRONT_RIGHT,
        }

        return orientation_region_to_cube_position.get((orientation, position))
