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





                






