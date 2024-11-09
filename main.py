#This will be our main file for the board game
import request_sender as request
import receive
import piece


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
    board = receive.interpretBoard(board_data)

    #Create the pieces we can use
    pieces = piece.Piece.all_pieces

    game_ongoing = True
    while game_ongoing:
        #Get the piece we want to use
        piece_to_use = pieces[0]

        try:
            #Send the move
            statusCode, data = request.send_move(0, 0, 0, piece_to_use.piece_id)
        except Exception as e:
            request.end_game()
        

        #If the status code is not 200, then there was an error sending the move
        if statusCode != 200:
            print("Error sending move")
            request.end_game()
            return
        
    request.end_game()

    # while game_ongoing:

if __name__ == "__main__":
   main()