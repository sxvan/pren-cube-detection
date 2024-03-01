from enum import Enum


class QuadrantRegionPosition(Enum):
    RIGHT = 0
    RIGHT_FRONT = 45
    FRONT = 90
    FRONT_LEFT = 135
    LEFT = 180
    LEFT_BACK = 225
    BACK = 270
    BACK_RIGHT = 315
