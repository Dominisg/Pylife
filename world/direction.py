import random
from enum import Enum


class Direction(Enum):
    RIGHT = (1, 0, 0, 0)
    LEFT = (-1, 0, 0, 0)
    DOWN = (1, 1, 0, 1)
    UP = (0, -1, -1, -1)
    HEXRIGHT = (1, -1, 0, -1)
    HEXLEFT = (0, 1, -1, 1)

    def __init__(self, xo, yo, xe, ye):
        self.xo = xo
        self.yo = yo
        self.xe = xe
        self.ye = ye

    def translate(self, point):
        if self == Direction.DOWN:
            point.x += self.xe
            point.y += self.ye
        else:
            point.x += self.xo
            point.y += self.yo

    def translate_hex(self, point):
        if point.y % 2 == 1:
            point.x += self.xo
            point.y += self.yo
        else:
            point.x += self.xe
            point.y += self.ye

    @staticmethod
    def get_dir(i):
        if i == 0:
            return Direction.RIGHT
        if i == 1:
            return Direction.LEFT
        if i == 2:
            return Direction.DOWN
        if i == 3:
            return Direction.UP
        if i == 4:
            return Direction.HEXRIGHT
        if i == 5:
            return Direction.HEXLEFT

    @staticmethod
    def random_direction():
        i = random.randrange(0, 4)
        return Direction.get_dir(i)

    @staticmethod
    def random_direction_hex():
        i = random.randrange(0, 6)
        return Direction.get_dir(i)


