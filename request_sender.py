import requests
#file to hold the request sender function

# Assuming Piece is defined in a module named piece_module
from piece import Piece

baseURL = "http://localhost:5001"

def start_game():
    #send a basic post request to the server to start the game
    urlToStartGame = baseURL + "/start_game"
    response = requests.post(urlToStartGame)

    if response.status_code == 200:
        print("Game started successfully")
    else:
        print("Error starting game")

    return response.status_code, response.json()

def send_move(x, y, orientation, piece_id):
    #send a post request to the server to make a move
    urlToMove = baseURL + "/send_move"

    data = {
        "x": x,
        "y": y,
        "orientation": orientation,
        "piece_id": piece_id
    }

    piece = Piece.getPiece(piece_id)
    if piece is None:
        print("Piece not found")
        return 404, {"message": "Piece not found"}
    
    if piece.count == 0:
        print("Piece out of stock")
        return 400, {"message": "Piece out of stock"}

    response = requests.post(urlToMove, json=data)

    if response.status_code == 200:
        print("Move sent successfully")
        piece.count -= 1
        
    else:
        print("Error sending move")

    return response.status_code, response.json()

def end_game():
    #send a post request to the server to end the game
    urlToEndGame = baseURL + "/end_game"
    response = requests.post(urlToEndGame)

    if response.status_code == 200:
        print("Game ended successfully")
    else:
        print("Error ending game")

    return response.status_code