from Board import Board
from Player import Player
from Pieces import Piece, PieceType
from HandEvaluator import HandRank
from MovementRules import MOVEMENT_RULES

class Game:
    def __init__(self):
        self.board = Board(8, 8)
        self.players = {
            "White": Player("White"),
            "Black": Player("Black")
        }
        self.current_player_color = "White"
        self.board.setup_initial_game()
        
    def get_current_player(self):
        return self.players[self.current_player_color]
    
    def switch_player(self):
        self.current_player_color = "Black" if self.current_player_color == "White" else "White"

    def print_board(self):
        print(self.board)

    def is_game_over(self):
        # Check both players' kings
        for color in ["White", "Black"]:
            if self.board.is_king_dead(color):
                winner = "Black" if color == "White" else "White"
                print(f"{color} King is dead! {winner} wins!")
                return True
        return False