import cv2
from models.config import Config

#config = Config.from_json("config.json")

def click_event(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        print(f"Coordinates: ({x}, {y})")


capture = cv2.VideoCapture("assets/pren_cube_01.mp4")

frame_numbers = [109, 219, 330, 444, 560,670,786, 895]

for frame_number in frame_numbers:
    capture.set(1, frame_number)
    _, frame = capture.read()

    cv2.imshow('Image', frame)

    # Set the mouse callback function for the window
    cv2.setMouseCallback('Image', click_event)

    # Wait for any key to close the window
    cv2.waitKey(0)

    # Close all OpenCV windows
    cv2.destroyAllWindows()