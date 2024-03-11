import cv2 as cv

from models import orientation
from models.config import Config
from models.cube_position import CubePosition
from models.orientation import Orientation
from services.color_service import ColorService
from services.cube_service import CubeService
from services.quadrant_service import QuadrantService
from services.region_service import RegionService


def main():
    def get_orientation(img):
        return quadrant_service.get_orientation(img, config.quadrant_regions, config.quadrant_colors)

    def get_cubes(img, orientation: Orientation):
        return cube_service.detect_cubes(
            img,
            config.side_regions,
            config.edge_regions,
            config.cube_colors,
            orientation)

    def get_changed_cubes(previous_cubes, current_cubes):
        changed_cubes = {}
        for position, color in current_cubes.items():
            if position not in previous_cubes:
                changed_cubes[position] = color

        return changed_cubes

    def is_cubes_complete(cubes):
        positions = set(position for position in CubePosition)
        cubes_keys = set(cubes.keys())

        return positions.issubset(cubes_keys)

    color_service = ColorService()
    region_service = RegionService(color_service)
    quadrant_service = QuadrantService(region_service)
    cube_service = CubeService(region_service)

    config = Config.from_json('config.json')

    capture = cv.VideoCapture(config.video_source)
    frame_count = 0

    cubes = {}
    while True:
        frame_count += 1
        if frame_count % config.frame_frequency == 0:
            grabbed, frame = capture.read()
            if not grabbed:
                break

            orientation = get_orientation(frame)
            if orientation is None:
                continue

            current_cubes = get_cubes(frame, orientation)
            changed_cubes = get_changed_cubes(cubes, current_cubes)
            cubes.update(current_cubes)
            print(orientation, changed_cubes)

            if is_cubes_complete(cubes):
                break

            config.quadrant_regions.pop(orientation)  # also remove orientations that look at same cube positions?

            if len(config.quadrant_regions) < 1:
                break
        else:
            if not capture.grab():
                break

    print(cube_service.cubes)


if __name__ == '__main__':
    main()
