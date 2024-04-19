import time

import cv2 as cv

from models.config.config import Config
from models.cube_position import CubePosition
from models.orientation import Orientation
from services.color_service import ColorService
from services.control_unit_service import ControlUnitService
from services.cube_service import CubeService
from services.pren_service import PrenService
from services.quadrant_service import QuadrantService
from services.region_service import RegionService


def main():
    def get_orientation(img):
        return quadrant_service.get_orientation(img, config.quadrant.regions, config.quadrant.colors)

    def get_cubes(img, orientation: Orientation):
        return cube_service.detect_cubes(
            img,
            config.cubes.side_regions,
            config.cubes.edge_regions,
            config.cubes.colors,
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

    config = Config.from_json('config_new_new.json')

    color_service = ColorService()
    region_service = RegionService(color_service)
    quadrant_service = QuadrantService(region_service)
    cube_service = CubeService(region_service)
    pren_service = PrenService(config.pren_api.base_url, config.pren_api.team, config.pren_api.datetime_format)
    control_unit_service = ControlUnitService(config.control_unit.ready_pin, config.control_unit.start_pin,
                                              config.control_unit.uart.port, config.control_unit.uart.baud_rate,
                                              config.control_unit.uart.encoding, config.control_unit.uart.max_retries,
                                              config.control_unit.uart.retry_delay_ms,
                                              config.control_unit.uart.start_character,
                                              config.control_unit.uart.crc8_poly)

    # control_unit_service.send_ready_signal()
    # control_unit_service.wait_for_start_signal()
    # control_unit_service.send_unready_signal()
    pren_service.start()

    # capture = cv.VideoCapture('assets/pren_cube_01.mp4')

    camera_profile = config.camera_profile
    capture = cv.VideoCapture(f'{camera_profile.protocol}://{camera_profile.username}:{camera_profile.password}'
                              f'@{camera_profile.ip_address}/{camera_profile.url}'
                              f'?streamprofile={camera_profile.profile}')

    frame_count = 0
    cubes = {}

    fps = capture.get(cv.CAP_PROP_FPS)
    print(fps)

    start_time = time.time()
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
            # changed_cubes = get_changed_cubes(cubes, current_cubes)
            cubes.update(current_cubes)
            # print(orientation, cube_service.cubes)
            print(orientation)
            end_time = time.time()
            time_elapsed = end_time - start_time
            if time_elapsed > 4:
                print(time_elapsed)
            start_time = time.time()
            # control_unit_service.send_cube_config(cube_service.cubes)

            if is_cubes_complete(cubes):
                break

            config.quadrant.regions.pop(orientation)  # also remove orientations that look at same cube positions?

            if len(config.quadrant.regions) < 1:
                break
        else:
            if not capture.grab():
                break

    # control_unit_service.wait_for_end_signal()
    pren_service.submit(cube_service.cubes)
    pren_service.end()
    # print(pren_service.get().content)


if __name__ == '__main__':
    while True:
        main()
