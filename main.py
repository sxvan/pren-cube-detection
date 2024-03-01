from models.config import Config
import cv2 as cv

from models.orientation import Orientation
from services.color_service import ColorService
from services.cube_service import CubeService
from services.quadrant_service_deprecated import QuadrantServiceDeprecated
from services.region_service import RegionService


config = Config.from_json("config.json")

region_service = RegionService()
color_service = ColorService()

quadrant_service = QuadrantServiceDeprecated()
cube_service = CubeService()

capture = cv.VideoCapture(config.stream_path)

start_frame = None

while not start_frame:
    ret, frame = capture.read()

    if not ret:
        break


    orientation = quadrant_service.get_orientation(frame)
    if orientation:
        cube_service.get_cubes(frame, config.regions, config.colors, config.min_color_coverage, orientation)

    #if quadrant_service.is_start_position(frame):
     #   start_frame = capture.get(1)
      #  cube_service.get_cubes(frame, config.regions, config.colors, config.min_color_coverage, Direction.FRONT)

#capture.set(1, start_frame + 220)
#_, frame = capture.read()
#cube_service.get_cubes(frame, config.regions, config.colors, config.min_color_coverage, Direction.RIGHT)

#print(cube_service.result)