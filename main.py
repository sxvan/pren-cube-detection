import cv2

from models.config import Config
import cv2 as cv
import numpy as np

from models.cube_position import CubePosition
from models.orientation import Orientation
from services.cube_service import CubeService
from services.quadrant_service_deprecated import QuadrantServiceDeprecated


# Define the mouse callback function
def click_event(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        print(f"Coordinates: ({x}, {y})")


def get_cubes(img, orientation):
    if orientation.value % 90 == 0:
        regions = config.side_regions
    else:
        regions = config.edge_regions

    cube_detection_results = cube_service.detect_cubes(
        img,
        regions,
        config.colors,
        config.min_color_coverage,
        orientation)

    cubes_dict.update(cube_detection_results)


config = Config.from_json("config.json")

quadrant_service = QuadrantServiceDeprecated()
cube_service = CubeService()

cubes_dict = {position: 'undefined' for position in CubePosition}

capture = cv.VideoCapture(config.stream_path)

# capture.set(1, 109)
# _, frame = capture.read()
# get_cubes(frame, Orientation.LEFT_EDGE)

# capture.set(1, 219)
# _, frame = capture.read()
# get_cubes(frame, Orientation.FRONT)

# capture.set(1, 330)
# _, frame = capture.read()
# get_cubes(frame, Orientation.FRONT_EDGE)

capture.set(1, 435)
_, frame = capture.read()
get_cubes(frame, Orientation.RIGHT)

# capture.set(1, 560)
# _, frame = capture.read()
# get_cubes(frame, Orientation.RIGHT_EDGE)

# capture.set(1, 670)
# _, frame = capture.read()
# get_cubes(frame, Orientation.BACK)

# capture.set(1, 786)
# _, frame = capture.read()
# get_cubes(frame, Orientation.BACK_EDGE)

# capture.set(1, 895)
# _, frame = capture.read()
# get_cubes(frame, Orientation.LEFT)

print(cubes_dict)

# cv2.imshow('Image', frame)
#
# # Set the mouse callback function for the window
# cv2.setMouseCallback('Image', click_event)
#
# # Wait for any key to close the window
# cv2.waitKey(0)
#
# # Close all OpenCV windows
# cv2.destroyAllWindows()
