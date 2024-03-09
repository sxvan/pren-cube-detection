import cv2 as cv
from models.config import Config
from services.cube_service import CubeService
from services.quadrant_service import QuadrantService


def main():
    def get_orientation(img):
        return quadrant_service.get_orientation(img, config.quadrant_regions, config.quadrant_colors)

    def get_cubes(img, orientation):
        return cube_service.detect_cubes(
            img,
            config.side_regions,
            config.edge_regions,
            config.cube_colors,
            orientation)

    cube_service = CubeService()
    quadrant_service = QuadrantService()
    config = Config.from_json('config.json')

    capture = cv.VideoCapture(config.video_source)
    frame_count = 0
    while True:
        frame_count += 1
        if frame_count % config.frame_frequency == 0:
            ret, frame = capture.read()
            if not ret:
                break

            orientation = get_orientation(frame)
            if orientation is not None:
                print(orientation, get_cubes(frame, orientation))
                config.quadrant_regions.pop(orientation)

            if len(config.quadrant_regions) < 1:
                break
        else:
            capture.grab()

    print(cube_service.cubes)


if __name__ == '__main__':
    main()
