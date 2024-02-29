from models.region_position import RegionPosition


class RegionService:
    def get_img_region(self, img, region):
        x1, y1 = region.cords
        x2, y2 = x1 + region.width, y1 + region.height

        return img[y1:y2, x1:x2]
