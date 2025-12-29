from HandEvaluator import HandRank
from Pieces import Piece, PieceType
import string

HAND_TO_PIECE = {
    HandRank.HIGH_CARD:     PieceType.WARRIOR,
    HandRank.ONE_PAIR:      PieceType.ARCHER,
    HandRank.TWO_PAIR:      PieceType.KNIGHT,
    HandRank.THREE_KIND:    PieceType.WIZARD,
    HandRank.STRAIGHT:      PieceType.CATAPULT,
    HandRank.FLUSH:         PieceType.JUGGERNAUT,
    HandRank.FULL_HOUSE:    PieceType.DIREWOLF,
    HandRank.FOUR_KIND:     PieceType.JESTER,
    HandRank.STRAIGHT_FLUSH: PieceType.QUEEN,
}


def ask_loc(player, board):
    # Allowed rows depend on player color
    if player.color == "Black":
        allowed_rows = {0, 1}
    else:
        allowed_rows = {board.rows - 1, board.rows - 2}

    letters = string.ascii_uppercase[:board.cols]

    while True:
        print(f"Place on rows {sorted(allowed_rows)} only.")
        print(f"Valid columns: {letters}")
        raw = input("Enter placement (eg. A7): ").strip().upper()

        # Basic format check
        if len(raw) < 2:
            print("Invalid format — use letter+number like A3. Try again.\n")
            continue

        col_char = raw[0]
        row_str = raw[1:]

        # Column check
        if col_char not in letters:
            print("Invalid column letter. Try again.\n")
            continue

        # Row number check
        if not row_str.isdigit():
            print("Row must be a number. Try again.\n")
            continue

        r = int(row_str)
        c = letters.index(col_char)

        # In-bounds check
        if not board.in_bounds((r, c)):
            print("That position is outside the board. Try again.\n")
            continue

        # Placement row restriction
        if r not in allowed_rows:
            print("You may only place in your starting rows. Try again.\n")
            continue

        # Occupied square check
        if board.get_piece((r, c)) is not None:
            print("That square is already occupied. Pick another.\n")
            continue

        return r, c


def calc_piece(hand_rank, player):

    piece_type = HAND_TO_PIECE.get(hand_rank)
    return Piece(piece_type, player.color)


"""
    Walks through the Movement Phase for the inputed player

    If player played a poker hand: calc piece created then can place piece in first two ranks
    Otherwise skip phase
    
"""
def PlacementPhase(player, hand_rank, board):
    
    # Check if played a poker hand
    if (hand_rank != None):

        # Calc piece + loc, then place on the board
        piece = calc_piece(hand_rank, player)
        print(f"Piece created: {piece.type.name}")
        r, c = ask_loc(player, board)
        board.place_piece(piece, (r,c))