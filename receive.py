import requests
import piece
import request_sender
import base64
from PIL import Image
import io

def initializeGame(data):
    color = data.get("color", str)
    board_id = data.get("board", str)
    pieces = data.get("pieces", [])
    for pieceDict in pieces:
        piece.Piece(pieceDict["id"], pieceDict["count"], pieceDict["shape"])

    return color, board_id


def interpretBoard(board_id):
    image_data = base64.b64decode(board_id)
    with open("decoded_board.png", "wb") as file:
        file.write(image_data)
    
    # Open the image from the decoded bytes
    image = Image.open(io.BytesIO(image_data))
    
    # Resize to 20x20 if necessary
    image = image.resize((20, 20))
    
    # Initialize a 20x20 matrix
    color_matrix = []

    # Define target colors with their integer codes
    color_mapping = {
        (0, 0, 0): 0,         # Black
        (255, 0, 0): 1,       # Red
        (0, 255, 0): 2,       # Green
        (0, 0, 255): 3,       # Blue
        (255, 255, 0): 4      # Yellow
    }

    # Define a color tolerance
    tolerance = 100

    # Helper function to check if colors are within a tolerance
    def is_close(color1, color2, tolerance):
        return all(abs(c1 - c2) <= tolerance for c1, c2 in zip(color1, color2))

    # Process each pixel in the 20x20 image
    for y in range(20):
        row = []
        for x in range(20):
            # Get the RGB color of the pixel
            pixel_color = image.getpixel((x, y))

            # Find the closest matching color within the tolerance
            color_code = -1  # Default for unrecognized color
            for target_color, code in color_mapping.items():
                if is_close(pixel_color, target_color, tolerance):
                    color_code = code
                    break
            
            row.append(color_code)
        color_matrix.append(row)
    return color_matrix


if __name__ == "__main__":
    requests.post("http://localhost:5001/end_game")
    errorCode, data = request_sender.start_game()
    initializeGame(data)

    color, board_id = initializeGame(data)

    matrix = interpretBoard(board_id)
    for row in matrix:
        print(row)
