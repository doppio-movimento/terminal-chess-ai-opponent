def get_checking_pieces(current_player, other_player, state):
    king_location = current_player.get_piece("k1").get_coordinates()
    return set(
        filter(
            lambda piece: king_location in get_legal_moves(piece, other_player, state),
            other_player.get_all_pieces(),
        )
    )


def checkmate_achieved(current_player, other_player, state):
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
