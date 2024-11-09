import piece
class Move:
    moves = []
    def __init__(self, piece, position, orientation):

        self.piece = piece
        self.position = position
        self.orientation = orientation

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
    def generate_moves (matrix : list[list[int]], pieces : list[piece]):
        orientations = ["up", "right", "down", "left"]
        for piece in pieces:
            for orientation in orientations:
                






