from sys import path
from time import sleep

import graphics.colors as colors
from artificial_intelligence.input_cleaner import get_corrected_input
from graphics.board import Board
from transformations.mapping import get_chess_coordinates, map_coordinates

import logic.rules.core as rules

## Game modes
DATA_COLLECTION = 0
HUMAN_VS_AI = 1

## Player types
HUMAN = 0
AI = 1


class Game:
    def __init__(self, white, black, file, ai_opponent=None, mode=DATA_COLLECTION):
        self.mode = mode
        self.player_one = white
        self.player_two = black
        self.file = file
        self.ai_opponent = ai_opponent
        self.current_player = self.player_one
        self.player_in_check = False
        piece_names = (
            "r1",
            "n1",
            "b1",
            "q1",
            "k1",
            "b2",
            "n2",
            "r2",
        ) + tuple(map(lambda n: f"p{n}", range(1, 9)))
        self.state = (
            [
                list(
                    map(
                        lambda name: black.get_piece(name),
                        piece_names[8 * i : 8 * (i + 1)],
                    )
                )
                for i in range(2)
            ]
            + [[None] * 8 for k in range(4)]
            + [
                list(
                    map(
                        lambda name: white.get_piece(name),
                        piece_names[8 * i : 8 * (i + 1)],
                    )
                )
                for i in reversed(range(2))
            ]
        )
        color_scheme = {
            "board_color_1": colors.WHITE_BG,
            "board_color_2": colors.BLACK_BG,
            "label_color": colors.BLACK,
            "border_color": colors.YELLOW_BG,
        }
        self.board = Board(color_scheme, self.state)

    def __str__(self):
        string = "[\n"

        for row_num, row in enumerate(self.state):
            string += 5 * "\t" + "["
            for column_letter, piece in zip("abcdefgh", row):
                if piece:
                    string += (
                        "\n"
                        + 6 * "\t"
                        + "{"
                        + f'"square": "{column_letter}{8 - row_num}", '
                        + f'"piece": "{piece.get_color_string()} {piece.get_id()}"'
                        + "}"
                    )
                    string += "," if column_letter != "h" else ""
                else:
                    string += (
                        "\n"
                        + 6 * "\t"
                        + "{"
                        + f'"square": "{column_letter}{8 - row_num}", '
                        + '"piece": "None"}'
                    )
                    string += "," if column_letter != "h" else ""
            string += "],\n"

        string = string.rstrip(",\n")

        string += "\n" + 4 * "\t" + "]"
        return string

    def __clear_state(self):
        self.state = [[None] * 8 for k in range(8)]

    def __destination_is_legal(self, destination, piece):
        computer_coords = map_coordinates(destination)
        return computer_coords in rules.get_legal_moves(
            piece, self.current_player, self.state
        )

    def __update_board(self, enemy):
        self.__clear_state()

        pieces_in_play = (
            self.player_one.get_all_pieces() | self.player_two.get_all_pieces()
        )

        for piece in pieces_in_play:
            self.state[piece.row()][piece.column()] = piece

        self.board.update_configuration(self.state)

        check_achieved = rules.check_achieved(self.current_player, enemy, self.state)
        if check_achieved:
            print("YOU ARE IN CHECK!")
        else:
            print("HI")

        self.current_player = (
            self.player_one
            if self.current_player is self.player_two
            else self.player_two
        )
        self.current_player.clear_double_jump_flag()


    def __save_training_data(self, piece_id, destination):
        data_string = (
            "{\n"
            + '\t"messages": [\n'
            + "\t\t{\n"
            + '\t\t\t"role": "system",\n'
            + '\t\t\t"content": "You are playing chess against a human. You need to return legal moves in JSON format based on the game state"\n'
            + "\t\t},\n"
            + "\t\t{\n"
            + '\t\t\t"role": "user",\n'
            + '\t\t\t"content": {\n'
            + '\t\t\t\t"game_state": '
            + str(self)
            + "\n"
            + "\t\t\t}\n"
            + "\t\t},\n"
            + "\t\t{\n"
            + '\t\t\t"role": "assistant",\n'
            + '\t\t\t"content": {\n'
            + '\t\t\t\t"piece": "'
            + piece_id
            + '",\n'
            + '\t\t\t\t"square": "'
            + destination
            + '"\n'
            + "\t\t\t}\n"
            + "\t\t}\n"
            + "\t]\n"
            + "}"
        )

        self.file.write(data_string + 2 * "\n")

    async def __get_move(self, check_achieved, player_type=HUMAN):
        legal_moves = set()
        feedback = ""
        while len(legal_moves) == 0:
            if player_type == HUMAN:
                piece_id = input(
                    f"{self.current_player.get_color()}Select piece:{colors.BLUE}{colors.BLACK_BG} "
                )
            else:
                piece_id = await self.ai_opponent.choose_piece(
                    str(self), check_achieved, feedback
                )
            piece = self.current_player.get_piece(piece_id)
            if piece:
                legal_moves = rules.get_legal_moves(
                    piece, self.current_player, self.state
                )
            else:
                if player_type == AI:
                    feedback = (
                        f"Your {piece_id} is in the graveyard. Pick a different piece."
                    )
            if len(legal_moves) == 0 and player_type == HUMAN:
                if piece:
                    print(f"{colors.MAGENTA}Piece {piece_id} has no legal moves")
                else:
                    print(f"{colors.MAGENTA}Your {piece_id} is in the graveyard")
        if player_type == HUMAN:
            self.board.highlight_piece(piece)
            self.board.highlight_moves(legal_moves, self.current_player.move_color)
            print(self.board, flush=True)
        move = None
        feedback = ""
        while move not in legal_moves:
            if player_type == HUMAN:
                chess_notation_destination = input(
                    f"{self.current_player.get_color()}Select square: {colors.BLUE}{colors.BLACK_BG} "
                )
            else:
                chess_notation_destination = await self.ai_opponent.choose_destination(
                    str(self), piece_id, legal_moves, feedback
                )
            move = tuple(map_coordinates(chess_notation_destination))
            if move not in legal_moves:
                if player_type == HUMAN:
                    print(f"{colors.MAGENTA}ILLEGAL MOVE ERROR")
                else:
                    feedback = f"Your last destination was illegal. You cannot move your {piece_id} to square {chess_notation_destination}"
        if player_type == AI:
            self.board.highlight_piece(piece)
            self.board.highlight_moves(legal_moves, self.current_player.move_color)
            print(self.board, flush=True)
            sleep(2)

        return piece_id, chess_notation_destination

    def is_complete(self):
        other_player = (
            self.player_one
            if self.current_player is self.player_two
            else self.player_two
        )
        return rules.checkmate_achieved(self.current_player, other_player, self.state)

    async def execute_move(self):
        print(self.board, flush=True)
        ai_making_move = (
            self.mode == HUMAN_VS_AI and self.current_player == self.player_two
        )

        q_castling_possible = rules.queen_side_castling_possible(
            self.current_player, self.board
        )
        k_castling_possible = rules.king_side_castling_possible(
            self.current_player, self.board
        )
        executed_castling = False

        enemy = (
            self.player_one
            if self.current_player is self.player_two
            else self.player_two
        )

        #check_achieved = rules.check_achieved(enemy, self.current_player, self.state)

        if not ai_making_move:
            if k_castling_possible:
                response = input(
                    "KING-SIDE CASTLING POSSIBLE: Execute? " + colors.GREEN
                ).upper()
                if response == "YES":
                    executed_castling = True
                    self.current_player.castle()
                    self.__update_board()
            if not executed_castling and q_castling_possible:
                response = input(
                    "QUEEN-SIDE CASTLING POSSIBLE: Execute? " + colors.GREEN
                ).upper()
                if response == "YES":
                    executed_castling = True
                    self.current_player.castle(king_side_castling=False)
                    self.__update_board()

        if not executed_castling:
            piece_id, destination = await self.__get_move(
                self.player_in_check, ai_making_move
            )
            immediate_rear = destination[0] + str(
                int(destination[1]) + (-1) ** (self.current_player.get_number())
            )
            rear_piece = self.board.get_squares((immediate_rear,)).get_piece()
            rear_is_enemy_pawn = (
                rear_piece and
                "p" in rear_piece.get_rank()
                and rear_piece.get_color_string()
                != self.current_player.get_piece(piece_id).get_color_string()
            )
            if "p" in piece_id and rear_is_enemy_pawn:
                immediate_rear = destination[0] + str(
                    int(destination[1]) + (-1) ** (self.current_player.get_number())
                )
                enemy_piece = self.board.get_squares((immediate_rear,)).get_piece()
                if enemy_piece and enemy_piece.get_just_performed_double_jump():
                    enemy.remove_piece(enemy_piece.get_id())
            else:
                enemy_piece = self.board.get_squares((destination,)).get_piece()
                if enemy_piece:
                    enemy.remove_piece(enemy_piece.get_id())
            self.current_player.move_piece(piece_id, destination)
            self.__update_board(enemy)
