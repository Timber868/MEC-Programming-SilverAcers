import numpy as np
import requests
import base64
import random
from piece import Piece
from receive import parse_game_data

class GerrymanderingGame:
    def __init__(self):
        self.board = None
        self.pieces = []
        self.color = None
        self.server_url = "http://127.0.0.1:5000"
        self.scores = {"player": 89, "agent1": 89, "agent2": 89, "agent3": 89}
        self.players = ["player", "agent1", "agent2", "agent3"]
        self.current_turn = 0

    def start_game(self):
        """
        Sends a request to start the game and initializes the board, pieces, and player color.
        """
        response = requests.post(f"{self.server_url}/start_game")
        if response.status_code == 200:
            data = response.json()
            self.initialize_board(data)
        else:
            raise Exception("Failed to start game")

    def initialize_board(self, data):
        """
        Initializes the board and player data from the server response.
        :param data: The JSON response from the server.
        """
        # Parse game data using the helper function from receive.py
        parsed_data = parse_game_data(data)
        
        # Initialize the board
        self.board = np.zeros((20, 20), dtype=int)

        # Store the player's color and pieces
        self.color = parsed_data['color']
        self.pieces = [Piece(piece_data) for piece_data in parsed_data['pieces']]

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

    def update_board(self, x, y, piece, orientation, player):
        """
        Updates the board with the given piece at the specified coordinates and orientation.
        :param x: x-coordinate of the top-left position of the piece.
        :param y: y-coordinate of the top-left position of the piece.
        :param piece: The shape of the piece as a 2D list.
        :param orientation: The orientation of the piece ("UP", "DOWN", "LEFT", "RIGHT").
        :param player: The player placing the piece.
        """
        # Rotate the piece based on the orientation
        rotated_piece = self.rotate_piece(piece.shape, orientation)
        
        # Check if the piece can be placed on the board without going out of bounds
        for i in range(len(rotated_piece)):
            for j in range(len(rotated_piece[i])):
                if rotated_piece[i][j] == 1:
                    if (x + i >= len(self.board) or y + j >= len(self.board[0]) or 
                            self.board[x + i][y + j] != 0):
                        raise ValueError("Invalid move: Piece cannot be placed at the specified location.")

        # Check if the piece placement touches at least one corner of another piece of the same color
        if not self.is_valid_corner_placement(x, y, rotated_piece):
            raise ValueError("Invalid move: Piece must touch at least one corner of another piece of the same color and cannot touch sides of the same color.")
        
        # Place the piece on the board
        for i in range(len(rotated_piece)):
            for j in range(len(rotated_piece[i])):
                if rotated_piece[i][j] == 1:
                    self.board[x + i][y + j] = 1
                    self.scores[player] -= 1

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

    def display_board(self):
        """
        Prints the board matrix to the console.
        """
        print("Current Board State:")
        for row in self.board:
            print(" ".join(map(str, row)))

    def send_move(self, x, y, orientation, piece_id):
        """
        Send move data to the server.
        :param x: x-coordinate of the move.
        :param y: y-coordinate of the move.
        :param orientation: Orientation of the piece.
        :param piece_id: ID of the piece to be placed.
        """
        # Assuming the function to send the move is written by a friend
        response = requests.post(f"{self.server_url}/send_move", json={
            "x": x,
            "y": y,
            "orientation": orientation,
            "piece_id": piece_id
        })
        if response.status_code == 200:
            move_response = response.json()
            # Update the board with the new move
            piece = next(p for p in self.pieces if p.id == piece_id)
            self.update_board(x, y, piece, orientation, "player")
            return move_response
        else:
            raise Exception("Failed to send move")

    def end_game(self):
        """
        Send a request to end the game.
        """
        response = requests.post(f"{self.server_url}/end_game")
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception("Failed to end game")

    def agent_move(self, agent_name):
        """
        Simulate a move for an intelligent agent.
        :param agent_name: The name of the agent making the move.
        """
        # Placeholder logic: Randomly pick a piece and a position
        available_pieces = [piece for piece in self.pieces if piece.count > 0]
        if not available_pieces:
            return

        piece = random.choice(available_pieces)
        orientation = random.choice(["UP", "DOWN", "LEFT", "RIGHT"])
        x = random.randint(0, 19)
        y = random.randint(0, 19)

        try:
            self.update_board(x, y, piece, orientation, agent_name)
            piece.count -= 1
            print(f"{agent_name} placed piece {piece.id} at ({x}, {y}) with orientation {orientation}")
        except ValueError:
            print(f"{agent_name} could not place piece {piece.id} at ({x}, {y})")

    def play_game(self):
        """
        Game loop logic to interact with the server and make moves.
        """
        # Initialize game settings
        self.start_game()
        self.display_board()

        # Main game loop
        while True:
            current_player = self.players[self.current_turn]

            if current_player == "player":
                # Player's turn (for now, we hardcode a move for testing purposes)
                try:
                    move_response = self.send_move(0, 0, "UP", 7)
                    print(f"Move response: {move_response}")
                    self.display_board()
                except Exception as e:
                    print(e)
            else:
                # Agent's turn
                self.agent_move(current_player)

            # Check if all players are unable to move (game over condition)
            if all(self.scores[player] <= 0 for player in self.players):
                print("Game over: No more valid moves.")
                break

            # Move to the next player
            self.current_turn = (self.current_turn + 1) % len(self.players)

        # End game
        self.end_game()
        print("Final Scores:")
        for player, score in self.scores.items():
            print(f"{player}: {score}")

if __name__ == "__main__":
    game = GerrymanderingGame()
    game.play_game()
