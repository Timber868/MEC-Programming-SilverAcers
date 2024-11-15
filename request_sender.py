import requests
import piece
#file to hold the request sender function

baseURL = "http://localhost:5000"

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

    pieceToCheck = piece.Piece.getPiece(piece_id)
    if(pieceToCheck == None):
        print("Piece not found")
        return 404, {"message": "Piece not found"}
    
    if(pieceToCheck.count == 0):
        print("Piece is out of stock")
        return 400, {"message": "Piece is out of stock"}

    response = requests.post(urlToMove, json=data)

    if response.status_code == 200:
        print("Move sent successfully")
        pieceToCheck.count -= 1
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