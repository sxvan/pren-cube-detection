import colorsys

import cv2
import numpy as np

from models.color import Color
from models.color_range import ColorRange


class ColorService:
    def get_color(self, img, colors: [Color], min_coverage: float, max_coverage: float):
        for color in colors:
            if self._check_for_color(img, color, min_coverage, max_coverage):
                return color
        return None

    def _check_for_color(self, img, color: [Color], min_coverage: float, max_coverage: float):
        return max_coverage >= self._get_color_coverage(img, color.color_ranges) >= min_coverage

    def _get_color_coverage(self, img, color_ranges: [ColorRange]):
        output = self.__get_img_in_color_ranges(img, color_ranges)
        total_pixel_count = np.prod(img.shape[:2])
        color_pixel_count = np.count_nonzero(output)
        return color_pixel_count / total_pixel_count

    @staticmethod
    def generate_color_palette(min_hue, max_hue, min_saturation, max_saturation, min_value, max_value, num_colors):
        # Create an empty canvas for the color palette
        palette_width = num_colors
        palette_height = 100
        palette = np.zeros((palette_height, palette_width, 3), dtype=np.uint8)

        # Generate colors for the palette
        for i in range(palette_width):
            hue = min_hue + (max_hue - min_hue) * i / (palette_width - 1)
            saturation = min_saturation + (max_saturation - min_saturation) * i / (palette_width - 1)
            value = min_value + (max_value - min_value) * i / (palette_width - 1)
            palette[:, i, 0] = hue
            palette[:, i, 1] = saturation
            palette[:, i, 2] = value

        # Convert palette to 8-bit unsigned integer for display
        palette_display = cv2.cvtColor(palette, cv2.COLOR_HSV2BGR)

        # Display the color palette
        cv2.imshow('Color Palette (HSV)', cv2.resize(palette_display, (palette_width * 10, palette_height)))
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    @staticmethod
    def __get_img_in_color_ranges(img, color_ranges: [ColorRange]):
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        mask = np.zeros_like(hsv[:, :, 0], dtype=np.uint8)

        for color_range in color_ranges:
            current_mask = cv2.inRange(hsv, color_range.lower_color, color_range.upper_color)
            mask = cv2.bitwise_or(mask, current_mask)

        # result_img = cv2.bitwise_and(img, img, mask=mask)

        return mask
