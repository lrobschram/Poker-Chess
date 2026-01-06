import pygame
from Screens import Screen

ROWS, COLS = 8, 8
TILE = 70

def draw_board(screen):
    for r in range(ROWS):
        for c in range(COLS):
            color = (180, 180, 180) if (r + c) % 2 == 0 else (120, 120, 120)
            rect = pygame.Rect(c*TILE, r*TILE, TILE, TILE)
            pygame.draw.rect(screen, color, rect)

def get_square_from_mouse(pos):
    x, y = pos
    return y // TILE, x // TILE


def draw_pieces(screen, board_state, font):
    for r in range(ROWS):
        for c in range(COLS):
            piece = board_state[r][c]
            if piece is None:
                continue

            text = font.render(piece.piece_initial(), True, (0, 0, 0))
            screen.blit(text, (c*TILE + 22, r*TILE + 15))

def draw_highlights(screen, moves):
    for r,c in moves:
        rect = pygame.Rect(c*TILE, r*TILE, TILE, TILE)
        pygame.draw.rect(screen, (255, 200, 0), rect, 4)


class MovementScreen:

    def __init__(self):
        self.font = pygame.font.SysFont(None, 42)
        self.moves = []
        self.selected = False
        self.curr_piece = None

    def handle_event(self, event, game):

        if event.type == pygame.MOUSEBUTTONDOWN:

            row, col = get_square_from_mouse(event.pos)
            print("Clicked:", (row, col))

            if not self.selected:
                piece = game.board.get_piece( (row, col) )

                if piece != None:
                    self.curr_piece = (row, col)
                    self.moves = piece.get_raw_moves(game.board)
                    self.selected = True
                else:
                    self.moves = []
            else:
                if (game.board.get_piece((row, col)) == None):
                    if ((row, col) in self.moves):
                        game.board.move_piece(self.curr_piece,(row, col))

                self.selected = False
                self.moves = []

        if (not game.get_current_player().can_move()):
            return Screen.ATTACK
        return Screen.MOVEMENT

    def draw(self, screen, game):
        self.board_state = game.board.grid
        screen.fill((240, 240, 240))  # background
        draw_board(screen)
        draw_highlights(screen, self.moves)
        draw_pieces(screen, self.board_state, self.font)