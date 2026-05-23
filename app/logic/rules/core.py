from . import primary

def get_legal_moves(piece, player, state):
    if piece.get_rank() == "p":
        return primary.get_pawn_moves(piece, player, state)
    elif piece.get_rank() == "b":
        return primary.get_bishop_moves(piece, player, state)
    elif piece.get_rank() == "n":
        return primary.get_knight_moves(piece, player, state)
    elif piece.get_rank() == "r":
        return primary.get_rook_moves(piece, player, state)
    elif piece.get_rank() == "k":
        return primary.get_king_moves(piece, player, state)
    else:
        return primary.get_queen_moves(piece, player, state)


def castling_possible(player, board, columns):
    squares = board.get_squares((f"{c}{7 * player.get_number() - 6}" for c in columns))
    king = player.get_piece("k1")
    rook = player.get_piece(f"r{2 if columns == 'fg' else 1}")
    return bool(king and rook) and (
        king.is_unmoved()
        and rook.is_unmoved()
        and all(sq.get_piece() is None for sq in squares)
    )


def queen_side_castling_possible(player, board):
    columns = "bcd"
    return castling_possible(**locals())


def king_side_castling_possible(player, board):
    columns = "fg"
    return castling_possible(**locals())

def get_checking_pieces(current_player, other_player, state):
    king_location = other_player.get_piece("k1").get_coordinates()
    return set(
        filter(
            lambda piece: king_location in get_legal_moves(piece, current_player, state),
            current_player.get_all_pieces(),
        )
    )

def check_achieved(player, enemy, state):
    return len(get_checking_pieces(player, enemy, state)) > 0

