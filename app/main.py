from asyncio import run
from os import get_terminal_size, getenv
from sys import argv

from colorama import init
from dotenv import load_dotenv

import graphics.colors as colors
from artificial_intelligence.ai_chess_opponents import LLMOpponent
from graphics.settings import Settings
from logic.game import Game
from logic.player import Player


async def async_main():
    if len(argv) < 2:
        print(
            "".join(
                (
                    f"{colors.RED}Error! ",
                    f"{colors.YELLOW}Usage: ",
                    f"{colors.WHITE}pipenv run python main.py mode, ",
                    f"where {colors.MAGENTA}mode = tmode {colors.WHITE}or ",
                    f"{colors.CYAN}mode = aimode{colors.WHITE}",
                )
            )
        )
        return
    init(autoreset=True)
    data_file = open("training_data/legal_moves_1.json", "a")
    terminal_dimensions = get_terminal_size()
    settings = Settings(terminal_dimensions)
    # settings.request_settings()
    white = Player(colors.BRIGHT_WHITE, colors.CYAN_BG, first=True)
    black = Player(colors.BRIGHT_BLACK, colors.BLUE_BG)
    if argv[1] == "tmode":
        chess_game = Game(white, black, data_file)
        ai_opponent = None
    else:
        load_dotenv()
        ai_opponent = LLMOpponent(getenv("OPENAI_API_KEY"))
        chess_game = Game(white, black, data_file, ai_opponent=ai_opponent, mode=1)

    while not chess_game.is_complete():
        await chess_game.execute_move()
    data_file.close()


if __name__ == "__main__":
    run(async_main())
