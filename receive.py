import requests
import piece
import request_sender
import base64

def initializeGame(data):
    color = data.get("color", str)
    board_id = data.get("board", str)
    pieces = data.get("pieces", [])
    for pieceDict in pieces:
        piece.Piece(pieceDict["id"], pieceDict["count"], pieceDict["shape"])

    return color, board_id


def interpretMove():
    return


def StartingBoard(startingResponse: str):
    return startingResponse


if __name__ == "__main__":
    requests.post("http://localhost:5001/end_game")
    errorCode, data = request_sender.start_game()

    color, board_id = initializeGame(data)

    print(color)
    print(board_id)
    piece.Piece.printPieces()