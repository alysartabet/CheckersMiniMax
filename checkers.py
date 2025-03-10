"""
CSCI 355 Spring 2025
M01
Assignment 2: MiniMax (*SOLO*)
Author: Alysar Tabet
Professor: Susan Gass
March 8 2025
Checkers MiniMax: a strategy board game for two players, played on an 8x8 grid with 12 pieces per player. 
The objective is to capture all opponent's pieces or block them so they cannot move.
Players take turns moving their pieces diagonally forward one square at a time. 
A piece can capture an opponent's piece by jumping over it into an empty space, and capturing is mandatory if a jump is available.
If a piece reaches the last row, it is promoted to a king, which can move both forward and backward diagonally. 
The game continues until one player captures all opponent's pieces or blocks them from making any legal move, resulting in a win. 
If neither player can move, the game ends in a draw. 
"""

import math

class CheckersMinimax:
    def __init__(self):
        self.depth = self.depth_user()
    
    def depth_user(self):
        """Prompts the user to choose a depth for Minimax and explains its meaning."""
        print("\nUnderstanding Depth in Minimax:")
        print("1. Depth determines how many moves ahead the AI will look.")
        print("2. A higher depth means a smarter AI but takes longer to compute.")
        print("3. Typically, a depth of 2-4 is reasonable for Checkers at this stage of the game.")
        print("4. Going beyond depth 6 may slow down the AI significantly.")
        
        while True:
            try:
                depth = int(input("Enter Minimax search depth: "))
                if 1 <= depth <= 6:
                    return depth
                else:
                    print("Invalid choice. Please enter a depth between 1 and 6.")
            except ValueError:
                print("Invalid input. Please enter a number.")
    
    def player(self, board):
        """Determines whose turn it is based on the number of moves made."""
        x_count = sum(row.count('X') for row in board)
        o_count = sum(row.count('O') for row in board)
        return 'X' if x_count <= o_count else 'O'
    
    def termial_state(self, board): #checking validity of game state
        """Checks if the game is over (no valid moves left for either player or no pieces left)."""
        x_pieces = sum(row.count('X') for row in board)
        o_pieces = sum(row.count('O') for row in board)
        
        # If either player has no pieces left, the game is over
        if x_pieces == 0 or o_pieces == 0:
            return True
        
        # If both players have no valid moves, the game is over
        return not self.get_valid_moves(board, True) and not self.get_valid_moves(board, False)
    
    def utility(self, board):
        """Assigns a number to terminal state based on Minimax evaluation."""
        if self.termial_state(board):
            x_pieces = sum(row.count('X') for row in board)
            o_pieces = sum(row.count('O') for row in board)
            
            if x_pieces > o_pieces:
                return 1  # AI wins
            elif o_pieces > x_pieces:
                return -1  # Player wins
            else:
                return 0  # Draw
        return None  # Non-terminal states return None, so Minimax continues searching
    
    def move(self, board, move):
        """Returns a new board state after making a move."""
        new_board = [list(row) for row in board]  
        (r1, c1), (r2, c2) = move
        new_board[r2][c2] = new_board[r1][c1]
        new_board[r1][c1] = '.'  # Empty the old position
        
        # Handle captures
        if abs(r2 - r1) == 2:  # Capture happened
            mid_r, mid_c = (r1 + r2) // 2, (c1 + c2) // 2
            new_board[mid_r][mid_c] = '.'  # Remove captured piece
        
        return new_board
    
    def minimax(self, board, depth, is_maximizing): #Minimax algorithm to compute the best move sequence.
        utility_value = self.utility(board)
        
        if depth == self.depth or utility_value is not None:
            return utility_value, []  # Return utility and an empty move sequence
        
        best_move_sequence = []
        
        if is_maximizing:
            best_value = -math.inf
            for move in self.get_valid_moves(board, True):
                new_board = self.move(board, move)
                value, move_sequence = self.minimax(new_board, depth + 1, False)
                if value is not None and value > best_value:
                    best_value = value
                    best_move_sequence = [move] + move_sequence
            return (best_value if best_value != -math.inf else 0), best_move_sequence
        else:
            best_value = math.inf
            for move in self.get_valid_moves(board, False):
                new_board = self.move(board, move)
                value, move_sequence = self.minimax(new_board, depth + 1, True)
                if value is not None and value < best_value:
                    best_value = value
                    best_move_sequence = [move] + move_sequence
            return (best_value if best_value != math.inf else 0), best_move_sequence
    
    def get_valid_moves(self, board, is_maximizing):
        """Returns a list of possible moves for a player."""
        player_piece = 'X' if is_maximizing else 'O'
        opponent_piece = 'O' if is_maximizing else 'X'
        moves = []
        
        for r in range(8):
            for c in range(8):
                if board[r][c] == player_piece:
                    # Normal moves
                    if is_maximizing and r > 0:
                        if c < 7 and board[r-1][c+1] == '.':
                            moves.append(((r, c), (r-1, c+1)))
                        if c > 0 and board[r-1][c-1] == '.':
                            moves.append(((r, c), (r-1, c-1)))
                    if not is_maximizing and r < 7:
                        if c < 7 and board[r+1][c+1] == '.':
                            moves.append(((r, c), (r+1, c+1)))
                        if c > 0 and board[r+1][c-1] == '.':
                            moves.append(((r, c), (r+1, c-1)))
                    # Capture moves
                    if is_maximizing and r > 1:
                        if c < 6 and board[r-1][c+1] == opponent_piece and board[r-2][c+2] == '.':
                            moves.append(((r, c), (r-2, c+2)))
                        if c > 1 and board[r-1][c-1] == opponent_piece and board[r-2][c-2] == '.':
                            moves.append(((r, c), (r-2, c-2)))
                    if not is_maximizing and r < 6:
                        if c < 6 and board[r+1][c+1] == opponent_piece and board[r+2][c+2] == '.':
                            moves.append(((r, c), (r+2, c+2)))
                        if c > 1 and board[r+1][c-1] == opponent_piece and board[r+2][c-2] == '.':
                            moves.append(((r, c), (r+2, c-2)))
        return moves
    
    def select_predefined_board(self):
        """Allows the user to choose from eight predefined board states."""
        boards = [
            [  # Starting position
                ['O', '.', 'O', '.', 'O', '.', 'O', '.'],
                ['.', 'O', '.', 'O', '.', 'O', '.', 'O'],
                ['O', '.', 'O', '.', 'O', '.', 'O', '.'],
                ['.', '.', '.', '.', '.', '.', '.', '.'],
                ['.', '.', '.', '.', '.', '.', '.', '.'],
                ['.', 'X', '.', 'X', '.', 'X', '.', 'X'],
                ['X', '.', 'X', '.', 'X', '.', 'X', '.'],
                ['.', 'X', '.', 'X', '.', 'X', '.', 'X']
            ],
            [  # Mid-game state1
                ['O', '.', '.', '.', 'O', '.', '.', '.'],
                ['.', 'O', '.', '.', '.', 'O', '.', 'O'],
                ['.', '.', 'O', '.', '.', '.', 'O', '.'],
                ['.', '.', '.', 'O', '.', '.', '.', '.'],
                ['.', '.', '.', '.', 'X', '.', '.', '.'],
                ['.', 'X', '.', 'X', '.', '.', 'X', '.'],
                ['X', '.', 'X', '.', 'X', '.', '.', '.'],
                ['.', 'X', '.', '.', '.', 'X', '.', 'X']
            ],
            [  # Mid-game state2
                ['O', '.', '.', '.', '.', '.', 'O', '.'],
                ['.', 'O', '.', 'O', '.', '.', '.', '.'],
                ['.', '.', 'O', '.', '.', 'O', '.', 'O'],
                ['.', '.', '.', 'O', '.', '.', '.', '.'],
                ['.', '.', 'X', '.', '.', '.', '.', '.'],
                ['.', 'X', '.', 'X', '.', '.', 'X', '.'],
                ['X', '.', '.', '.', 'X', '.', '.', '.'],
                ['.', 'X', '.', 'X', '.', '.', '.', 'X']
            ],
            [  # Mid-game state3
                ['O', '.', '.', 'O', '.', '.', 'O', '.'],
                ['.', 'O', '.', '.', '.', 'O', '.', 'O'],
                ['O', '.', 'O', '.', 'O', '.', '.', '.'],
                ['.', '.', '.', '.', '.', '.', '.', '.'],
                ['.', '.', 'X', '.', 'X', '.', '.', '.'],
                ['.', 'X', '.', '.', '.', 'X', '.', '.'],
                ['X', '.', 'X', '.', '.', '.', '.', '.'],
                ['.', 'X', '.', 'X', '.', '.', '.', 'X']
            ],
            [  # Mid-game state4
                ['O', '.', 'O', '.', 'O', '.', '.', '.'],
                ['.', 'O', '.', '.', '.', 'O', '.', '.'],
                ['O', '.', '.', '.', 'O', '.', 'O', '.'],
                ['.', '.', '.', 'O', '.', '.', '.', '.'],
                ['.', '.', '.', 'X', '.', 'X', '.', '.'],
                ['.', 'X', '.', '.', '.', 'X', '.', 'X'],
                ['X', '.', 'X', '.', 'X', '.', '.', '.'],
                ['.', 'X', '.', '.', '.', 'X', '.', '.']
            ],
            [  # Late-game state
                ['.', '.', '.', '.', '.', '.', '.', '.'],
                ['.', 'O', '.', '.', '.', '.', '.', '.'],
                ['.', '.', '.', '.', '.', 'O', '.', '.'],
                ['.', '.', '.', 'X', '.', '.', '.', '.'],
                ['.', '.', '.', '.', '.', '.', 'O', '.'],
                ['.', '.', 'X', '.', '.', '.', '.', '.'],
                ['.', '.', '.', '.', '.', '.', '.', '.'],
                ['.', '.', '.', '.', '.', '.', '.', '.']
            ],
            [  # AI winning state
                ['.', '.', '.', '.', '.', '.', '.', '.'],
                ['.', '.', '.', '.', '.', '.', '.', '.'],
                ['.', '.', '.', '.', '.', '.', '.', '.'],
                ['.', '.', 'X', '.', '.', '.', '.', '.'],
                ['.', '.', '.', '.', '.', 'X', '.', '.'],
                ['.', '.', '.', 'X', '.', '.', '.', '.'],
                ['.', '.', '.', '.', '.', '.', '.', '.'],
                ['.', '.', '.', '.', '.', '.', '.', '.']
            ],
            [  # Player winning state
                ['.', '.', '.', '.', '.', '.', '.', '.'],
                ['.', '.', '.', '.', '.', '.', '.', '.'],
                ['.', '.', '.', '.', '.', '.', '.', '.'],
                ['.', '.', 'O', '.', '.', '.', '.', '.'],
                ['.', '.', '.', '.', '.', 'O', '.', '.'],
                ['.', '.', '.', 'O', '.', '.', '.', '.'],
                ['.', '.', '.', '.', '.', '.', '.', '.'],
                ['.', '.', '.', '.', '.', '.', '.', '.']
            ]
        ]
        print("Choose a predefined board state:")
        while True:
            try:
                choice = int(input("Enter a number (1-8): "))
                if 1 <= choice <= 8:
                    return boards[choice - 1]
                else:
                    print("Invalid choice. Please enter a number between 1 and 8.")
            except ValueError:
                print("Invalid input. Please enter a number.")
    
    def evaluate_custom_state(self):
        """Main function to allow user to choose a board state and evaluate the Minimax decision."""
        board = self.select_predefined_board()
        print("Here is the board you selected:")
        self.print_board(board)
        
        best_utility, best_move_sequence = self.minimax(board, 0, True)

        print("\nBest Possible Outcome:")
        if best_utility == 1:
            print("AI (X) wins! (1)")
        elif best_utility == -1:
            print("Player (O) wins! (-1)")
        else:
            print("It's a draw. (0)")

        print("\nBest Move Sequence to Achieve This Outcome:")
        for i, move in enumerate(best_move_sequence):
            print(f"Step {i + 1}: Move from {move[0]} to {move[1]}")
    
    def move(self, board, move):
        """Returns a new board state after making a move."""
        new_board = [list(row) for row in board]  # board copy
        (r1, c1), (r2, c2) = move
        new_board[r2][c2] = new_board[r1][c1]
        new_board[r1][c1] = '.'  # Empty the old position
        
        # Handle captures
        if abs(r2 - r1) == 2: 
            mid_r, mid_c = (r1 + r2) // 2, (c1 + c2) // 2
            new_board[mid_r][mid_c] = '.'  # Remove captured piece
        
        return new_board
    
    def print_board(self, board):
        """Prints the board in a readable format."""
        for row in board:
            print(' '.join(row)) #so each row is printed on a new line, displaying the board row by row.
        print() 

if __name__ == "__main__":
    minimax_solver = CheckersMinimax()
    minimax_solver.evaluate_custom_state()
