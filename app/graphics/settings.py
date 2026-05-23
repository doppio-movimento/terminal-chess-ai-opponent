from os import system

from pynput import keyboard


def cursor_off():
    print("\033[?25l", end="")


def move_cursor_to(point):
    print("\033[%d;%dH" % (point[0], point[1]), end="", flush=True)


def print_horizontally_centered(string, line_number, string_length, screen_width):
    move_cursor_to((line_number, screen_width / 2 - string_length / 2))
    print(string, end="", flush=True)


class Settings:

    def __init__(self, terminal_dimensions):
        self.terminal_height = terminal_dimensions.lines
        self.terminal_width = terminal_dimensions.columns
        self.p1_primary_color = None
        self.p1_secondary_color = None
        self.p2_primary_color = None
        self.p2_secondary_color = None
        self.board_color_one = None
        self.board_color_two = None
        self.board_border_color = None
        self.board_border_labels_color = None
        self.board_square_labels_color = None

    def get_background_color(self, face, row, column):
        color_code = 16 + 36 * row + face * 6 + column
        return "\x1b[48;5;" + str(color_code) + "m"

    def request_settings(self):
        cursor_off()
        system("clear")
        print_horizontally_centered(
            "Choose your color scheme",
            2,
            len("Choose your color scheme"),
            self.terminal_width,
        )
        print_horizontally_centered(
            "BOARD GOES HERE", 10, len("BOARD GOES HERE"), self.terminal_width
        )

        start = 50
        color_coordinates = [0, 0]
        k = 0
        color_row = ""
        for face in range(6):
            for row in range(6):
                for column in range(6):
                    color_row += self.get_background_color(face, row, column) + "  "
                color_row += "\x1b[0m "
                print_horizontally_centered(
                    color_row, start + k, 78, self.terminal_width
                )
            k += 1
            color_row = ""

        def on_press(key):
            try:
                if key == keyboard.Key.right:
                    move_cursor_to(
                        (start, self.terminal_width / 2 - 78 / 2 + 2 * location)
                    )
                    print("[]", end="", flush=True)
            except AttributeError:
                pass

        def on_release(key):
            if key == keyboard.Key.esc:
                return False

        settings_incomplete = True
        listener = keyboard.Listener(
            on_press=on_press, on_release=on_release, suppress=True
        )
        listener.start()
        while settings_incomplete:
            pass
