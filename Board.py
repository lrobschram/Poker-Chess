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

    def print_board(self):
        board = "  ABCDEFGH"
        for i in range(self.rows):
            rowi = "\n" + str(i) + " "
            for j in range(self.cols):
                if (self.grid[i][j] == None):
                    rowi += "-"
                else:
                    rowi += self.grid[i][j].piece_initial() # TODO make a method to print piece initial
            board += rowi
        print(board)

testBoard = Board()
testBoard.print_board()