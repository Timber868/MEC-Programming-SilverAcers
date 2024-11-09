import numpy as np
from piece import Piece
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

def isValidMove(matrix, piece, x, y, color):
    rows, cols = 20, 20  # The board dimensions
    piece_shape = piece.shape  # Get the shape of the piece as a 2D list
    piece_height = len(piece_shape)
    piece_width = len(piece_shape[0]) if piece_height > 0 else 0

    # Helper function to check if coordinates are within bounds
    def in_bounds(x, y):
        return 0 <= x < rows and 0 <= y < cols

    # Validate if the piece is within bounds
    if x + piece_height > rows or y + piece_width > cols:
        return False

    # Track if the piece is touching a corner of the same color
    is_touching_corner = False

    # Loop through the shape of the piece to check placement
    for i in range(piece_height):
        for j in range(piece_width):
            if piece_shape[i][j] == 1:  # If there's a square in the piece here
                # Check if the position in the board is empty
                if matrix[x + i][y + j] != 0:
                    return False  # Cannot place piece on occupied space

                # Check for corner adjacency to the same color
                adjacent_corners = [
                    (x + i - 1, y + j - 1), (x + i - 1, y + j + 1),
                    (x + i + 1, y + j - 1), (x + i + 1, y + j + 1)
                ]
                touching_same_color_corner = False
                for adj_x, adj_y in adjacent_corners:
                    if in_bounds(adj_x, adj_y) and matrix[adj_x][adj_y] == color:
                        touching_same_color_corner = True
                        break

                # If no touching corner of the same color, check edges
                if not touching_same_color_corner:
                    adjacent_edges = [
                        (x + i - 1, y + j), (x + i + 1, y + j),
                        (x + i, y + j - 1), (x + i, y + j + 1)
                    ]
                    for adj_x, adj_y in adjacent_edges:
                        if in_bounds(adj_x, adj_y) and matrix[adj_x][adj_y] == color:
                            return False  # Touching edge with the same color is invalid

                # Track if at least one corner is touching the same color
                if touching_same_color_corner:
                    is_touching_corner = True

    # The move is valid if at least one square of the piece touches a corner of the same color
    return is_touching_corner


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


def generate_moves (positions : list[tuple[int]], pieces : list[piece], ):
    moves = []
    orientations = ["UP", "RIGHT", "DOWN", "LEFT"]
    for piece in pieces:
        for orientation in orientations:
            for position in positions:
                if is_valid_corner_placement(position[0],position[1],piece):

        #check if position is valid
        # if valid put into list moves
    return moves