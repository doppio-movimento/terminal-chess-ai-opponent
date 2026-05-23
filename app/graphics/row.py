import graphics.colors as colors
from graphics.square import Square


class Row:
    def __init__(
        self, number, contents, color_scheme, pad_length, square_height, square_width
    ):
        self.number = number
        self.contents = contents
        self.primary_color = color_scheme["board_color_1"]
        self.secondary_color = color_scheme["board_color_2"]
        self.label_color = color_scheme["label_color"]
        self.border_color = color_scheme["border_color"]
        self.pad_length = pad_length
        self.square_height = square_height
        self.square_width = square_width
        self.squares = []
        for index, piece in enumerate(contents):
            color = (
                (self.secondary_color if index % 2 == 0 else self.primary_color)
                if self.number % 2 == 0
                else (self.primary_color if index % 2 == 0 else self.secondary_color)
            )
            self.squares.append(
                Square(
                    number, index, piece, color, self.square_height, self.square_width
                )
            )

    def __str__(self):
        row_string = ""
        for line_number in range(self.square_height):
            for index, square in enumerate(self.squares):
                if line_number == 2:
                    row_string += (
                        (
                            (
                                (self.pad_length - 2) * " "
                                + self.label_color
                                + self.border_color
                                + " "
                                + str(8 - self.number)
                            )
                            if index == 0
                            else ""
                        )
                        + square.get_line(line_number)
                        + (colors.BLACK_BG if index == 7 else "")
                    )
                    row_string += (
                        self.border_color
                        + self.label_color
                        + str(8 - self.number)
                        + " "
                        + colors.BLACK_BG
                        if index == 7
                        else ""
                    )
                else:
                    row_string += (
                        (
                            ((self.pad_length - 2) * " " + self.border_color + 2 * " ")
                            if index == 0
                            else ""
                        )
                        + square.get_line(line_number)
                        + (colors.BLACK_BG if index == 7 else "")
                    )
                    row_string += (
                        self.border_color + 2 * " " + colors.BLACK_BG
                        if index == 7
                        else ""
                    )
            row_string += "\n"
        return row_string

    def get_square(self, number):
        return self.squares[number]

    def highlight(self, square_nums, color):
        if square_nums:
            for index in square_nums:
                self.squares[index].highlight(color)

    def select(self, index, color):
        print(index)
        self.squares[index].select(color)
