class Board:

    def __init__(self, rows=8, cols=8):
        self.rows = rows
        self.cols = cols
        self.grid = [[None for _ in range(rows)] for _ in range(cols)]

    def in_bounds(self, pos):
        x, y = pos
        return 0 <= x < self.cols and 0 <= y < self.rows

    def get_piece(self, pos):
        x, y = pos
        return self.grid[x][y]

    def place_piece(self, piece, pos):
        x, y = pos
        self.grid[x][y] = piece

    def move_piece(self, start, end):
        piece = self.get_piece(start)
        self.grid[end[0]][end[1]] = piece
        self.grid[start[0]][start[1]] = None

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