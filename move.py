import piece
import corner
class Move:

    def __init__(self, piece, position, orientation, board):

        self.piece = piece
        self.position = position
        self.orientation = orientation
        self.score = self.move_score(board)

    def to_dict(self):
       #dictionnary representation
        return {
            "piece_id": self.piece.id,
            "x": self.position[0],
            "y": self.position[1],
            "orientation": self.orientation
        }
    

    def updateBoard(self, board):
        # Extract move details, assuming 'move' is an instance with attributes or methods to access x, y, piece, and color
        start_x = self.x
        start_y = self.y
        piece_shape = self.piece.shape  # Accessing the shape of the piece (2D list)
        color_code = self.color

        # Create a copy of the board to avoid modifying the original
        newBoard = [row[:] for row in board]

        # Get the dimensions of the piece
        piece_height = len(piece_shape)
        piece_width = len(piece_shape[0]) if piece_height > 0 else 0

        # Place the piece on the new board
        for i in range(piece_height):
            for j in range(piece_width):
                if piece_shape[i][j] == 1:  # Only place cells where the piece has a 1
                    # Calculate the actual board position
                    board_x = start_x + i
                    board_y = start_y + j

                    # Ensure we are within the bounds of the board
                    if 0 <= board_x < len(newBoard) and 0 <= board_y < len(newBoard[0]):
                        newBoard[board_x][board_y] = color_code  # Set the color code on the board

        return newBoard


    def move_score(self, board):
        score = 0
        for i in range(len(self.piece.shape)):
            for j in range(len(self.piece.shape[i])):
                if self.piece.shape[i][j]!=0:
                    score += 1
        return score





                






