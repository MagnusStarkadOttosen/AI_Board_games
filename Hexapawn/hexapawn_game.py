


class hexapawn_game:
    def __init__(self):
        self.board = [
            [2,2,2],
            [0,1,0],
            [1,1,1]
        ]
        self.current_player = 1

    #Start game
    def start_game(self):

        winner = -1

        while(1):
            print(self.current_player)
            self.print_board()

            #Check for win
            winner = self.win_condition()
            if winner != -1:
                break
            #Swap player
            if self.current_player == 1:
                self.current_player = 2
            else:
                self.current_player = 1
        
        print(f"Winner is {winner}")


    #Move
    def move(self):


        return
    
    #Print board
    def print_board(self):
        for row in self.board:
            print(row)

    #Check for win
    def win_condition(self):
        #If there is no more player 1, player 2 wins
        if not any(1 in row for row in self.board):
            return 2
        #If there is no more player 2, player 1 wins
        if not any(2 in row for row in self.board):
            return 1
        
        #If player 1 reach the other side they win
        if 1 in self.board[0]:
            return 1
        #If player 2 reach the other side they win
        if 2 in self.board[2]:
            return 2
        
        #Check if there are valid moves left
        for row in self.board:
            for e in row:
                print(e)

        #If no one has won return -1
        return -1
        
        
    #Return board
    def return_board(self):
        return self.board

    #Validate moves
    def valid_moves(self, pawn):
        row, col = pawn
        rows = 3
        cols = 3
        

        if self.board[row][col] == 1:
            # Get diagonal up-left (row-1, col-1)
            diag_up_left = self.board[row - 1][col - 1] if row - 1 < rows and col - 1 >= 0 else None

            # Get directly up (row-1, col)
            up = self.board[row - 1][col] if row - 1 < rows else None

            # Get diagonal up-right (row-1, col+1)
            diag_up_right = self.board[row - 1][col + 1] if row - 1 < rows and col + 1 < cols else None

            return {
                "Diagonal UP-Left": diag_up_left,
                "Directly Up": up,
                "Diagonal Up-Right": diag_up_right
            }
        else:
            # Get diagonal down-left (row+1, col-1)
            diag_down_left = self.board[row + 1][col - 1] if row + 1 < rows and col - 1 >= 0 else None

            # Get directly down (row+1, col)
            down = self.board[row + 1][col] if row + 1 < rows else None

            # Get diagonal down-right (row+1, col+1)
            diag_down_right = self.board[row + 1][col + 1] if row + 1 < rows and col + 1 < cols else None

            return {
                "Diagonal Down-Left": diag_down_left,
                "Directly Down": down,
                "Diagonal Down-Right": diag_down_right
            }

    
    def get_player_pawns(self, player):
        pawns = []
        for row_index, row in enumerate(self.board):
            for col_index, value in enumerate(row):
                if value == player:
                    pawns.append((row_index,col_index))
        return pawns




start_game = hexapawn_game()
# start_game.print_board()

# temp = start_game.return_board()
# print(temp[0])

# start_game.win_condition()
pawns = start_game.get_player_pawns(2)
print(pawns)

print(start_game.valid_moves((0,0)))
print(start_game.valid_moves((1,1)))
print(start_game.valid_moves((2,2)))