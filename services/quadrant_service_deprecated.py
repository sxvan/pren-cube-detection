from models.color_range import ColorRange
from models.orientation import Orientation
from services.color_service import ColorService
from services.image_service import ImageService
import cv2 as cv


class QuadrantServiceDeprecated:
    def get_orientation(self, img):
        return None
        return Orientation.FRONT

    def is_start_position(self, img):
        image_service = ImageService()
        color_service = ColorService()

        img = color_service.get_img_in_color_ranges(img, [ColorRange((0, 0, 100), (255, 50, 200))])
        img = color_service.grayscale_img(img)
        img = image_service.blur_img(img, 3)

        angles = image_service.get_angles_of_straight_lines(img, 200)
        if len(angles) > 1:
            if -145 -2 <= angles[0] <= -145 + 2:
                if 145 -2 <= angles[1] <= 145 + 2:
                    return True

        return False

    def get_angles(self, img):
        image_service = ImageService()
        color_service = ColorService()

        img = color_service.get_img_in_color_ranges(img, [ColorRange((0, 0, 100), (255, 50, 200))])
        img = color_service.grayscale_img(img)
        img = image_service.blur_img(img, 3)

        angles = image_service.get_angles_of_straight_lines(img, 250)

    def get_middle_angle(self, angle1, angle2):
        # If the difference between the two angles is greater than 180
        if abs(angle2 - angle1) > 180:
            # Add 360 to the smaller angle
            if angle1 < angle2:
                angle1 += 360
            else:
                angle2 += 360

        # Calculate the middle angle
        middle_angle = (angle1 + angle2) / 2

        # Normalize the middle angle to the range of 0 to 359
        middle_angle = middle_angle % 360

        return middle_angle


