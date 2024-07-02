import os
import re
import sys

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


def update_json_file_side_regions(file_path, region, region_name, new_value, behind):
    with open(file_path, 'r+') as file:
        data = json.load(file)
        cubes = data['cubes']

        def update_region(cubes, region, region_name, new_value, behind):
            if region in cubes and region_name in cubes[region]:
                region_list = cubes[region][region_name]
                for i, region_data in enumerate(region_list):
                    if i == 0 and not behind:
                        region_data['coord'] = new_value
                    elif i != 0 and behind:
                        region_data['coord'] = new_value


        if region_name == 'top_front_left':
            update_region(cubes, region, 'top_front_left', new_value, behind)
            update_region(cubes, region, 'bottom_back_left', new_value, behind)
        if region_name == 'top_front_right':
            update_region(cubes, region, 'top_front_right', new_value, behind)
            update_region(cubes, region, 'bottom_back_right', new_value, behind)
        else:
            update_region(cubes, region, region_name, new_value, behind)

        file.seek(0)
        json.dump(data, file, indent=4)
        file.truncate()



def update_json_file_edge_regions(file_path, region, region_name, new_value, behind, behind_number):
    with open(file_path, 'r+') as file:
        data = json.load(file)
        cubes = data['cubes']
        if region in cubes and region_name in cubes[region]:
            region_list = cubes[region][region_name]
            for i, region_data in enumerate(region_list):
                print(i)
                if i == 0 and not behind:
                    region_data['coord'] = new_value
                elif behind_number == 1 and 0 < i <= 5 and behind:
                    region_data['coord'] = new_value
                    cubes[region]['bottom_back_left'][2]['coord'] = new_value
                elif behind_number == 2 and 5 < i <= 10 and behind:
                    region_data['coord'] = new_value
                    cubes[region]['bottom_back_left'][3]['coord'] = new_value
                elif behind_number == 3 and i == 11 and behind:
                    region_data['coord'] = new_value
                    cubes[region]['bottom_back_left'][0]['coord'] = new_value
                elif behind_number == 4 and i == 12 and behind:
                    region_data['coord'] = new_value
                    cubes[region]['bottom_back_left'][1]['coord'] = new_value
                file.seek(0)
                json.dump(data, file, indent=4)
                file.truncate()


def accept_cube_position(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        draw_rectangle(event, x, y, param['frame'])
        if param['edge']:
            update_json_file_edge_regions(param['config_path'], param['region'], param['cube_position'], [x, y],
                                          param['behind'], param['behind_number'])
        else:
            update_json_file_side_regions(param['config_path'], param['region'], param['cube_position'], [x, y],
                                          param['behind'])


def remove_suffix(text, suffix):
    # Use a regular expression to match suffix with or without a number
    pattern = re.compile(re.escape(suffix) + r'(_\d+)?$')
    match = pattern.search(text)
    if match:
        return text[:match.start()]
    return text


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
    started = False
    frames = {}
    frame_count = 0
    while True:
        grabbed, frame = cap.read()
        if not grabbed:
            break
        orientation = quadrant_service.get_orientation(frame)
        if orientation and (started or orientation == Orientation.FRONT):
            print("frame")
            started = True

            if orientation not in frames:
                frames[orientation] = frame
                # frame_path = os.path.join('template_frames', f'{orientation}.jpg')
                # cv2.imwrite(frame_path, frame)
                frame_count += 1

            if frame_count >= 2:
                print("finish")
                break

    side_region_cube_positions = [
        "top_back_left",
        "top_back_right",
        "bottom_front_left",
        "bottom_front_right",
        "top_front_left",
        "top_front_left_behind",
        "top_front_right",
        "top_front_right_behind"
    ]
    edge_region_cube_positions = [
        "top_front_left",
        "bottom_front_left",
        "top_back_right",
        "bottom_back_right",
        "bottom_front_right",
        "top_back_left",
        "top_front_right",
        "top_front_right_behind_1",
        "top_front_right_behind_2",
        "top_front_right_behind_3",
        "top_front_right_behind_4"
    ]
    for orientation, frame in frames.items():
        region, cube_positions, frames_directory, edge = (
        "edge_regions", edge_region_cube_positions, "template_frames_edge", True) if \
            orientation.name.endswith("EDGE") else (
        "side_regions", side_region_cube_positions, "template_frames_side", False)

        cv2.imshow('frame', frame)
        print(f"-------------{orientation}-----------------")
        for cube_position in cube_positions:
            print(cube_position)
            behind = True if re.search(r'behind(_\d+)?$', cube_position) else False
            print(behind)
            template_frames = cv2.imread(os.path.join(frames_directory, f'{cube_position}.jpg'))
            behind_number = sys.maxsize
            if behind:
                if edge: behind_number = int(cube_position[-1])
                cube_position = remove_suffix(cube_position, "_behind")
                print(f"cut: {cube_position}")
            cv2.imshow('template_frames', template_frames)
            cv2.setMouseCallback('frame', accept_cube_position, {'frame': frame, "config_path": 'config.json',
                                                                 'region': region, 'cube_position': cube_position,
                                                                 'behind': behind,
                                                                 'edge': edge, 'behind_number': behind_number})
            cv2.waitKey()
        cv2.waitKey()


if __name__ == '__main__':
    main()
