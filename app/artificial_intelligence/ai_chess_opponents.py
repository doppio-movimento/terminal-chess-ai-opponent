from os import get_terminal_size
from sys import path
from time import sleep
from urllib.request import urlretrieve

from openai import OpenAI

from graphics.text_animation import print_grid, type_matrix
from transformations.mapping import get_chess_coordinates

from .prompts import destination_selection_prompt, piece_selection_prompt


class LLMOpponent:
    def __init__(self, api_key, model="gpt-4o"):
        self.api_key = api_key
        self.model = model
        self.client = OpenAI(api_key=api_key)
        self.total_cost = 0

    async def choose_piece(self, game_state, king_in_check, feedback):
        completion = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": piece_selection_prompt(king_in_check, feedback),
                },
                {"role": "user", "content": game_state},
            ],
        )

        return completion.choices[0].message.content

    async def choose_destination(self, game_state, piece, legal_destinations, feedback):
        legal_destinations_string = ", ".join(
            list(map(lambda c: get_chess_coordinates(c), legal_destinations))
        )
        completion = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": destination_selection_prompt(
                        piece, legal_destinations_string, feedback
                    ),
                },
                {"role": "user", "content": game_state},
            ],
        )
        return completion.choices[0].message.content
