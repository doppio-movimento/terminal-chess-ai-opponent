import graphics.colors as colors


class Square:
    def __init__(self, row, column, piece, color, height, width):
        self.contains_selected_piece = False
        self.highlighted = False
        self.selection_color = colors.GREEN_BG
        self.highlight_color = colors.GREEN
        self.piece = piece
        self.bg_color = color
        self.height = height
        self.width = width
        self.lines = [None] * self.height
        self.label = f"{chr(column + 65)}{8 - row}"
        self.set_lines()

    def get_piece(self):
        return self.piece

    def select(self, selection_color):
        self.contains_selected_piece = True
        self.selection_color = selection_color

    def highlight(self, highlight_color):
        self.highlighted = True
        self.highlight_color = highlight_color

    def set_lines(self):
        self.lines[0] = self.bg_color + (self.width - 2) * " "
        if self.piece:
            text_color = colors.RED if self.bg_color == colors.BLACK_BG else colors.BLACK
            self.lines[0] += f"{text_color}{self.piece.get_id()[-1]} "
            icon = str(self.piece).split("\n")
            if self.highlighted:
                for j in range(3):
                    self.lines[j + 1] = (
                        f"{self.bg_color}{2 * ' '}"
                        + f"{self.highlight_color}{2 * ' '}"
                        + f"{self.piece.color}{icon[j]}"
                        + f"{(colors.MAGENTA + self.label) if (j == 2) else 2 * ' '}"
                        + f"{self.bg_color}{2 * ' '}"
                    )
            elif self.contains_selected_piece:
                for j in range(3):
                    self.lines[j + 1] = ( 
                        f"{self.bg_color}{4 * ' '}"
                        + f"{self.highlight_color}{icon[j]}"
                        + f"{4 * ' '}"
                    )
            else:
                for j in range(3):
                    self.lines[j + 1] = (
                        f"{self.bg_color}{4 * ' '}"
                        + f"{self.piece.color}{icon[j]}"
                        + f"{self.bg_color}{4 * ' '}"
                    )
        else:
            self.lines[0] += 2 * " "
            for j in range(1, self.height - 1):
                self.lines[j] = (
                        f"{self.bg_color}{2 * ' '}"
                        + f"{self.highlight_color}{(self.width - 6) * ' '}"
                        + f"{(colors.MAGENTA + self.label) if (self.highlighted and j == 3) else 2 * ' '}"
                        + f"{self.bg_color}{2 * ' '}"
                )
        self.lines[self.height - 1] = self.bg_color + self.width * " "

    def get_line(self, number):
        self.set_lines()
        return self.lines[number]
