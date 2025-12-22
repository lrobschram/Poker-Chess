class Board:

    def __init__(self, rows=8, cols=8):
        self.rows = rows
        self.cols = cols
        self.grid = [[None for _ in range(cols)] for _ in range(rows)]

    def in_bounds(self, pos):
        x, y = pos
        return 0 <= x < self.cols and 0 <= y < self.rows

    def get_piece(self, pos):
        x, y = pos
        return self.grid[y][x]

    def place_piece(self, piece, pos):
        x, y = pos
        self.grid[y][x] = piece

    def move_piece(self, start, end):
        piece = self.get_piece(start)
        self.grid[end[1]][end[0]] = piece
        self.grid[start[1]][start[0]] = None

    def __str__(self):
        lines = []
        for row in self.grid:
            line = []
            for cell in row:
                line.append(cell.piece_initial() if cell else ".")
            lines.append(" ".join(line))
        return "\n".join(lines)
    
    def get_legal_moves(self, piece):
        return NotImplementedError