class Piece:
	all_pieces = []

	def __init__(self, piece_id: int, count: int, shape: list[list[int]]):
		# Initialize the attributes
		self.piece_id = piece_id
		self.count = count
		self.shape = shape
		if self.piece_id >=9:
			self.points = 5
		elif self.piece_id >=4:
			self.points = 4
		elif self.piece_id >= 2:
			self.points = 3
		elif self.piece_id ==1:
			self.points = 2
		else: self.points = 1
		Piece.all_pieces.append(self)

	def __str__(self):
		# Custom string representation of the piece
		return f"Piece(id={self.piece_id}, count={self.count}, shape={self.shape})"

	def __repr__(self):
		# Representation of the piece for debugging
		return self.__str__()

	def create_piece_from_string(data_str: str):
		# Convert the string to a dictionary
		data = ast.literal_eval(data_str)

		# Use the dictionary to initialize a Piece object
		piece = Piece(
		    piece_id=data['id'],
		    count=data['count'],
		    shape=data['shape']
		)

		return piece

	def printPieces():
		for piece in Piece.all_pieces:
			print(piece)

	def getPiece(piece_id: int):
		# Find the piece with the given piece_id
		for piece in Piece.all_pieces:
			if piece.piece_id == piece_id:
				return piece
