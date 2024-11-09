import piece
class Move:

    def __init__(self, piece, position, orientation, board):

        self.piece = piece
        self.position = position
        self.orientation = orientation
        self.score = self.move_score(board)

    def __repr__(self):
       # string representation
        return (f"Move(piece_id={self.piece.id}, "
                f"position={self.position}, "
                f"orientation='{self.orientation}')")

    def to_dict(self):
       #dictionnary representation
        return {
            "piece_id": self.piece.id,
            "x": self.position[0],
            "y": self.position[1],
            "orientation": self.orientation
        }
    

def updateBoard(board, move):
    # Extract move details, assuming 'move' is an instance with attributes or methods to access x, y, piece, and color
    start_x = move.x
    start_y = move.y
    piece_shape = move.piece.shape  # Accessing the shape of the piece (2D list)
    color_code = move.color

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
        piece_score= self.piece.points

        piece_position= self.piece.position
        difference_x= abs(10-piece_position[0])
        difference_y= abs(10-piece_position[1])
        difference_center=difference_x + difference_y

        piece_shape= self.piece.shape
        for i in range(len(piece_shape)):
            return
        return ((piece_score/5)*0.7+(difference_center/10)*0.3)*100





                






