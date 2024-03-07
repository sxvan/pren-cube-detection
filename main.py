from models.config import Config
import cv2 as cv

from models.cube_position import CubePosition
from models.orientation import Orientation
from services.cube_service import CubeService
from services.quadrant_service_deprecated import QuadrantServiceDeprecated


def get_cubes(img, orientation):
    regions = config.edge_regions
    if orientation.value % 90 == 0:
        regions = config.side_regions

    cube_detection_results = cube_service.detect_cubes(
        img,
        regions,
        config.colors,
        config.min_color_coverage,
        orientation)

    for cube_detection_result in cube_detection_results:
        cubes_dict[cube_detection_result.cube_position] = cube_detection_result.color_name


config = Config.from_json("config.json")

quadrant_service = QuadrantServiceDeprecated()
cube_service = CubeService()

cubes_dict = {position: 'undefined' for position in CubePosition}

capture = cv.VideoCapture(config.stream_path)

capture.set(1, 109)
_, frame = capture.read()
get_cubes(frame, Orientation.LEFT_EDGE)

capture.set(1, 219)
_, frame = capture.read()
get_cubes(frame, Orientation.FRONT)

capture.set(1, 330)
_, frame = capture.read()
get_cubes(frame, Orientation.FRONT_EDGE)

capture.set(1, 444)
_, frame = capture.read()
get_cubes(frame, Orientation.RIGHT)

capture.set(1, 560)
_, frame = capture.read()
get_cubes(frame, Orientation.RIGHT_EDGE)

capture.set(1, 670)
_, frame = capture.read()
get_cubes(frame, Orientation.BACK)

capture.set(1, 786)
_, frame = capture.read()
get_cubes(frame, Orientation.BACK_EDGE)

capture.set(1, 895)
_, frame = capture.read()
get_cubes(frame, Orientation.LEFT)

print(cubes_dict)

