def face_generation_prompt(mood="ANGRY", no_detail=True):
    string = (
        "I NEED to test how the tool works with extremely simple prompts. DO NOT add any detail, just use it AS-IS: "
        if no_detail
        else ""
    )
    string += (
        """
        Lots of bright colorful sparkles on a pitch black background.
        """
        if mood == "ANGRY"
        else """
        The head of a smirking humanoid robot with green eyes and a blue face on a plain black background. His head is shaped like a skeleton skull.
        There are 7 green pentagrams around his head and he's holding a bright red chess piece.
    """
    )
    return string


def piece_selection_prompt(king_in_check, feedback):
    string = """
         We are playing a game of chess. You control the black pieces and I control the white pieces.
         In the next message, I will pass the state of the game to you as a two dimensional array.
         Each element in the 2D array is a dictionary that corresponds to a square on the chessboard.
         Each dictionary has two keys: 'square' and 'piece'. For example, when the game starts,
         game_state[0][0] = {'square': 'a8', 'piece': 'black rook1'}. If a square is empty,
         then it's 'piece' is None (a python keyword). For example, when the game starts,
         game_state[2][0] = {'square': 'a6', 'piece': None}. Your task is specify the
         best possible move for black, based on the current game state. Choose a 'piece'
         and a 'destination', but for now, only give me the name of the piece you chose.
         Do not include the word 'black' in your response, since I already know you are black.
         Your response should be a single word: the name of the piece you want to move along
         with its number.
    """
    string += (
        "Your king is in check, so you must move your king." if king_in_check else ""
    )
    string += feedback
    return string


def destination_selection_prompt(piece, possible_destinations, feedback):
    return "".join(
        [
            f"We are playing a game of chess. You are black; I am white. You have decided to move ",
            f"your {piece}. The possible squares this piece can move to are {possible_destinations}. ",
            f"In the next 'user' message, I will give you the game state. Select a square from the list ",
            f"of possible squares I have provided to you. The only thing in your response should be a ",
            f"letter and a number representing one of the possible squares I have given you.",
            f"Whenever possible, you should capture my pieces.",
            f"Refer to the game state to see if capture is possible.",
            f"{feedback}",
        ]
    )
