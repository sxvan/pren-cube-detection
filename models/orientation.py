from enum import Enum


class Orientation(Enum):
    FRONT = 0
    FRONT_EDGE = 45
    RIGHT = 90
    RIGHT_EDGE = 135
    BACK = 180
    BACK_EDGE = 225
    LEFT = 270
    LEFT_EDGE = 315
