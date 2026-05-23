from os import get_terminal_size
from sys import path

import graphics.colors as colors
from graphics.row import Row
from transformations.mapping import map_coordinates


class Board:
    def __init__(self, color_scheme, configuration, sq_dim=[5, 13]):
        self.square_height = sq_dim[0]
        self.square_width = sq_dim[1]
        self.border_width = 2
        self.width = 8 * self.square_width + 2 * self.border_width
        self.pad_length = int((get_terminal_size().columns - self.width) / 2) + 2
        self.color_scheme = color_scheme
        self.configuration = configuration
        self.rows = []
        self.selected_row = None
        self.selected_column = None
        self.__set_rows()

    def __str__(self):
        board_string = self.__insert_horizontal_border("") + "\n"
        board_string = "".join(
            tuple(board_string) + tuple(str(self.rows[i]) for i in range(8))
        )
        board_string = (
            f"{colors.BLACK_BG}\n\n"
            + self.__insert_horizontal_border(board_string)
            + f"{colors.BLACK_BG}\n\n"
        )
        return board_string

    def get_width(self):
        return self.width

    def get_squares(self, destinations):
        squares = []
        for destination in destinations:
            computer_coords = map_coordinates(destination)
            squares.append(self.rows[computer_coords[0]].get_square(computer_coords[1]))
        return squares[0] if len(squares) == 1 else tuple(squares)

    def update_configuration(self, config):
        self.configuration = config
        self.rows = []
        self.__set_rows()

    def highlight_piece(self, piece):
        coordinates = piece.get_coordinates()
        self.rows[coordinates[0]].select(coordinates[1], colors.BRIGHT_YELLOW)

    def highlight_moves(self, coordinates, color):
        d = {}
        for elem in coordinates:
            try:
                d[elem[0]].append(elem[1])
            except KeyError:
                d[elem[0]] = [elem[1]]
        for key in d.keys():
            self.rows[key].highlight(d[key], color)

    def __set_rows(self):
        self.rows = [
            Row(
                i,
                self.configuration[i],
                self.color_scheme,
                self.pad_length,
                self.square_height,
                self.square_width,
            )
            for i in range(8)
        ]

    def __insert_horizontal_border(self, board_string):
        return "".join(
            [
                board_string,
                (self.pad_length - self.border_width) * " ",
                self.color_scheme["label_color"],
                self.color_scheme["border_color"],
                2 * " ",
            ]
            + [
                f"{6 * ' '}{letter}{6 * ' '}"
                + (f"{2 * ' '}{colors.BLACK_BG}{colors.RED}" if letter == "H" else "")
                for letter in "ABCDEFGH"
            ]
        )
