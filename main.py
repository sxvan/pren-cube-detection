import random
import time

import cv2
from gpiozero import DigitalOutputDevice

from models.config.config import Config
from models.cube_position import CubePosition
from models.orientation import Orientation
from services import pren_service
from services.color_service import ColorService
from services.control_unit_service import ControlUnitService
from services.cube_service import CubeService
from services.pren_service import PrenService
from services.quadrant_service import QuadrantService
from services.region_service import RegionService


def main():
    config = Config.from_json('config.json')

    # color_service = ColorService()
    # region_service = RegionService(color_service)
    # quadrant_service = QuadrantService(region_service, config.quadrant.regions, config.quadrant.colors)
    # cube_service = CubeService(region_service, config.cubes.side_regions, config.cubes.edge_regions,
    #                            config.cubes.colors)
    # pren_service = PrenService(config.pren_api.base_url, config.pren_api.team, config.pren_api.datetime_format)
    control_unit_service = ControlUnitService(config.control_unit.ready_pin, config.control_unit.start_pin,
                                              config.control_unit.uart.port, config.control_unit.uart.baud_rate,
                                              config.control_unit.uart.encoding, config.control_unit.uart.max_retries,
                                              config.control_unit.uart.retry_delay_ms,
                                              config.control_unit.uart.start_character,
                                              config.control_unit.uart.crc8_poly)

    cube_str = input('Enter cube string to send: ')

    control_unit_service.send_ready_signal()
    control_unit_service.wait_for_start_signal()
    control_unit_service.send_unready_signal()
    #
    # # pren_service.start()  # when to start? can capture be before start?
    current_cube_str = ''

    for cube in cube_str:
        choice = random.choice([True, False])
        if choice:
            current_cube_str += cube
        else:
            current_cube_str += '?'

    current_cube_str = current_cube_str + '0'
    cube_str = cube_str + '0'

    print('Sending:', current_cube_str)
    control_unit_service.send_cube_config_str(current_cube_str)

    time.sleep(1)

    if cube_str != current_cube_str:
        control_unit_service.send_cube_config_str(cube_str)
        print('Sending:', cube_str)

    print('Finished sending')


    # camera_profile = config.camera_profile
    # cap = cv2.VideoCapture(f'{camera_profile.protocol}://{camera_profile.username}:{camera_profile.password}'
    #                        f'@{camera_profile.ip_address}/{camera_profile.url}'
    #                        f'?streamprofile={camera_profile.profile}')
    #
    # frame_count = 0
    # while True:
    #     frame_count += 1
    #     if frame_count % config.frame_frequency == 0:
    #         grabbed, frame = cap.read()
    #         if not grabbed:
    #             break
    #
    #         orientation = quadrant_service.get_orientation(frame)
    #         if orientation is None:
    #             continue
    #
    #         print(orientation)
    #
    #         cube_service.detect_cubes(frame, orientation)
    #         # control_unit_service.send_cube_config(cube_service.cubes)
    #
    #         if '?' not in cube_service.cubes.values():
    #             break
    #
    #         config.quadrant.regions.pop(orientation)
    #     else:
    #         if not cap.grab():
    #             break
    #
    # print(cube_service.cubes)
    # # pren_service.submit(cube_service.cubes)
    # #
    # # # control_unit_service.wait_for_end_signal()
    # # pren_service.end()
    # #
    # # print(pren_service.get().content)


if __name__ == '__main__':
    # while True:
    main()
