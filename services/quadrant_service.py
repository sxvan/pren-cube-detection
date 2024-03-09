from services.region_service import RegionService


class QuadrantService:
    def get_orientation(self, img, quadrant_regions, colors):
        region_service = RegionService()
        for orientation, regions in quadrant_regions.items():
            region_not_met = False
            for region in regions:
                color_name = region_service.get_region_color_name(img, region, colors)
                if color_name == '':
                    region_not_met = True

            if not region_not_met:
                return orientation

        return None
