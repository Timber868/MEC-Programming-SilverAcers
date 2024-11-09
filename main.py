#This will be our main file for the board game
import request_sender as request
import receive
import piece
import board as Board
import os

server_host = os.getenv("SERVER_HOST", "localhost")
server_port = os.getenv("SERVER_PORT", "5000")
urlToStartGame = f"http://{server_host}:{server_port}/start_game"


def getMaxPiece(pieces):
    maxPiece = pieces[0]
    for piece in pieces:
        if piece.points > maxPiece.points:
            maxPiece = piece
    return maxPiece

def main():
    #Start the game if we get an exception the game was not previously well terminated
    try:
        statusCode, data = request.start_game()
    except Exception as e:
        request.end_game()
        statusCode, data = request.start_game()

    #If the status code is not 200, then there was an error starting the game
    if statusCode != 200:
        print("Error starting game")
        return
    
    #Get the current board data and our color
    color, board_data = receive.initializeGame(data)

    #Set up the starting Matrix
    currentBoard = receive.interpretBoard(board_data)

    #Create the pieces we can use
    pieces = piece.Piece.all_pieces

    #Our first two moves are fixed
    try:
            #Send the move
            statusCode, data = request.send_move(0, 10, "UP", 9)
            print(statusCode)

    except Exception as e:
        print("Error sending move", e)
        request.end_game()
        return

    #Update our board and score
    score, currentBoard = receive.interpretMove(data)
    
    #Our first two moves are fixed
    try:
            #Send the move
            statusCode, data = request.send_move(5, 11, "RIGHT", 6)
            print(statusCode)
    except Exception as e:
        print("Error sending move", e)
        print(score)
        request.end_game()
        return
    
    #Update our board and score
    score, currentBoard = receive.interpretMove(data)

    boardPlaceholder = currentBoard
    piecesPlaceholder = pieces

    i = 0
    game_ongoing = True
    while game_ongoing:
        i += 1
        if(i==1):
            currentBoard = boardPlaceholder
            pieces = piecesPlaceholder
        #Get the piece we want to use

        moves = Board.generate_moves(currentBoard, pieces)
        best_move = Board.return_best_move(moves)
        try:
            #Send the move
            print(best_move.position[0], best_move.position[1], best_move.orientation, best_move.piece.piece_id)
            statusCode, data = request.send_move(best_move.position[0], best_move.position[1], best_move.orientation, best_move.piece.piece_id)
        except Exception as e:
            print("Error sending move", e)
            print(score)
            request.end_game()
            return
        
        #Update our board and score
        score, currentBoard = receive.interpretMove(data)
        
        #If the status code is not 200, then there was an error sending the move
        if statusCode != 200:
            print("Error sending move")
            request.end_game()
            print(score)
            return
        

    print("Total score:", score)
    # while game_ongoing:

if __name__ == "__main__":
   main()