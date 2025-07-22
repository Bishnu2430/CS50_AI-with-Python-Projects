import math
import copy

class TicTacToe:
    def __init__(self):
        # Initialize empty 3x3 board
        self.board = [[None for _ in range(3)] for _ in range(3)]
        self.X = "X"
        self.O = "O"
        self.EMPTY = None
    
    def print_board(self):
        """Print the current board state"""
        print("\n   0   1   2")
        for i in range(3):
            print(f"{i}  ", end="")
            for j in range(3):
                if self.board[i][j] is None:
                    print(" ", end="")
                else:
                    print(self.board[i][j], end="")
                if j < 2:
                    print(" | ", end="")
            print()
            if i < 2:
                print("  -----------")
        print()
    
    def actions(self, board):
        """Return set of all possible actions (i, j) available on the board"""
        possible_actions = set()
        for i in range(3):
            for j in range(3):
                if board[i][j] is None:
                    possible_actions.add((i, j))
        return possible_actions
    
    def player(self, board):
        """Return player who has the next turn on a board"""
        x_count = sum(row.count(self.X) for row in board)
        o_count = sum(row.count(self.O) for row in board)
        
        # X goes first
        if x_count <= o_count:
            return self.X
        else:
            return self.O
    
    def result(self, board, action):
        """Return the board that results from making move (i, j) on the board"""
        if action not in self.actions(board):
            raise Exception("Invalid action")
        
        # Make a deep copy of the board
        new_board = copy.deepcopy(board)
        new_board[action[0]][action[1]] = self.player(board)
        return new_board
    
    def winner(self, board):
        """Return the winner of the game, if there is one"""
        # Check rows
        for row in board:
            if row[0] == row[1] == row[2] and row[0] is not None:
                return row[0]
        
        # Check columns
        for j in range(3):
            if board[0][j] == board[1][j] == board[2][j] and board[0][j] is not None:
                return board[0][j]
        
        # Check diagonals
        if board[0][0] == board[1][1] == board[2][2] and board[0][0] is not None:
            return board[0][0]
        
        if board[0][2] == board[1][1] == board[2][0] and board[0][2] is not None:
            return board[0][2]
        
        return None
    
    def terminal(self, board):
        """Return True if game is over, False otherwise"""
        # Game is over if someone won or board is full
        return self.winner(board) is not None or len(self.actions(board)) == 0
    
    def utility(self, board):
        """Return 1 if X has won the game, -1 if O has won, 0 otherwise"""
        winner = self.winner(board)
        if winner == self.X:
            return 1
        elif winner == self.O:
            return -1
        else:
            return 0
    
    def minimax(self, board):
        """
        Return the optimal action for the current player on the board using Minimax algorithm
        """
        if self.terminal(board):
            return None
        
        current_player = self.player(board)
        
        if current_player == self.X:
            # X is maximizing player
            _, action = self.max_value(board)
            return action
        else:
            # O is minimizing player  
            _, action = self.min_value(board)
            return action
    
    def max_value(self, board):
        """Return maximum value and corresponding action for maximizing player (X)"""
        if self.terminal(board):
            return self.utility(board), None
        
        v = -math.inf
        best_action = None
        
        for action in self.actions(board):
            min_val, _ = self.min_value(self.result(board, action))
            if min_val > v:
                v = min_val
                best_action = action
        
        return v, best_action
    
    def min_value(self, board):
        """Return minimum value and corresponding action for minimizing player (O)"""
        if self.terminal(board):
            return self.utility(board), None
        
        v = math.inf
        best_action = None
        
        for action in self.actions(board):
            max_val, _ = self.max_value(self.result(board, action))
            if max_val < v:
                v = max_val
                best_action = action
        
        return v, best_action
    
    def make_move(self, row, col):
        """Make a move on the actual game board"""
        if self.board[row][col] is not None:
            return False
        
        current_player = self.player(self.board)
        self.board[row][col] = current_player
        return True
    
    def play_game(self):
        """Main game loop"""
        print("Welcome to Tic Tac Toe!")
        print("You are X, Computer is O")
        print("Enter moves as 'row col' (0-2 for both)")
        
        while not self.terminal(self.board):
            self.print_board()
            current_player = self.player(self.board)
            
            if current_player == self.X:
                # Human player turn
                try:
                    move_input = input("Your move (row col): ").strip().split()
                    if len(move_input) != 2:
                        print("Please enter row and column separated by space")
                        continue
                    
                    row, col = int(move_input[0]), int(move_input[1])
                    
                    if row < 0 or row > 2 or col < 0 or col > 2:
                        print("Row and column must be between 0 and 2")
                        continue
                    
                    if not self.make_move(row, col):
                        print("That position is already taken!")
                        continue
                        
                except (ValueError, IndexError):
                    print("Please enter valid numbers for row and column")
                    continue
            
            else:
                # Computer turn
                print("Computer is thinking...")
                action = self.minimax(self.board)
                if action:
                    self.make_move(action[0], action[1])
                    print(f"Computer chose position ({action[0]}, {action[1]})")
        
        # Game over
        self.print_board()
        winner = self.winner(self.board)
        if winner == self.X:
            print("Congratulations! You won!")
        elif winner == self.O:
            print("Computer wins! Better luck next time.")
        else:
            print("It's a tie!")


def main():
    game = TicTacToe()
    game.play_game()


if __name__ == "__main__":
    main()