def checkmate_achieved(current_player, other_player, state):
    return False
    # (1.) Is the king in check?
    checking_pieces = get_checking_pieces(current_player, other_player, state)
    if len(checking_pieces) == 0:
        return False
    # (2.) The king is in check. Now, are all of the king's possible moves into check?
    enemy_pieces = other_player.get_all_pieces()
    king = current_player.get_piece("k1")
    king_moves = get_legal_moves(king, current_player, state)
    print(king_moves)
    for move in king_moves:
        move_attackers = 0
        for piece in enemy_pieces:
            piece_moves = get_legal_moves(piece, other_player, state)
            for attacking_move in piece_moves:
                if attacking_move == move:
                    move_attackers += 1
        if move_attackers == 0:
            return False
    # (3.) The king is in check and can only move into check. If only
    #     one piece is checking the king, can that piece be blocked?
    print("all possible moves into check")
    if len(checking_pieces) > 1:
        return True
    [checking_piece] = checking_pieces  # <- singleton
    # Note that checking_piece cannot be a king.
    # Thus, it is either a pawn, knight, queen, rook, or bishop.
    # If it is a pawn or a knight, then it cannot be blocked.
    # Knights can't be blocked because they jump over other pieces.
    # Pawns cannot be blocked because, if they can attack, there is
    # no space between them and what they are attacking.
    if checking_piece.get_rank() in {"p", "n"}:
        return True
    # If we have gotten this far, then the checking piece is
    # either a rook, a queen, or a bishop. Each of these pieces
    # may have multiple movement vectors, but we only care about
    # the one that terminates in the opposing king. Can this
    # one path be blocked?
    blockable_check_path = set()
    c_coords, k_coords = checking_piece.get_coordinates(), king.get_coordinates()
    # ----
    # ROOK
    # ----
    if checking_piece.get_rank() == "r":
        if c_coords[0] == k_coords[0]:  # rook to left or right of king
            if c_coords[1] < k_coords[1]:  # rook to the left
                column = c_coords[1] + 1
                while column < k_coords[1]:
                    blockable_check_path.add((c_coords[0], column))
                    column += 1
            else:  # rook to the right
                column = c_coords[1] - 1
                while column > k_coords[1]:
                    blockable_check_path.add((c_coords[0], column))
                    column -= 1
        else:  # rook above or below king
            if c_coords[0] < k_coords[0]:  # rook below king
                row = c_coords[0] + 1
                while row < k_coords[0]:
                    blockable_check_path.add((row, c_coords[1]))
                    row += 1
            else:  # rook above king
                row = c_coords[0] - 1
                while row > k_coords[0]:
                    blockable_check_path.add((row, c_coords[1]))
                    row -= 1
    # ------
    # BISHOP
    # ------
    if checking_piece.get_rank() == "b":
        if c_coords[0] < k_coords[0] and c_coords[1] < k_coords[1]:  # att from bot left
            row, column = c_coords[0] + 1, c_coords[1] + 1
            while row < k_coords[0]:
                blockable_check_path.add((row, column))
                row += 1
                column += 1
        if (
            c_coords[0] < k_coords[0] and c_coords[1] > k_coords[1]
        ):  # att. from bot right
            row, column = c_coords[0] + 1, c_coords[1] - 1
            while row < k_coords[0]:
                blockable_check_path.add((row, column))
                row += 1
                column -= 1
        if (
            c_coords[0] > k_coords[0] and c_coords[1] < k_coords[1]
        ):  # att. from top left
            row, column = c_coords[0] - 1, c_coords[1] + 1
            while row > k_coords[0]:
                blockable_check_path.add((row, column))
                row -= 1
                column += 1
        if (
            c_coords[0] > k_coords[0] and c_coords[1] < k_coords[1]
        ):  # att. from top right
            row, column = c_coords[0] - 1, c_coords[1] - 1
            while row > k_coords[0]:
                blockable_check_path.add((row, column))
                row -= 1
                column -= 1
    # -----
    # QUEEN
    # -----
    if checking_piece.get_rank() == "q":
        if c_coords[0] == k_coords[0] or c_coords[1] == k_coords[1]:  # queen as rook
            if c_coords[0] == k_coords[0]:  # rook to left or right of king
                if c_coords[1] < k_coords[1]:  # rook to the left
                    column = c_coords[1]
                    while column < k_coords[1]:
                        blockable_check_path.add((c_coords[0], column))
                        column += 1
                else:  # rook to the right
                    column = c_coords[1]
                    while column > k_coords[1]:
                        blockable_check_path.add((c_coords[0], column))
                        column -= 1
            else:  # rook above or below king
                if c_coords[0] < k_coords[0]:  # rook below king
                    row = c_coords[0]
                    while row < k_coords[0]:
                        blockable_check_path.add((row, c_coords[1]))
                        row += 1
                else:  # rook above king
                    row = c_coords[0]
                    while row > k_coords[0]:
                        blockable_check_path.add((row, c_coords[1]))
                        row -= 1
        else:  # queen attacking like a bishop
            if (
                c_coords[0] < k_coords[0] and c_coords[1] < k_coords[1]
            ):  # att from b left
                row, column = c_coords[0], c_coords[1]
                while row < k_coords[0]:
                    blockable_check_path.add((row, column))
                    row += 1
                    column += 1
            if (
                c_coords[0] < k_coords[0] and c_coords[1] > k_coords[1]
            ):  # att from b right
                row, column = c_coords[0], c_coords[1]
                while row < k_coords[0]:
                    blockable_check_path.add((row, column))
                    row += 1
                    column -= 1
            if (
                c_coords[0] > k_coords[0] and c_coords[1] < k_coords[1]
            ):  # att from t left
                row, column = c_coords[0], c_coords[1]
                while row > k_coords[0]:
                    blockable_check_path.add((row, column))
                    row -= 1
                    column += 1
            if (
                c_coords[0] > k_coords[0] and c_coords[1] < k_coords[1]
            ):  # att from t right
                row, column = c_coords[0], c_coords[1]
                while row > k_coords[0]:
                    blockable_check_path.add((row, column))
                    row -= 1
                    column -= 1

    friendly_pieces = current_player.get_all_pieces()
    for piece in friendly_pieces:
        if piece.get_rank() == "k":
            continue
        legal_moves = get_legal_moves(piece, current_player, state)
        if legal_moves & blockable_check_path:  # is intersection non-empty?
            return False

    # all conditions for checkmate met; return true
    return True


def get_blockable_check_path(piece, player, state):
    if piece.get_rank() in {"p", "n"}:
        return piece.get_coordinates()

