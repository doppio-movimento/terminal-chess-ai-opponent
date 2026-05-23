def map_coordinates(destination):
    phys_coords = (int(destination[1]), ord(destination[0].capitalize()) - 64)
    computer_row = 8 - phys_coords[0]
    computer_col = phys_coords[1] - 1
    return (computer_row, computer_col)


def get_chess_coordinates(computer_coordinates):
    physical_row = 8 - computer_coordinates[0]
    physical_column = computer_coordinates[1] + 1
    chess_notation = f"{chr(physical_column + 64).lower()}{physical_row}"
    return chess_notation
