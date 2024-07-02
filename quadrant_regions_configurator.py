import cv2
import os
import re
import sys
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


def update_json_file_quadrant(file_path, region_name, new_value):
    with open(file_path, 'r+') as file:
        data = json.load(file)
        regions = data['quadrant']['regions']

        def update_coords(primary_region, secondary_region, new_value, regions):
            if primary_region in regions and len(regions[primary_region]) > 1:
                regions[primary_region][1]['coord'] = new_value
            if secondary_region in regions and len(regions[secondary_region]) > 0:
                regions[secondary_region][0]['coord'] = new_value

        if region_name == 'bottom':
            update_coords('front', 'right', new_value, regions)
        elif region_name == 'left':
            update_coords('right', 'back', new_value, regions)
        elif region_name == 'top':
            update_coords('back', 'left', new_value, regions)
        elif region_name == 'right':
            update_coords('left', 'front', new_value, regions)
        elif region_name == 'bottom_left':
            update_coords('front_edge', 'right_edge', new_value, regions)
        elif region_name == 'left_top':
            update_coords('right_edge', 'back_edge', new_value, regions)
        elif region_name == 'top_right':
            update_coords('back_edge', 'left_edge', new_value, regions)
        elif region_name == 'right_bottom':
            update_coords('left_edge', 'front_edge', new_value, regions)

        file.seek(0)
        json.dump(data, file, indent=4)
        file.truncate()


def accept_cube_position(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        draw_rectangle(event, x, y, param['frame'])
        update_json_file_quadrant(param['config_path'], param['position'], [x, y])


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

    regions_positions = [
        "bottom",
        "left",
        "top",
        "right",
        "bottom_left",
        "left_top",
        "top_right",
        "right_bottom"
    ]

    right = 0
    bottom = 0
    while True:
        grabbed, frame = cap.read()

        if not grabbed:
            break

        orientation = quadrant_service.get_orientation(frame)
        if not orientation:
            continue

        frame_copy = frame.copy()
        for orientation, regions in config.quadrant.regions.items():
            for region in regions:
                x1 = int((region.coord[0] + right - region.width / 2))
                y1 = int((region.coord[1] + bottom - region.height / 2))
                x2 = int(x1 + region.width)
                y2 = int(y1 + region.height)

                cv2.rectangle(frame_copy, (x1, y1), (x2, y2), (0, 255, 0))

        for position in regions_positions:
            print(position)
            cv2.imshow('frame', frame_copy)
            cv2.setMouseCallback('frame', accept_cube_position, {'frame': frame, "config_path": 'config.json', 'position': position })
            key = cv2.waitKey(0) & 0xFF
            if key == 13 or key == ord('s'):  # ENTER or 's' key for skip
                break
            elif key == ord('q'):  # 'q' key for quit
                cap.release()
                cv2.destroyAllWindows()
                return

        key = None
        while key != 13:  # ENTER key
            key = cv2.waitKeyEx(0)
            if key == 2424832:  # Left arrow
                right -= 1
            elif key == 2555904:  # Right arrow
                right += 1
            elif key == 2490368:  # Up arrow
                bottom -= 1
            elif key == 2621440:  # Down arrow
                bottom += 1

            frame_copy = frame.copy()
            for orientation, regions in config.quadrant.regions.items():
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