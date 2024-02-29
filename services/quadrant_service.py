from models.color_range import ColorRange
from services.color_service import ColorService
from services.image_service import ImageService


class QuadrantService:
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


