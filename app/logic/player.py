from math import floor
from sys import path

import graphics.colors as colors
from transformations.mapping import map_coordinates

from .piece import Piece


class Player:
    def __init__(self, color, move_color, first=False):
        self.color = color
        self.move_color = move_color
        self.color_string = "white" if first else "black"
        self.first = first
        self.pieces = {
            name: Piece(
                name,
                self.color,
                self.color_string,
                (
                    7 - floor(index / 16 + 0.5) if first else floor(index / 16 + 0.5),
                    index % 8,
                ),
            )
            for index, name in enumerate(
                (
                    "r1",
                    "n1",
                    "b1",
                    "q1",
                    "k1",
                    "b2",
                    "n2",
                    "r2",
                )
                + tuple(map(lambda n: f"p{n}", range(1, 9)))
            )
        }

    def clear_double_jump_flag(self):
        for piece in self.pieces.values():
            piece.set_just_performed_double_jump(False)

    def get_number(self):
        return 1 if self.first else 2

    def remove_piece(self, piece_id):
        del self.pieces[piece_id]

    def promote_piece(self, old_piece, new_piece_name):
        if new_piece_name != "p":
            old_id = old_piece.get_id()
            new_id = "".join([new_piece_name, "3"])
            coordinates = old_piece.get_coordinates()
            self.remove_piece(old_id)
            self.pieces[new_id] = Piece(
                new_id, self.color, self.color_string, coordinates
            )

    def castle(self, king_side_castling=True):
        if king_side_castling:
            rook_destination = "f1" if self.first else "f8"
            king_destination = "g1" if self.first else "g8"
            self.move_piece("r2", rook_destination)
            self.move_piece("k1", king_destination)
        else:
            rook_destination = "c1" if self.first else "c8"
            king_destination = "b1" if self.first else "b8"
            self.move_piece("r1", rook_destination)
            self.move_piece("k1", king_destination)

    def move_piece(self, piece_id, destination):
        computer_coords = map_coordinates(destination)
        piece = self.pieces[piece_id]
        if piece.get_rank() == "p":
            current_coords = piece.get_coordinates()
            if abs(computer_coords[0] - current_coords[0]) == 2:
                piece.set_just_performed_double_jump(True)
        piece.update_coordinates(computer_coords[0], computer_coords[1])
        piece.set_moved()
        promotion_possible = piece.get_rank() == "p" and (
            computer_coords[0] == 0 if self.first else computer_coords[0] == 7
        )
        if promotion_possible:
            chosen_piece = ""
            while chosen_piece not in {"q", "b", "r", "n"}:
                chosen_piece = input("Promote pawn to: ")
                if chosen_piece not in {"q", "b", "r", "n"}:
                    print(
                        f"{colors.MAGENTA}PROMOTION ERROR: {chosen_piece}{colors.GREEN}"
                    )
            self.promote_piece(piece, chosen_piece)

    def get_all_pieces(self):
        return set(self.pieces.values())

    def get_piece(self, piece_id):
        try:
            piece = self.pieces[piece_id]
        except KeyError:
            piece = None
        return piece

    def get_color(self):
        return self.color
