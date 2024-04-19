import cv2
import numpy as np

from models.color import Color
from models.color_range import ColorRange


class ColorService:
    def get_color(self, img, colors: [Color], min_coverage: float, max_coverage: float):
        for color in colors:
            if self.__check_for_color(img, color, min_coverage, max_coverage):
                return color

        return None

    def __check_for_color(self, img, color: [Color], min_coverage: float, max_coverage: float):
        return max_coverage >= self.__get_color_coverage(img, color.color_ranges) >= min_coverage

    def __get_color_coverage(self, img, color_ranges: [ColorRange]):
        output = self.__get_img_in_color_ranges(img, color_ranges)
        total_pixel_count = output.size
        color_pixel_count = np.count_nonzero(output)
        return color_pixel_count / total_pixel_count

    @staticmethod
    def __get_img_in_color_ranges(img, color_ranges: [ColorRange]):
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        mask = np.zeros_like(hsv[:, :, 0], dtype=np.uint8)

        for color_range in color_ranges:
            current_mask = cv2.inRange(hsv, color_range.lower_color, color_range.upper_color)
            mask = cv2.bitwise_or(mask, current_mask)

        result_img = cv2.bitwise_and(img, img, mask=mask)

        return result_img
