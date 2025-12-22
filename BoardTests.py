from Board import Board
from Pieces import Piece, PieceType

def main():
    board = Board(8, 8)

    king = Piece(PieceType.KING, owner="White")
    archer = Piece(PieceType.ARCHER, owner="Black")
    wizard = Piece(PieceType.WIZARD, owner="White")

    board.place_piece(king, (0, 4))
    board.place_piece(archer, (6, 4))
    board.place_piece(wizard, (3, 3))

    print(board)

    print("\nWizard attacks Archer!")
    archer.take_damage(wizard.attack)

    print(f"Archer health: {archer.health}")

if __name__ == "__main__":
    main()