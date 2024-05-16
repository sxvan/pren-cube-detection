import cv2
import pickle
import os
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


def update_json_file(file_path, region, region_name, new_value, behind):
    with open(file_path, 'r+') as file:
        data = json.load(file)
        cubes = data['cubes']
        if region in cubes and region_name in cubes[region]:
            region_list = cubes[region][region_name]
            for i, region_data in enumerate(region_list):
                print(i)
                if i == 0 and not behind:
                    region_data['coord'] = new_value
                elif i!=0 and behind:
                    region_data['coord'] = new_value
                file.seek(0)
                json.dump(data, file, indent=4)
                file.truncate()


def accept_cube_position(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        draw_rectangle(event, x, y, param['frame'])
        update_json_file(param['config_path'], param['region'], param['cube_position'], [x, y], param['behind'])
def remove_suffix(text, suffix):
    if text.endswith(suffix):
        return text[:-len(suffix)]
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
    frame_count=0
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
        "top_front_right_behind",
        "bottom_back_left",
        "bottom_back_left_behind",
        "bottom_back_right",
        "bottom_back_right_behind"
    ]

    edge_region_cube_positions = [
        "top_front_left",
        "bottom_front_left",
        "top_back_left",
        "bottom_back_left",
        "top_front_right",
        "bottom_front_right",
        "top_back_right",
        "bottom_back_right"
    ]
    for orientation, frame in frames.items():
        region = "edge_regions" if orientation.name.endswith("EDGE") else "side_regions"
        #cube_positions = side_region_cube_positions if orientation.name.endswith("EDGE") else edge_region_cube_positions
        cube_positions = side_region_cube_positions


        cv2.imshow('frame', frame)
        print(f"-------------{orientation}-----------------")
        for cube_position in cube_positions:
            print(cube_position)
            behind = True if cube_position.endswith("behind") else False
            print(behind)
            template_frames = cv2.imread(os.path.join('test_frames', f'{cube_position}.jpg'))
            if behind:
                cube_position = remove_suffix(cube_position, "_behind")
            cv2.imshow('template_frames', template_frames)
            cv2.setMouseCallback('frame', accept_cube_position, {'frame': frame, "config_path": 'config.json',
                                                                 'region': region, 'cube_position': cube_position, 'behind':behind})
            cv2.waitKey()
        cv2.waitKey()

if __name__ == '__main__':
    main()