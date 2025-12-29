from HandEvaluator import HandRank
from Pieces import Piece, PieceType

def ask_loc(player):
    return None

def calc_piece(hand_rank):
    return None

"""
    Walks through the Movement Phase for the inputed player

    If player played a poker hand: calc piece created then can place piece in first two ranks
    Otherwise skip phase
    
"""
def PlacementPhase(player, hand_rank, board):
    
    # Check if played a poker hand
    if (hand_rank != None):

        # Calc piece + loc, then place on the board
        piece = calc_piece()
        r, c = ask_loc(player)
        board.place_piece(piece, (r,c))