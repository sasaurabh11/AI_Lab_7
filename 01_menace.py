import random
import time
from typing import List, Tuple, Optional
import os

class TicTacToeBoard:
    def __init__(self):
        self.board = [' ' for _ in range(9)]
        self.current_player = 'X'
        
    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        
    def display_board(self):
        self.clear_screen()
        print("\n=== Tic Tac Toe ===\n")
        
        print("Reference positions:")
        self._print_reference_board()
        print("\nCurrent game:")

        for i in range(0, 9, 3):
            print(f" {self._get_colored_piece(i)} │ {self._get_colored_piece(i+1)} │ {self._get_colored_piece(i+2)} ")
            if i < 6:
                print("───┼───┼───")
        print()

    def _get_colored_piece(self, position: int) -> str:
        piece = self.board[position]
        if piece == 'X':
            return f"\033[94mX\033[0m"  # Blue for X
        elif piece == 'O':
            return f"\033[91mO\033[0m"  # Red for O
        return piece

    def _print_reference_board(self):
        for i in range(0, 9, 3):
            print(f" {i} │ {i+1} │ {i+2} ")
            if i < 6:
                print("───┼───┼───")
        print()

    def make_move(self, position: int) -> bool:
        if self.is_valid_move(position):
            self.board[position] = self.current_player
            return True
        return False

    def is_valid_move(self, position: int) -> bool:
        return 0 <= position <= 8 and self.board[position] == ' '

    def check_winner(self) -> Optional[str]:
        winning_combinations = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Rows
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columns
            [0, 4, 8], [2, 4, 6]              # Diagonals
        ]
        
        for combo in winning_combinations:
            if (self.board[combo[0]] != ' ' and
                self.board[combo[0]] == self.board[combo[1]] == self.board[combo[2]]):
                return self.board[combo[0]]
        return None

    def is_board_full(self) -> bool:
        return ' ' not in self.board

    def get_available_moves(self) -> List[int]:
        return [i for i, piece in enumerate(self.board) if piece == ' ']

class AIPlayer:
    def __init__(self, difficulty: str = 'medium'):
        self.difficulty = difficulty
        self.winning_moves = {}

    def get_move(self, board: TicTacToeBoard) -> int:
        if self.difficulty == 'easy':
            return self._make_random_move(board)
        elif self.difficulty == 'medium':
            return self._make_smart_move(board)
        else:  # hard
            return self._make_best_move(board)

    def _make_random_move(self, board: TicTacToeBoard) -> int:
        available_moves = board.get_available_moves()
        return random.choice(available_moves)

    def _make_smart_move(self, board: TicTacToeBoard) -> int:
        for move in board.get_available_moves():
            board.board[move] = 'O'
            if board.check_winner() == 'O':
                board.board[move] = ' '
                return move
            board.board[move] = ' '

        for move in board.get_available_moves():
            board.board[move] = 'X'
            if board.check_winner() == 'X':
                board.board[move] = ' '
                return move
            board.board[move] = ' '

        if board.is_valid_move(4):
            return 4

        corners = [0, 2, 6, 8]
        available_corners = [x for x in corners if board.is_valid_move(x)]
        if available_corners:
            return random.choice(available_corners)

        return self._make_random_move(board)

    def _make_best_move(self, board: TicTacToeBoard) -> int:
        best_score = float('-inf')
        best_move = None

        for move in board.get_available_moves():
            board.board[move] = 'O'
            score = self._minimax(board, 0, False)
            board.board[move] = ' '

            if score > best_score:
                best_score = score
                best_move = move

        return best_move

    def _minimax(self, board: TicTacToeBoard, depth: int, is_maximizing: bool) -> int:
        winner = board.check_winner()
        if winner == 'O':
            return 1
        elif winner == 'X':
            return -1
        elif board.is_board_full():
            return 0

        if is_maximizing:
            best_score = float('-inf')
            for move in board.get_available_moves():
                board.board[move] = 'O'
                score = self._minimax(board, depth + 1, False)
                board.board[move] = ' '
                best_score = max(score, best_score)
            return best_score
        else:
            best_score = float('inf')
            for move in board.get_available_moves():
                board.board[move] = 'X'
                score = self._minimax(board, depth + 1, True)
                board.board[move] = ' '
                best_score = min(score, best_score)
            return best_score

def play_game():
    board = TicTacToeBoard()
    ai = AIPlayer(difficulty='medium')
    game_stats = {'wins': 0, 'losses': 0, 'draws': 0}

    while True:
        board.display_board()
        
        # Player's turn
        if board.current_player == 'X':
            try:
                position = int(input(f"\nEnter your move (0-8): "))
                if not board.make_move(position):
                    print("\nInvalid move! Try again.")
                    time.sleep(1)
                    continue
            except ValueError:
                print("\nPlease enter a number between 0 and 8!")
                time.sleep(1)
                continue
        # AI's turn
        else:
            print("\nAI is thinking...")
            time.sleep(0.5)
            position = ai.get_move(board)
            board.make_move(position)

        # Check for game end
        winner = board.check_winner()
        if winner:
            board.display_board()
            if winner == 'X':
                print("\nCongratulations! You won! 🎉")
                game_stats['wins'] += 1
            else:
                print("\nAI wins! Better luck next time! 🤖")
                game_stats['losses'] += 1
            break

        if board.is_board_full():
            board.display_board()
            print("\nIt's a draw! 🤝")
            game_stats['draws'] += 1
            break

        board.current_player = 'O' if board.current_player == 'X' else 'X'

    print("\nGame Statistics:")
    print(f"Wins: {game_stats['wins']}")
    print(f"Losses: {game_stats['losses']}")
    print(f"Draws: {game_stats['draws']}")

    play_again = input("\nWould you like to play again? (y/n): ").lower()
    if play_again == 'y':
        board = TicTacToeBoard()
        play_game()

if __name__ == "__main__":
    try:
        play_game()
    except KeyboardInterrupt:
        print("\n\nThanks for playing! Goodbye! 👋")