import numpy as np
from piece import Piece
from receive import parse_game_data
from request_sender import start_game, send_move, end_game

class GerrymanderingGame:
    def __init__(self):
        self.board = None
        self.pieces = []
        self.color = None
        self.scores = {"player": 89, "agent1": 89, "agent2": 89, "agent3": 89}
        self.players = ["player", "agent1", "agent2", "agent3"]
        self.current_turn = 0

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

    def play_game(self):
        """
        Game loop logic to interact with the server and make moves.
        """
        # Initialize game settings
        status_code, data = start_game()
        if status_code == 200:
            self.initialize_board(data)
        else:
            raise Exception("Failed to start game")
        
        self.display_board()

        # Main game loop
        while True:
            current_player = self.players[self.current_turn]

            if current_player == "player":
                # Player's turn (for now, we hardcode a move for testing purposes)
                try:
                    status_code, move_response = send_move(0, 0, "UP", 7)
                    if status_code == 200:
                        print(f"Move response: {move_response}")
                        self.display_board()
                    else:
                        print("Failed to send move")
                except Exception as e:
                    print(e)
            else:
                # Skip agent moves since the server handles them
                print(f"{current_player}'s move is handled by the server.")

            # Check if all players are unable to move (game over condition)
            if all(self.scores[player] <= 0 for player in self.players):
                print("Game over: No more valid moves.")
                break

            # Move to the next player
            self.current_turn = (self.current_turn + 1) % len(self.players)

        # End game
        end_game()
        print("Final Scores:")
        for player, score in self.scores.items():
            print(f"{player}: {score}")

if __name__ == "__main__":
    game = GerrymanderingGame()
    game.play_game()
