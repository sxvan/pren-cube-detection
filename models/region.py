from models.cube_position import CubePosition


class Region:
    def __init__(self, coord, width, height,
                 min_color_coverage, max_color_coverage=1,
                 only_missing=False, when_missing=None, when_different=None):
        self.coord = tuple(coord)
        self.width = width
        self.height = height
        self.min_color_coverage = min_color_coverage
        self.max_color_coverage = max_color_coverage
        self.only_missing = only_missing

        if when_missing is None:
            when_missing = []
        self.when_missing = [CubePosition[position.upper()] for position in when_missing]

        if when_different is None:
            when_different = []
        self.when_different = [CubePosition[position.upper()] for position in when_different]
