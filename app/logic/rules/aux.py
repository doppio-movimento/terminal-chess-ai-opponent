from functools import wraps
from itertools import product


def ensure_no_index_errors(func):
    @wraps(func)
    def wrapper(*args):
        if not is_on_chess_board(args[0]):
            return False
        return func(*args)

    return wrapper


def is_on_chess_board(coordinates):
    return coordinates in product(range(8), repeat=2)


@ensure_no_index_errors
def contains_enemy_piece(coordinates, state, player):
    piece = state[coordinates[0]][coordinates[1]]
    return piece is not None and player.get_color() != piece.get_color()


@ensure_no_index_errors
def contains_friendly_piece(coordinates, state, player):
    piece = state[coordinates[0]][coordinates[1]]
    return piece is not None and player.get_color() == piece.get_color()


@ensure_no_index_errors
def contains_piece(coordinates, state):
    piece = state[coordinates[0]][coordinates[1]]
    return piece is not None
