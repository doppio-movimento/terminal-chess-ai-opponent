from itertools import filterfalse, product

from . import aux


def get_pawn_moves(piece, player, state):
    legal_moves = set()
    coordinates = piece.get_coordinates()
    player_number = player.get_number()

    move1 = (coordinates[0] + (-1) ** player_number, coordinates[1])
    move2 = (coordinates[0] + 2 * ((-1) ** player_number), coordinates[1])

    if not state[move1[0]][move1[1]]:
        legal_moves.add(move1)
    if (
        piece.is_unmoved()
        and not state[move1[0]][move1[1]]
        and not state[move2[0]][move2[1]]
    ):
        legal_moves.add(move2)

    for i in [-1, 1]:
        square1 = (coordinates[0] + (-1) ** player_number, coordinates[1] + i)
        square2 = (coordinates[0], coordinates[1] + i)
        piece = None
        if aux.is_on_chess_board(square2):
            piece = state[square2[0]][square2[1]]
        if aux.contains_enemy_piece(square1, state, player) or (
            piece and piece.get_just_performed_double_jump()
        ):
            legal_moves.add(
                (coordinates[0] + (-1) ** player_number, coordinates[1] + i)
            )

    return legal_moves


def get_rook_moves(piece, player, state):
    directions = {"up", "down", "right", "left"}
    return get_rook_or_bishop_moves(**locals())


def get_bishop_moves(piece, player, state):
    directions = set(
        map(lambda t: "".join(t), product({"up", "down"}, {"right", "left"}))
    )
    return get_rook_or_bishop_moves(**locals())


def get_knight_moves(piece, player, state):
    filtration = lambda pair: abs(pair[0]) == abs(pair[1])
    cartesian_product = product({-2, -1, 1, 2}, repeat=2)
    return get_knight_or_king_moves(**locals())


def get_king_moves(piece, player, state):
    filtration = lambda pair: pair == (0, 0)
    cartesian_product = product(range(-1, 2), repeat=2)
    return get_knight_or_king_moves(**locals())


def get_knight_or_king_moves(piece, player, state, filtration, cartesian_product):
    coordinates = piece.get_coordinates()
    return set(
        filter(
            lambda move: aux.is_on_chess_board(move)
            and not state[move[0]][move[1]]
            or aux.contains_enemy_piece(move, state, player),
            tuple(
                (coordinates[0] + ord_pair[0], coordinates[1] + ord_pair[1])
                for ord_pair in filterfalse(filtration, cartesian_product)
            ),
        )
    )


def get_queen_moves(piece, player, state):
    return get_rook_moves(**locals()) | get_bishop_moves(**locals())


def get_rook_or_bishop_moves(piece, player, state, directions):
    legal_moves = set()
    coordinates = piece.get_coordinates()
    for direction in directions:
        i = "up" in direction or "down" in direction
        j = "left" in direction or "right" in direction
        destination = (
            coordinates[0] + (i if "down" in direction else -i),
            coordinates[1] + (j if "right" in direction else -j),
        )
        while aux.is_on_chess_board(destination) and not aux.contains_piece(
            destination, state
        ):
            legal_moves.add(destination)
            i += "up" in direction or "down" in direction
            j += "left" in direction or "right" in direction
            destination = (
                coordinates[0] + (i if "down" in direction else -i),
                coordinates[1] + (j if "right" in direction else -j),
            )
        if aux.is_on_chess_board(destination) and aux.contains_enemy_piece(
            destination, state, player
        ):
            legal_moves.add(destination)
    return legal_moves
