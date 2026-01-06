class Board:
    def __init__(self, rows=8, cols=8):
        self.rows = rows
        self.cols = cols
        self.grid = [[None for _ in range(rows)] for _ in range(cols)]
        self.kings = {}

    def in_bounds(self, pos):
        x, y = pos
        return 0 <= x < self.cols and 0 <= y < self.rows

    def get_piece(self, pos):
        x, y = pos
        return self.grid[x][y]

    def place_piece(self, piece, pos):
        x, y = pos
        piece.row = x
        piece.col = y
        self.grid[x][y] = piece

    def move_piece(self, start, end):
        piece = self.get_piece(start)
        self.grid[end[0]][end[1]] = piece
        self.grid[start[0]][start[1]] = None
        piece.row = end[0]
        piece.col = end[1]

    def remove_piece(self, piece):
        self.grid[piece.row][piece.col] = None
        piece.row = None
        piece.col = None


    def setup_initial_game(self, white_player, black_player):
        from Pieces import Piece, PieceType
    #place white king, 2 Warriors and 1 Archer
        K = Piece(PieceType.KING, "White")
        self.place_piece(K, (7, 4))
        self.kings["White"] = K  # Store reference

        A = Piece(PieceType.ARCHER, "White")
        self.place_piece(A, (7, 3))
        W1 = Piece(PieceType.WARRIOR, "White")
        self.place_piece(W1, (6, 3))
        W2 = Piece(PieceType.WARRIOR, "White")
        self.place_piece(W2, (6,4))

        white_player.my_pieces.append(K)
        white_player.my_pieces.append(A)
        white_player.my_pieces.append(W1)
        white_player.my_pieces.append(W2)

    #place piece black king, 2 Warriors and Archer
    
        k = Piece(PieceType.KING, "Black")
        self.place_piece(k, (0, 3))
        self.kings["Black"] = k  # Store reference

        a = Piece(PieceType.ARCHER, "Black")
        self.place_piece(a, (0, 4))
        w1 = Piece(PieceType.WARRIOR, "Black")
        self.place_piece(w1, (1, 3))
        w2 = Piece(PieceType.WARRIOR, "Black")
        self.place_piece(w2, (1, 4))

        black_player.my_pieces.append(k)
        black_player.my_pieces.append(a)
        black_player.my_pieces.append(w1)
        black_player.my_pieces.append(w2)

    def attack(self, attacker_pos, target_pos):
        attacker = self.get_piece(attacker_pos)
        target = self.get_piece(target_pos)
        
        if not attacker:
            raise RuntimeError("No attacker at that position")
        if not target:
            raise RuntimeError("No target at that position")
        if attacker.color == target.color:
            raise RuntimeError("Cannot attack own piece")
        
        # Apply attack
        died = target.take_damage(attacker.attack_power)
        if died:
            self.remove_piece(target)
       

    def is_king_dead(self, color):
        """
        Check if the King for a specific color is dead.
        Uses the stored King reference and Piece.is_piece_dead() for efficiency.
        Args:
            color (str): "White" or "Black"
        Returns:
            bool: True if King is dead (health <= 0), False otherwise
        """
        king = self.kings.get(color)
        if king is None:
            return False
        return king.is_piece_dead()
        
    



    def __str__(self):
        col_labels = "  " + " ".join(chr(ord("A") + c) for c in range(self.cols))
        lines = [col_labels]

        for r in range(self.rows):
            row_cells = []
            for c in range(self.cols):
                cell = self.grid[r][c]
                row_cells.append(cell.piece_initial() if cell else ".")
            lines.append(f"{r} " + " ".join(row_cells))

        return "\n".join(lines)
    
    def get_legal_moves(self, piece):

        
        return NotImplementedError