from services.RegionService import RegionService
from models.config import Config
import cv2
from models.orientation import Orientation
from models.cube_detection_result import QuadrantDetectionResult




class QuadrantService:
    def get_orientation(self, img):
        config = Config.from_json("config.json")
        regions = config.quadrant_regions
        detected_quadrant_positions = []

        regionService = RegionService()
        for region in regions:
            color_name = regionService.get_region_color_name(img, region, config.colors, 30)
            if(color_name == "white"):
                detected_quadrant_positions.append(QuadrantDetectionResult(region, color_name))

        return self.quadrant_position(detected_quadrant_positions)



    def unstructured_test(self, img):
        regionService = RegionService()
        color = regionService.get_region_color_name()


    def quadrant_position(self, detected_quadrant_positions):
        detected_positon = detected_quadrant_positions[1]
        if detected_positon == "right":
            return Orientation.FRONT
        if detected_positon == "right_front":
            return Orientation.FRONT_EDGE
        if detected_positon == "front":
            return Orientation.RIGHT
        if detected_positon == "front_left":
            return Orientation.RIGHT_EDGE
        if detected_positon == "left":
            return Orientation.BACK
        if detected_positon == "left_back":
            return Orientation.BACK_EDGE
        if detected_positon == "back":
            return Orientation.LEFT
        if detected_positon == "back_right":
            return Orientation.FRONT

