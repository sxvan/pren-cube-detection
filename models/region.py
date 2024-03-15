class Region:
    def __init__(self, coord, width, height, min_color_coverage, max_color_coverage=1):
        self.coord = tuple(coord)
        self.width = width
        self.height = height
        self.min_color_coverage = min_color_coverage
        self.max_color_coverage = max_color_coverage
