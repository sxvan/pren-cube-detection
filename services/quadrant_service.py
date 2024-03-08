from models.cube_position import CubePosition
from services.region_service import RegionService
from models.config import Config
import cv2
from models.orientation import Orientation
from models.quadrant_region_position import QuadrantRegionPosition
from models.quadrant_detection_result import QuadrantDetectionResult




class QuadrantService:
    def get_orientation(self, img):
        config = Config.from_json("../config.json")
        regions = config.quadrant_regions  # Assuming a method to get quadrant_regions
        detected_quadrant_positions = []

        regionService = RegionService()
        for region in regions:
            color_name = regionService.get_region_color_name(img, region, config.colors, 1)
            print(color_name)
            if(color_name == "white"):
                detected_quadrant_positions.append(region)

        return self.quadrant_position(detected_quadrant_positions)

    def quadrant_position(self, detected_quadrant_positions):
        mapping = {
            #CubePosition.BOTTOM_FRONT_RIGHT: Orientation.FRONT_EDGE,

            QuadrantRegionPosition.RIGHT: Orientation.FRONT,
            QuadrantRegionPosition.RIGHT_FRONT: Orientation.FRONT_EDGE,
            QuadrantRegionPosition.FRONT: Orientation.RIGHT,
            QuadrantRegionPosition.FRONT_LEFT: Orientation.RIGHT_EDGE,
            QuadrantRegionPosition.LEFT: Orientation.BACK,
            QuadrantRegionPosition.LEFT_BACK: Orientation.BACK_EDGE,
            QuadrantRegionPosition.BACK: Orientation.LEFT,
            QuadrantRegionPosition.BACK_RIGHT: Orientation.FRONT_EDGE,
        }
        if len(detected_quadrant_positions) > 0:
            detected_position = detected_quadrant_positions[0].position
            return mapping.get(detected_position)
        else:
            return


def main():
    config = Config.from_json("../config.json")

    quadrant_service = QuadrantService()

    capture = cv2.VideoCapture("../assets/pren_cube_01.mp4")


    capture.set(1, 435)
    _, frame = capture.read()
    service = QuadrantService()

    result = service.get_orientation(frame)


    # quadrant_service = QuadrantService()
    #
    # # Load your image
    # img = cv2.imread("path_to_your_image.jpg")
    #
    # # Get the orientation
    # orientation = quadrant_service.get_orientation(img)

    # Print the result
    print("Detected orientation:", result)

if __name__ == "__main__":
    main()