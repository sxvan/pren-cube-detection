import time

import cv2

from models.config.config import Config
from models.cube_position import CubePosition
from models.orientation import Orientation
from services.color_service import ColorService
from services.cube_service import CubeService
from services.quadrant_service import QuadrantService
from services.region_service import RegionService


def draw_rectangle(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        frame = param['frame']
        cv2.rectangle(frame, (x - 10, y - 10), (x + 10, y + 10), (0, 255, 0), 1)
        cv2.imshow('frame', frame)
        print((x, y))


def main():
    config = Config.from_json('config.json')
    color_service = ColorService()
    region_service = RegionService(color_service)
    quadrant_service = QuadrantService(region_service, config.quadrant.regions, config.quadrant.colors)
    cube_service = CubeService(region_service, config.cubes.side_regions, config.cubes.edge_regions,
                               config.cubes.colors)

    camera_profile = config.camera_profile
    cap = cv2.VideoCapture(f'{camera_profile.protocol}://{camera_profile.username}:{camera_profile.password}'
                           f'@{camera_profile.ip_address}/{camera_profile.url}'
                           f'?streamprofile={camera_profile.profile}')

    # ColorService.generate_color_palette(0, 0, 221, 221, 233, 233, 10)
    right = 0
    bottom = 0
    while True:
        cube_service = CubeService(region_service, config.cubes.side_regions, config.cubes.edge_regions,
                                   config.cubes.colors)
        grabbed, frame = cap.read()

        if not grabbed:
            continue

        # orientation = quadrant_service.get_orientation(frame)
        # if not orientation:
        #     continue
        #
        # print(orientation)
        #
        # cube_service.detect_cubes(frame, orientation)
        # print(cube_service.cubes)

        cube_regions = config.cubes.edge_regions
        # if orientation.value % 90 == 0:
        #     cube_regions = config.cubes.side_regions

        for position, regions in cube_regions.items():
            for region in regions:
                x1 = int((region.coord[0] - region.width / 2))
                y1 = int((region.coord[1] - region.height / 2))
                x2 = int(x1 + region.width)
                y2 = int(y1 + region.height)

                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0))

        cv2.imshow('frame', frame)
        cv2.setMouseCallback('frame', draw_rectangle, {'frame': frame})
        cv2.waitKey(1)

if __name__ == '__main__':
    main()
