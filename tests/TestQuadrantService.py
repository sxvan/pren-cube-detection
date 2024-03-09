from models.orientation import Orientation
from services.quadrant_service import QuadrantService
import cv2 as cv  # Ensure OpenCV is installed and importable
from models.config import Config


# class TestQuadrantService:
#     def test_get_orientation(self):
#         quadrant_service = QuadrantService()
#
#         config = Config.from_json("config.json")
#
#         capture = cv.VideoCapture(config.video_source)
#
#
#         capture.set(1, 435)
#         _, frame = capture.read()
#
#         service = QuadrantService()
#
#         result = service.get_orientation(frame)
#
#         # Assert that result is of type Orientation
#         assert isinstance(result, Orientation.FRONT)

