import numpy as np
from piece import Piece
from receive import *
from move import Move
import random
from request_sender import start_game, send_move, end_game
from move import Move

def is_valid_corner_placement(board, x, y, piece, orientation):
    # Define corner and side directions
    corner_directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
    side_directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    # Rotate the piece based on its orientation
    rotated_piece = rotate_piece(piece, orientation)

    # Check the placement validity
    touches_corner = False
    for i in range(len(rotated_piece)):
        for j in range(len(rotated_piece[i])):
            board_x = x + i
            board_y = y + j

            # Boundary check
            if not (0 <= board_x < len(board) and 0 <= board_y < len(board[0])):
                # Piece extends beyond the board
                return False

            if rotated_piece[i][j] == 1 and board[board_x][board_y] == 0:  # Only consider colored spaces
                # Check for invalid side contact
                for dx, dy in side_directions:
                    new_x, new_y = board_x + dx, board_y + dy
                    if 0 <= new_x < len(board) and 0 <= new_y < len(board[0]):
                        if board[new_x][new_y] == 1:
                            return False  # Invalid if touching a side of the same color

                # Check for valid corner contact
                for dx, dy in corner_directions:
                    new_x, new_y = board_x + dx, board_y + dy
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


def rotate_piece(piece_shape, orientation):
    """
    Rotates the piece based on the given orientation.
    :param piece: The shape of the piece as a 2D list.
    :param orientation: The orientation of the piece ("UP", "DOWN", "LEFT", "RIGHT").
    :return: The rotated piece as a 2D list.
    """
    piece_array = np.array(piece_shape)
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


def generate_moves(board, pieces):
    moves = []
    positions = get_positions()
    orientations = ["UP", "RIGHT", "DOWN", "LEFT"]
    for piece in pieces:
        for orientation in orientations:
            for position in positions:
                if is_valid_corner_placement(board, position[0], position[1], piece.shape, orientation):
                    moves.append(Move(piece, position, orientation, board))
    return moves

def get_positions ():
    positions = []
    for i in range(20):
        for j in range(20):
            positions.append((i,j))
    return positions

def return_best_move(moves):
    best_score = 0
    best_moves = []
    best_move : Move
    for move in moves:
        if move.score > best_score:
            best_move = move
            best_score = move.score
    for move in moves:
        if move.score == best_score:
            best_moves.append(move)
    if best_moves:
        selected_move = random.choice(best_moves)
        print(f"Selected best move: {selected_move}")  # Debug
        return selected_move
    else:
        print("No moves match the best score.")
        return None  # Shouldn't occur if moves is not empty









