import cv2

from models.config.config import Config
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
    def get_orientation(img):
        return quadrant_service.get_orientation(img, config.quadrant.regions, config.quadrant.colors)

    config = Config.from_json('config_new_new.json')

    color_service = ColorService()
    region_service = RegionService(color_service)
    quadrant_service = QuadrantService(region_service)
    # cube_service = CubeService(region_service)


    cap = cv2.VideoCapture('rtsp://' +
                           'pren' + ':' +
                           '463997' +
                           '@' + '147.88.48.131' +
                           '/axis-media/media.amp' +
                           '?streamprofile=' + 'pren_profile_medium')

    while True:
        grabbed, frame = cap.read()
        if not grabbed:
            break

        orientation = get_orientation(frame)
        if orientation is None:
            continue

        print(orientation)

        cv2.imshow('frame', frame)
        cv2.setMouseCallback('frame', draw_rectangle, {'frame': frame})
        cv2.waitKey()


if __name__ == '__main__':
    main()
