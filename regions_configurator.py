import cv2
import json

from models.config.config import Config
from models.orientation import Orientation
from services.color_service import ColorService
from services.cube_service import CubeService
from services.quadrant_service import QuadrantService
from services.region_service import RegionService


def draw_rectangle(event, x, y, frame):
    cv2.rectangle(frame, (x - 10, y - 10), (x + 10, y + 10), (0, 255, 0), 1)
    cv2.imshow('frame', frame)
    print((x, y))


def update_json_file(file_path, side_regions, region_name, new_value):
    with open(file_path, 'r+') as file:
        print("open")
        data = json.load(file)
        for region in data['cubes'][side_regions][region_name]:
            region['coord'] = new_value
        file.seek(0)
        json.dump(data, file, indent=4)
        file.truncate()


def accept_cube_position(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        draw_rectangle(event, x, y, param['frame'])
        update_json_file(param['config_path'], param['side_regions'], param['cube_position'], [x, y])


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


    #while -> save Frames


    orientations_seen = []
    started = False
    while True:
        grabbed, frame = cap.read()
        if not grabbed:
            break

        orientation = quadrant_service.get_orientation(frame)
        if started or (not orientation or orientation != Orientation.FRONT_EDGE):
            continue
        else:
            started = True



        print(orientation)

        cube_service.detect_cubes(frame, orientation)
        print(cube_service.cubes)

        cube_regions = config.cubes.edge_regions
        if orientation.value % 90 == 0:
            cube_regions = config.cubes.side_regions

        for position, regions in cube_regions.items():
            for region in regions:
                x1 = int((region.coord[0] - region.width / 2))
                y1 = int((region.coord[1] - region.height / 2))
                x2 = int(x1 + region.width)
                y2 = int(y1 + region.height)

                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0))

        cv2.imshow('frame', frame)
        cv2.setMouseCallback('frame', accept_cube_position, {'frame': frame, "config_path": 'config.json',
                                                             'side_regions': 'side_regions',
                                                             'cube_position': 'bottom_front_right'})
        cv2.waitKey()


if __name__ == '__main__':
    main()