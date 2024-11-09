import numpy as np
from piece import Piece
from receive import *
from request_sender import start_game, send_move, end_game

def is_valid_corner_placement(self, x, y, piece):
    """
    Checks if the piece placement touches at least one corner of another piece of the same color.
    :param x: x-coordinate of the top-left position of the piece.
    :param y: y-coordinate of the top-left position of the piece.
    :param piece: The shape of the piece as a 2D list.
    :return: True if the piece touches at least one corner of the same color and does not touch sides of the same color, False otherwise.
    """
    corner_directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]  # Possible corner directions
    side_directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Possible side directions
    touches_corner = False

    for i in range(len(piece)):
        for j in range(len(piece[i])):
            if piece[i][j] == 1:
                # Check if the piece touches any sides of the same color
                for dx, dy in side_directions:
                    new_x, new_y = x + i + dx, y + j + dy
                    if 0 <= new_x < len(self.board) and 0 <= new_y < len(self.board[0]):
                        if self.board[new_x][new_y] == 1:
                            return False  # Invalid if touching a side of the same color
                # Check if the piece touches at least one corner of the same color
                for dx, dy in corner_directions:
                    new_x, new_y = x + i + dx, y + j + dy
                    if 0 <= new_x < len(self.board) and 0 <= new_y < len(self.board[0]):
                        if self.board[new_x][new_y] == 1:
                            touches_corner = True
    return touches_corner
    
def rotate_piece(self, piece, orientation):
    """
    Rotates the piece based on the given orientation.
    :param piece: The shape of the piece as a 2D list.
    :param orientation: The orientation of the piece ("UP", "DOWN", "LEFT", "RIGHT").
    :return: The rotated piece as a 2D list.
    """
    piece_array = np.array(piece)
    if orientation == "UP":
        return piece_array.tolist()
    elif orientation == "RIGHT":
        return np.rot90(piece_array, -1).tolist()
    elif orientation == "DOWN":
        return np.rot90(piece_array, 2).tolist()
    elif orientation == "LEFT":
        return np.rot90(piece_array, 1).tolist()
    else:
        raise ValueError("Invalid orientation")


