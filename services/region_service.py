from services.color_service import ColorService


class RegionService:
    def __init__(self, color_service: ColorService):
        self.color_service = color_service

    def get_region_color_name(self, img, region, colors):
        region_img = self.__get_region_img(img, region)
        color = self.color_service.get_color(region_img, colors, region.min_color_coverage, region.max_color_coverage)
        name = ''
        if color:
            name = color.name

        return name

    def __get_region_img(self, img, region):
        x1 = int(region.coord[0] - region.width / 2)
        y1 = int(region.coord[1] - region.height / 2)
        x2 = int(x1 + region.width)
        y2 = int(y1 + region.height)

        return img[y1:y2, x1:x2]
