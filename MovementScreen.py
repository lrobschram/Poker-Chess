import pygame
from Screens import Screen
from ui import Button

ROWS, COLS = 8, 8
TILE = 70

def draw_board(screen, x0=0, y0=0):
    for r in range(ROWS):
        for c in range(COLS):
            color = (180, 180, 180) if (r + c) % 2 == 0 else (120, 120, 120)
            rect = pygame.Rect(x0 + c*TILE, y0 + r*TILE, TILE, TILE)
            pygame.draw.rect(screen, color, rect)

def get_square_from_mouse(pos, x0=0, y0=0):
    x, y = pos
    x -= x0
    y -= y0
    if x < 0 or y < 0:
        return None
    col = x // TILE
    row = y // TILE
    if row < 0 or row >= ROWS or col < 0 or col >= COLS:
        return None
    return row, col


def draw_pieces(screen, board_state, font, x0=0, y0=0):
    for r in range(ROWS):
        for c in range(COLS):
            piece = board_state[r][c]
            if piece is None:
                continue
            text = font.render(piece.piece_initial(), True, (0, 0, 0))
            screen.blit(text, (x0 + c*TILE + 22, y0 + r*TILE + 15))


def draw_highlights(screen, moves, x0=0, y0=0):
    for r, c in moves:
        rect = pygame.Rect(x0 + c*TILE, y0 + r*TILE, TILE, TILE)
        pygame.draw.rect(screen, (255, 200, 0), rect, 4)

def draw_error(screen, pos, x0=0, y0=0):
    rect = pygame.Rect(x0 + pos[1]*TILE, y0 + pos[0]*TILE, TILE, TILE)
    pygame.draw.rect(screen, (255, 0, 0), rect, 4)


def draw_panel(screen, font, game, x0, w, h):
    # panel background
    pygame.draw.rect(screen, (220, 220, 220), pygame.Rect(x0, 0, w, h))

    player = game.get_current_player()
    lines = [
        f"Phase: MOVEMENT",
        f"Player: {player.color}",
        f"Moves left: {player.movements_left}",  # adjust to your field/method
    ]

    y = 20
    for line in lines:
        text = font.render(line, True, (0, 0, 0))
        screen.blit(text, (x0 + 15, y))
        y += 35


class MovementScreen:

    def __init__(self):
        self.font = pygame.font.SysFont("helvetica", 35)
        self.hud_font = pygame.font.SysFont("helvetica", 18)
        self.pos_moves = []
        self.selected = False
        self.curr_piece = None
        self.pieces_moved = []
        self.error = False
        self.err_loc = None
        self.error_start_time = 0
        self.ERROR_DURATION = 500  # milliseconds (0.5 seconds)
        self.skip_button = Button(
            rect=(COLS*TILE + 20, 200, 160, 40),  # sidebar position
            text="Skip to Attack",
            font=self.hud_font,
            bg_color=(200, 200, 200)
            )

    def handle_event(self, event, game):

        if self.skip_button.is_clicked(event):
            return Screen.ATTACK

        if event.type == pygame.MOUSEBUTTONDOWN:

            sq = get_square_from_mouse(event.pos, 0, 0)
            if sq is None:
                return Screen.MOVEMENT
            row, col = sq

            if not self.selected:
                piece = game.board.get_piece( (row, col) )

                if piece != None:
                    if (not piece in self.pieces_moved) and (game.get_current_player().color == piece.owner):
                        self.curr_piece = (row, col)
                        self.pos_moves = piece.get_raw_moves(game.board)
                        self.selected = True
                    else:
                        self.error = True
                        self.err_loc = (row, col)
                        self.error_start_time = pygame.time.get_ticks()
                else:
                    self.pos_moves = []
            else:
                if (game.board.get_piece((row, col)) == None):
                    if ((row, col) in self.pos_moves):
                        game.board.move_piece(self.curr_piece,(row, col))
                        self.pieces_moved.append(game.board.get_piece((row, col)))
                        game.get_current_player().use_move()

                self.selected = False
                self.pos_moves = []

        if (not game.get_current_player().can_move()):
            return Screen.ATTACK
        return Screen.MOVEMENT

    def draw(self, screen, game):
        now = pygame.time.get_ticks()
        if self.error and now - self.error_start_time > self.ERROR_DURATION:
            self.error = False
            self.err_loc = None

        board_x = 0
        board_y = 0
        panel_x = COLS * TILE
        panel_w = 200
        panel_h = ROWS * TILE

        screen.fill((240, 240, 240))
        draw_board(screen, board_x, board_y)
        draw_highlights(screen, self.pos_moves, board_x, board_y)
        if self.error:
            draw_error(screen, self.err_loc, board_x, board_y)
        draw_pieces(screen, game.board.grid, self.font, board_x, board_y)
        draw_panel(screen, self.hud_font, game, panel_x, panel_w, panel_h)
        self.skip_button.draw(screen)

    def on_enter(self, screen, game):
        game.get_current_player().start_turn()
        self.pieces_moved = []