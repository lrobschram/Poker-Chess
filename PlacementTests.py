from Player import Player
from PlacementPhase import PlacementPhase
from HandEvaluator import HandRank
from Pieces import Piece, PieceType
from Board import Board

def white_player_test():
    player = Player("White")
    board = Board()
    print(board)
    PlacementPhase(player, hand_rank=HandRank.FLUSH, board=board)
    print("\n")
    print(board)


def black_player_test():
    player = Player("Black")

def main():
    white_player_test()

if __name__ == "__main__":
    main()