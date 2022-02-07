from enum import Enum
from typing import List

CUBE_SIZE = 3
FACE_COUNT = 6

class Side(Enum):
    TOP = 0
    BACK = 1
    LEFT = 2
    FRONT = 3
    RIGHT = 4
    BOTTOM = 5


class Rotation(Enum):
    UP = 1
    CLOCKWISE = 2
    LEFT = 3
    DOWN = -1
    COUNTERCLOCKWISE = -2
    RIGHT = -3

    def inverse(self):
        return Rotation(-self.value)

class Color(Enum):
    GREEN = 0
    BLUE = 1
    RED = 2
    PURPLE = 3
    WHITE = 4
    YELLOW = 5


class Transposition(Enum):
    CLOCKWISE = 1
    COUNTERCLOCKWISE = -1


class Pixel(object):
    color: Color

    def __init__(self, color: Color):
        self.color = color

    def __str__(self):
        return self.color.name[0]


def _invert_offset(offset):
    if offset == 0:
        return 2
    elif offset == 2:
        return 0
    else:
        return 1


def _get_uniformity_score(pixels: List[Pixel]) -> int:
    colors = len(set(x.color for x in pixels))
    if colors == 3: return 0
    elif colors == 2: return 1
    elif colors == 1: return 3
    # return CUBE_SIZE - len(set(x.color for x in pixels))



class Face(object):
    side: Side
    rows: List[List[Pixel]]

    def __init__(self, side: Side, color: Color):
        self.side = side
        self.rows = []
        for row_num in range(0, CUBE_SIZE):
            self.rows.append([])
            for col_num in range(0, CUBE_SIZE):
                self.rows[row_num].append(Pixel(color))

    def get_row(self, row_num: int) -> List[Pixel]:
        if self.side == Side.TOP:
            row_num = _invert_offset(row_num)
        result = list(self.rows[row_num])
        if self.side == Side.BOTTOM:
            result.reverse()
        return result

    def set_row(self, row_num: int, pixels: List[Pixel]):
        if self.side == Side.TOP:
            row_num = _invert_offset(row_num)
        if self.side == Side.BOTTOM:
            pixels.reverse()
        self.rows[row_num] = pixels

    def get_column(self, column_num: int) -> List[Pixel]:
        result = []
        if self.side in [Side.BACK, Side.LEFT]:
            column_num = _invert_offset(column_num)
        for i in range(0, CUBE_SIZE):
            result.append(self.rows[i][column_num])
        if self.side in [Side.BACK, Side.LEFT]:
            result.reverse()
        return result

    def set_column(self, column_num: int, pixels: List[Pixel]):
        if self.side in [Side.BACK, Side.LEFT]:
            column_num = _invert_offset(column_num)
            pixels.reverse()
        for i in range(0, CUBE_SIZE):
            self.rows[i][column_num] = pixels[i]

    def transpose(self, direction: Transposition):
        toprow = list(self.rows[0])
        if direction == Transposition.CLOCKWISE:
            self.rows[0][0] = self.rows[2][0]
            self.rows[0][1] = self.rows[1][0]
            self.rows[0][2] = toprow[0]
            self.rows[1][0] = self.rows[2][1]
            self.rows[2][0] = self.rows[2][2]
            self.rows[2][1] = self.rows[1][2]
            self.rows[2][2] = toprow[2]
            self.rows[1][2] = toprow[1]
        elif direction == Transposition.COUNTERCLOCKWISE:
            self.rows[0][0] = self.rows[0][2]
            self.rows[0][1] = self.rows[1][2]
            self.rows[0][2] = self.rows[2][2]
            self.rows[1][2] = self.rows[2][1]
            self.rows[2][2] = self.rows[2][0]
            self.rows[2][1] = self.rows[1][0]
            self.rows[2][0] = toprow[0]
            self.rows[1][0] = toprow[1]
        else:
            raise ValueError('Invalid direction value %s', direction)


    def get_uniformity_score(self):
        uniformity_score = 0
        cols = [[None, None, None], [None, None, None], [None, None, None]]
        distinct_colors = set()
        for row_num in range(0, CUBE_SIZE):
            uniformity_score += _get_uniformity_score(self.rows[row_num])
            for col_num in range(0, CUBE_SIZE):
                cols[col_num][row_num] = self.rows[row_num][col_num]
                distinct_colors.add(self.rows[row_num][col_num].color)
        for col in cols:
            uniformity_score += _get_uniformity_score(col)
        #uniformity_score += FACE_COUNT - len(distinct_colors)
        return uniformity_score

    def is_uniform_color(self):
        first_color = self.rows[0][0]
        for row in self.rows:
            for pixel in row:
                if pixel.color != first_color:
                    return False
        return True


    def get_print_row(self, row_num: int):
        return str(self.rows[row_num][0]) + str(self.rows[row_num][1]) + str(self.rows[row_num][2])