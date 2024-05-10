import cv2

from models.config.config import Config
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

    # ColorService.generate_color_palette(0, 179, 0, 255, 0, 255, 100)
    right = 0
    bottom = 0
    while True:
        grabbed, frame = cap.read()

        if not grabbed:
            break

        frame_copy = frame.copy()
        for orientation, regions in config.quadrant.regions.items():
            if orientation != Orientation.RIGHT_EDGE:
                continue
            for region in regions:
                x1 = int((region.coord[0] + right - region.width / 2))
                y1 = int((region.coord[1] + bottom - region.height / 2))
                x2 = int(x1 + region.width)
                y2 = int(y1 + region.height)

                cv2.rectangle(frame_copy, (x1, y1), (x2, y2), (0, 255, 0))

        cv2.imshow('frame', frame_copy)
        cv2.setMouseCallback('frame', draw_rectangle, {'frame': frame})

        key = None
        while key != 13:
            key = cv2.waitKeyEx(0)
            if key == 2424832:
                right -= 1
            if key == 2555904:
                right += 1
            if key == 2490368:
                bottom -= 1
            if key == 2621440:
                bottom += 1

            frame_copy = frame.copy()
            for orientation, regions in config.quadrant.regions.items():
                if orientation != Orientation.RIGHT_EDGE:
                    continue
                for region in regions:
                    x1 = int((region.coord[0] + right - region.width / 2))
                    y1 = int((region.coord[1] + bottom - region.height / 2))
                    x2 = int(x1 + region.width)
                    y2 = int(y1 + region.height)

                    cv2.rectangle(frame_copy, (x1, y1), (x2, y2), (0, 255, 0))
            cv2.imshow('frame', frame_copy)

            print(right, bottom)


if __name__ == '__main__':
    main()
