import cv2

from models.config.config import Config
from models.orientation import Orientation
from services.color_service import ColorService
from services.cube_service import CubeService
from services.quadrant_service import QuadrantService
from services.region_service import RegionService


centerX = None
centerY = None
frame = None

def draw_rectangle(event, x, y, flags, param):
    global frame
    if event == cv2.EVENT_LBUTTONDOWN:
        cv2.rectangle(frame, (x - 10, y - 10), (x + 10, y + 10), (0, 255, 0), 1)
        cv2.imshow('frame', frame)
        print((x, y))

def on_mouse_click(event, x, y, flags, param):
    global centerX
    global centerY
    global frame
    if event == cv2.EVENT_LBUTTONDOWN:
        centerX = x
        centerY = y

        x1, x2 = 0, frame.shape[1]
        y1, y2 = centerY, centerY
        cv2.line(frame, (x1, y1), (x2, y2), (0, 255, 0), 1)

        x1, x2 = centerX, centerX
        y1, y2 = 0, frame.shape[0]
        cv2.line(frame, (x1, y1), (x2, y2), (0, 255, 0), 1)

        cv2.imshow('frame', frame)
def main():
    global centerX
    global centerY
    global frame

    config = Config.from_json('config_test.json')

    color_service = ColorService()
    region_service = RegionService(color_service)
    quadrant_service = QuadrantService(region_service, config.quadrant.regions, config.quadrant.colors)

    camera_profile = config.camera_profile
    cap = cv2.VideoCapture(f'{camera_profile.protocol}://{camera_profile.username}:{camera_profile.password}'
                           f'@{camera_profile.ip_address}/{camera_profile.url}'
                           f'?streamprofile={camera_profile.profile}')

    while True:
        grabbed, frame = cap.read()
        # if not grabbed:
        #     break

        # if centerX is not None and centerY is not None:
        #     x1, x2 = 0, frame.shape[1]
        #     y1, y2 = centerY, centerY
        #     cv2.line(frame, (x1, y1), (x2, y2), (0, 255, 0), 1)
        #
        #     x1, x2 = centerX, centerX
        #     y1, y2 = 0, frame.shape[0]
        #     cv2.line(frame, (x1, y1), (x2, y2), (0, 255, 0), 1)

        orientation = quadrant_service.get_orientation(frame)
        if orientation is None or orientation.value % 90 == 0:
            continue

        cv2.imshow('frame', frame)
        cv2.setMouseCallback('frame', draw_rectangle)
        cv2.waitKey()




if __name__ == '__main__':
    main()
