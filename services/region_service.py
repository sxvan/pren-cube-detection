from services.color_service import ColorService


class RegionService:
    def get_region_color_name(self, img, region, colors):
        color_service = ColorService()

        region_img = self.__get_region_img(img, region)
        color = color_service.get_color(region_img, colors, region.min_color_coverage, region.max_color_coverage)
        name = ''
        if color:
            name = color.name

        return name

    def __get_region_img(self, img, region):
        x1, y1 = region.coord
        x2, y2 = x1 + region.width, y1 + region.height

        return img[y1:y2, x1:x2]
