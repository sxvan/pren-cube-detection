import numpy as np

from services.color_service import ColorService


class RegionService:
    def __init__(self, color_service: ColorService):
        self._color_service = color_service

    def get_region_color_name(self, img, region, colors):
        region_img = self._get_region_img(img, region)
        # print(np.mean(region_img))
        color = self._color_service.get_color(region_img, colors, region.min_color_coverage, region.max_color_coverage)
        if color:
            return color.name

        return ''

    @staticmethod
    def _get_region_img(img, region):
        x1 = int((region.coord[0] - region.width / 2))
        y1 = int((region.coord[1] - region.height / 2))
        x2 = int(x1 + region.width)
        y2 = int(y1 + region.height)

        return img[y1:y2, x1:x2]
