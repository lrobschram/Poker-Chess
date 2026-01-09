from Board import Board
from Player import Player
from Pieces import Piece, PieceType
from HandEvaluator import HandRank
from MovementRules import MOVEMENT_RULES
from PokerPhase import PokerPhase
from PlacementPhase import PlacementPhase

class Game:
    def __init__(self):
        self.board = Board(8, 8)
        self.players = {
            "White": Player("White"),
            "Black": Player("Black")
        }
        self.current_player_color = "White"
        self.board.setup_initial_game(self.players["White"], self.players["Black"])
        
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
    
def main():
    game = Game()

    while(not game.is_game_over()):

        # Get the current player
        print("~~~~~~~~\n")
        curr_player = game.get_current_player()
        curr_player.start_turn()
        print(f"Current player: {curr_player.color}")
        print("\nMy current pieces:")
        curr_player.print_pieces()

        # Poker Phase
        hand_rank = PokerPhase(curr_player)

        # Placement Phase
        game.print_board()
        PlacementPhase(curr_player, hand_rank, game.board)

        # Movement Phase
        MovementPhase(curr_player, game.board)

        # Attack Phase

        game.switch_player()


if __name__ == "__main__":
    main()