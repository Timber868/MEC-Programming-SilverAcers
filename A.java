class Move:
    def __init__(self, piece, position, orientation):
        self.piece = piece
        self.position = position
        self.orientation = orientation

    def __repr__(self):

        return (f"Move(piece_id={self.piece.id}, "
                f"position={self.position}, "
                f"orientation='{self.orientation}')")

    def to_dict(self):

        return {
            "piece_id": self.piece.id,
            "x": self.position[0],
            "y": self.position[1],
            "orientation": self.orientation
        }