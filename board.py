import numpy as np
from piece import Piece
from move import Move
from receive import *
from request_sender import start_game, send_move, end_game

def is_valid_corner_placement(board, x, y, piece, orientation):
    """
    Checks if the piece placement touches at least one corner of another piece of the same color
    and does not touch any side of the same color, considering the orientation of the piece.

    :param board: The game board as a 2D list.
    :param x: x-coordinate of the top-left position of the piece.
    :param y: y-coordinate of the top-left position of the piece.
    :param piece: The shape of the piece as a 2D list where colored spaces are marked as 1.
    :param orientation: The orientation of the piece ('UP', 'DOWN', 'LEFT', 'RIGHT').
    :return: True if the placement is valid, False otherwise.
    """
    # Define corner and side directions
    corner_directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
    side_directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    # Rotate the piece based on its orientation
    rotated_piece = rotate_piece(piece, orientation)

    # Check the placement validity
    touches_corner = False
    for i in range(len(rotated_piece)):
        for j in range(len(rotated_piece[i])):
            if rotated_piece[i][j] == 1:  # Only consider colored spaces
                # Check for invalid side contact
                for dx, dy in side_directions:
                    new_x, new_y = x + i + dx, y + j + dy
                    if 0 <= new_x < len(board) and 0 <= new_y < len(board[0]):
                        if board[new_x][new_y] == 1:
                            return False  # Invalid if touching a side of the same color

                # Check for valid corner contact
                for dx, dy in corner_directions:
                    new_x, new_y = x + i + dx, y + j + dy
                    if 0 <= new_x < len(board) and 0 <= new_y < len(board[0]):
                        if board[new_x][new_y] == 1:
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


def generate_moves (pieces : list[piece],board ):
    """
    Generates all the possible moves our player can do
    :param positions: All the valid positions
    :param orientation: The orientation of the piece ("UP", "DOWN", "LEFT", "RIGHT").
    :return: The rotated piece as a 2D list.
    """
    moves = []
    positions = get_positions()
    orientations = ["UP", "RIGHT", "DOWN", "LEFT"]
    for piece in pieces:
        for orientation in orientations:
            for position in positions:
                if is_valid_corner_placement(board, position[0], position[1], piece, orientation):
                    moves.append( Move(piece, position, orientation, board))
    return moves
def get_positions ():
    positions = list [tuple[int]]
    for i in range(20):
        for j in range(20):
            positions.append((i,j))
    return positions

def return_best_move(moves):

    for move in moves:

