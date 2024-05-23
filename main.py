import time

import cv2
import logging

from models.config.config import Config
from services.color_service import ColorService
from services.control_unit_service import ControlUnitService
from services.cube_service import CubeService
from services.pren_service import PrenService
from services.quadrant_service import QuadrantService
from services.region_service import RegionService


def main():
    logging.basicConfig(filename='main.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    config = Config.from_json('config.json')

    color_service = ColorService()
    region_service = RegionService(color_service)
    quadrant_service = QuadrantService(region_service, config.quadrant.regions, config.quadrant.colors)
    cube_service = CubeService(region_service, config.cubes.side_regions, config.cubes.edge_regions,
                               config.cubes.colors)
    pren_service = PrenService(config.pren_api.base_url, config.pren_api.team, config.pren_api.datetime_format)
    control_unit_service = ControlUnitService(config.control_unit.ready_pin, config.control_unit.start_pin,
                                              config.control_unit.uart.port, config.control_unit.uart.baud_rate,
                                              config.control_unit.uart.encoding, config.control_unit.uart.max_retries,
                                              config.control_unit.uart.retry_delay_ms,
                                              config.control_unit.uart.start_character,
                                              config.control_unit.uart.crc8_poly)

    logging.info('Opening video capture')
    camera_profile = config.camera_profile
    cap = cv2.VideoCapture(f'{camera_profile.protocol}://{camera_profile.username}:{camera_profile.password}'
                           f'@{camera_profile.ip_address}/{camera_profile.url}'
                           f'?streamprofile={camera_profile.profile}')
    logging.info('Opened video capture')

    logging.info('Sending ready signal')
    control_unit_service.send_ready_signal()
    logging.info('Waiting for start signal')
    control_unit_service.wait_for_start_signal()
    logging.info('Sending unready signal')
    control_unit_service.send_unready_signal()

    logging.info('Sending start signal to pren endpoint')
    pren_service.start()  # when to start? can capture be before start?

    frame_count = 0
    consecutive_fails = 0
    while True and consecutive_fails < config.max_consecutive_fails:
        frame_count += 1
        if frame_count % config.frame_frequency == 0:
            grabbed, frame = cap.read()
            if not grabbed:
                consecutive_fails += 1
                time.sleep(1)
                logging.error("Failed to grab frame")
                continue

            consecutive_fails = 0

            orientation = quadrant_service.get_orientation(frame)
            if orientation is None:
                continue

            print(orientation)

            logging.info(f'Processing orientation: {orientation}')
            cube_service.detect_cubes(frame, orientation)

            logging.info(f'Sending cube config')
            success = control_unit_service.send_cube_config(cube_service.cubes)
            logging.info(f'Send was successful: {success}')

            if '?' not in cube_service.cubes.values():
                logging.info("Cube config complete")
                break

            config.quadrant.regions.pop(orientation)
        else:
            if not cap.grab():
                break

    logging.info(f'Finished analyzing cube config')
    pren_service.submit(cube_service.cubes)

    logging.info(f'Waiting for end signal')
    control_unit_service.wait_for_end_signal()
    logging.info(f'Received end signal')

    logging.info(cube_service.cubes)
    pren_service.end()
    print(pren_service.get().content)


if __name__ == '__main__':
    while True:
        main()
