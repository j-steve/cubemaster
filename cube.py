from face import Face
from face import Side
from face import Color
from face import Rotation
from face import FACE_COUNT
from face import Transposition
from typing import List



class Cube(object):
    faces: List[Side]

    def __init__(self):
        self.faces = []
        for side in Side:
            self.faces.append(Face(side, Color(side.value)))

    def rotate(self, direction: Rotation, offset: int):
        if direction == Rotation.LEFT:
            front_row = self[Side.FRONT].get_row(offset)
            self[Side.FRONT].set_row(offset, self[Side.RIGHT].get_row(offset))
            self[Side.RIGHT].set_row(offset, self[Side.BACK].get_row(offset))
            self[Side.BACK].set_row(offset, self[Side.LEFT].get_row(offset))
            self[Side.LEFT].set_row(offset, front_row)
            if offset == 0:
                self[Side.TOP].transpose(Transposition.CLOCKWISE)
            elif offset == 2:
                self[Side.BOTTOM].transpose(Transposition.COUNTERCLOCKWISE)
        if direction == Rotation.RIGHT:
            for i in range(0, 3):
                self.rotate(Rotation.LEFT, offset)
        if direction == Rotation.UP:
            front_col = self[Side.FRONT].get_column(offset)
            self[Side.FRONT].set_column(offset, self[Side.BOTTOM].get_column(offset))
            self[Side.BOTTOM].set_column(offset, self[Side.BACK].get_column(offset))
            self[Side.BACK].set_column(offset, self[Side.TOP].get_column(offset))
            self[Side.TOP].set_column(offset, front_col)
            if offset == 0:
                self[Side.LEFT].transpose(Transposition.COUNTERCLOCKWISE)
            elif offset == 2:
                self[Side.RIGHT].transpose(Transposition.CLOCKWISE)
        if direction == Rotation.DOWN:
            for i in range(0, 3):
                self.rotate(Rotation.UP, offset)
        if direction == Rotation.COUNTERCLOCKWISE:
            rightcol = self[Side.RIGHT].get_column(offset)
            self[Side.RIGHT].set_column(offset, self[Side.BOTTOM].get_row(offset))
            self[Side.BOTTOM].set_row(offset, self[Side.LEFT].get_column(offset))
            self[Side.LEFT].set_column(offset, self[Side.TOP].get_row(offset))
            self[Side.TOP].set_row(offset, rightcol)
            if offset == 0:
                self[Side.FRONT].transpose(Transposition.COUNTERCLOCKWISE)
            elif offset == 2:
                self[Side.BACK].transpose(Transposition.CLOCKWISE)
        if direction == Rotation.CLOCKWISE:
            for i in range(0, 3):
                self.rotate(Rotation.COUNTERCLOCKWISE, offset)

    def get_uniformity_score(self):
        uniformity_score = 0
        for face in self.faces:
            uniformity_score += face.get_uniformity_score()
        return uniformity_score

    def is_solved(self):
        for face in self.faces:
            if not face.is_uniform_color():
                return False
        return True

    def __getitem__(self, key):
        if key in Side:
            return self.faces[key.value]

    def print(self):
        print(' ' * 8 + self.faces[0].get_print_row(0))
        print(' ' * 8 + self.faces[0].get_print_row(1))
        print(' ' * 8 + self.faces[0].get_print_row(2))
        print(self.faces[1].get_print_row(0) + ' ' + self.faces[2].get_print_row(0) + ' ' + self.faces[3].get_print_row(
            0) + ' ' + self.faces[4].get_print_row(0))
        print(self.faces[1].get_print_row(1) + ' ' + self.faces[2].get_print_row(1) + ' ' + self.faces[3].get_print_row(
            1) + ' ' + self.faces[4].get_print_row(1))
        print(self.faces[1].get_print_row(2) + ' ' + self.faces[2].get_print_row(2) + ' ' + self.faces[3].get_print_row(
            2) + ' ' + self.faces[4].get_print_row(2))
        print(' ' * 8 + self.faces[5].get_print_row(0))
        print(' ' * 8 + self.faces[5].get_print_row(1))
        print(' ' * 8 + self.faces[5].get_print_row(2))
        print()

    def __eq__(self, other):
        if isinstance(other, Cube):
            for i in range(0, FACE_COUNT):
                if self.faces[i] != other.faces[i]:
                    return False
            return True
        return False

