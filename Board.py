class Board:

    def __init__(self, rows=8, cols=8):
        self.rows = rows
        self.cols = cols
        self.grid = [[None for _ in range(rows)] for _ in range(cols)]

    def in_bounds(self, pos):
        x, y = pos
        return 0 <= x < self.rows and 0 <= y < self.cols

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
        lines = []
        for row in self.grid:
            line = []
            for cell in row:
                line.append(cell.piece_initial() if cell else ".")
            lines.append(" ".join(line))
        return "\n".join(lines)
    
    def get_legal_moves(self, piece):
        return NotImplementedError