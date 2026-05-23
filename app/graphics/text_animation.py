from math import ceil
from time import sleep

import numpy as np
from colorama import init

import graphics.colors as colors


def cursor_off():
    print("\033[?25l", end="")


def move_cursor_to(point):
    print("\033[%d;%dH" % (point[0], point[1]), end="", flush=True)


def type_line(string, delay=0.000002):
    for char in string:
        print(char, end="", flush=True)
        sleep(delay)


def type_matrix(matrix):
    for line in matrix:
        line += "\n"
        type_line(line)


def replace_color(p, old_color, new_color):
    return new_color + p.strip(old_color)


def randomly_traverse(height, width, content, delay=0.00001):
    sample_space = np.arange(1, (height - 1) * width)
    deletions = 0
    while deletions < (height - 1) * width - 1:
        sample = np.random.choice(sample_space)
        row = ceil(sample / width) - 1
        column = sample % width if sample % width != 0 else row * width
        sample_space = np.delete(sample_space, np.argwhere(sample_space == sample))
        deletions += 1
        move_cursor_to((row, column))
        try:
            pixel = content[row - 1][column - 2]
        except:
            pixel = colors.BRIGHT_GREEN + "X"
        if colors.BLACK in pixel:
            print(" ", end="")
        else:
            print(pixel, end="")
        sleep(delay)


def L_traverse(
    height, width, trans_color, final_color, trans_char, final_char, delay=0.000001
):
    for r in range(height - 1):
        for c in range(width):
            move_cursor_to((r, c))
            print(f"{trans_color}{trans_char}", end="")
            sleep(delay)
            move_cursor_to((r, c))
            print(f"{final_color}{final_char}", end="")


def gamma_traverse(height, width, cursor, cursor_color, content, delay=0.0001):
    for r in range(height - 1):
        direction = "left" if r % 2 == 0 else "right"
        for c in range(width) if direction == "left" else range(width - 1, -1, -1):
            if direction == "left":
                move_cursor_to((height - r, c))
            else:
                move_cursor_to((height - r, c - 1))
            if c == 1 or c == width - 1:
                print(f"{cursor_color}{cursor}", end="", flush=True)
            else:
                print(f"{cursor_color}{2 * cursor}", end="", flush=True)
            move_cursor_to((height - r, c))
            sleep(0.001)
            pixel = content[height - r - 1][c]
            print(pixel, end="", flush=True)
            sleep(delay)


def reverse_gamma_traverse(
    height, width, trans_color, final_color, trans_char, content, delay=0.00000001
):
    for r in range(height - 1):
        for c in range(width):
            move_cursor_to((height - r, width - c))
            print(f"{trans_color}{trans_char}", end="")
            sleep(delay)
            move_cursor_to((height - r, width - c))
            print(f"{content[height - r - 1][width - c - 1]}", end="")


def color_diagonal(slant):
    i = 0
    for j in range(195):
        move_cursor_to((195 - j, 1 + slant * i))
        print(colors.BRIGHT_RED + "X", end="")
        sleep(0.00001)
        i += 1


def print_grid(width, height, images, delay=0.0001):
    init(autoreset=True)
    cursor_off()
    print((height - 1) * "\n", end="")
    print("\033[%d;%dH" % (1, 1), end="")
    cursor = "\u2B25"
    flip_char = " "
    # L_traverse(height, width, colors.MAGENTA, colors.WHITE, flip_char, grid_char)
    # gamma_traverse(height, width, cursor, colors.MAGENTA, content_a)
    # L_traverse(height, width, colors.CYAN, colors.BLUE, flip_char, grid_char)
    # gamma_traverse(height, width, cursor, colors.MAGENTA, content_b)
    # L_traverse(height, width, colors.BRIGHT_RED, colors.RED, flip_char, grid_char)
    # gamma_traverse(height, width, cursor, colors.MAGENTA, content_c)
    for image in images:
        randomly_traverse(height, width, image)
    move_cursor_to((height, width))
