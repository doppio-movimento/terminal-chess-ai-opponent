from sys import path

from graphics.pieces import pieces


class Piece:
    def __init__(self, piece_id, color, color_string, coordinates):
        self.id = piece_id
        self.rank = piece_id[0]
        self.color = color
        self.color_string = color_string
        self.coordinates = coordinates
        self.just_performed_double_jump = False
        self.unmoved = True

    def __str__(self):
        return "".join(
            tuple(f"{pieces[self.rank].strip('\n').split('\n')[i]}\n" for i in range(3))
        )

    def get_just_performed_double_jump(self):
        if self.rank != "p":
            return False
        return self.just_performed_double_jump

    def set_just_performed_double_jump(self, val):
        self.just_performed_double_jump = val

    def is_unmoved(self):
        return self.unmoved

    def set_moved(self):
        self.unmoved = False

    def update_coordinates(self, row, column):
        self.coordinates = (row, column)

    def get_id(self):
        return self.id

    def get_rank(self):
        return self.rank

    def get_color(self):
        return self.color

    def get_color_string(self):
        return self.color_string

    def get_coordinates(self):
        return self.coordinates

    def row(self):
        return self.coordinates[0]

    def column(self):
        return self.coordinates[1]
