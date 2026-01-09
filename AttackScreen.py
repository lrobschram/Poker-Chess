import pygame
from Screens import Screen
from ui import Button
from AttackRules import get_attack_targets
from Pieces import PieceType

ROWS, COLS = 8, 8
TILE = 70

# -------------------- Utility Functions --------------------

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

def draw_error(screen, pos, x0=0, y0=0):
    rect = pygame.Rect(x0 + pos[1]*TILE, y0 + pos[0]*TILE, TILE, TILE)
    pygame.draw.rect(screen, (255, 0, 0), rect, 4)

def draw_panel(screen, font, game, x0, w, h, phase="ATTACK", attacks_left=0):
    pygame.draw.rect(screen, (220, 220, 220), pygame.Rect(x0, 0, w, h))
    player = game.get_current_player()
    lines = [
        f"Phase: {phase}",
        f"Player: {player.color}",
        f"Attacks left: {attacks_left}"
    ]
    y = 20
    for line in lines:
        text = font.render(line, True, (0, 0, 0))
        screen.blit(text, (x0 + 15, y))
        y += 35

# -------------------- AttackScreen Class --------------------

class AttackScreen:

    def __init__(self):
        self.font = pygame.font.SysFont("helvetica", 35)
        self.hud_font = pygame.font.SysFont("helvetica", 18)

        self.used_attackers = set()  # Pieces that already attacked this phase
        self.attacks_left = 3        # Max attacks per phase
        self.selected_attacker = None
        self.valid_targets = []

        self.error = False
        self.err_loc = None
        self.error_start_time = 0
        self.ERROR_DURATION = 500  # milliseconds

        self.skip_button = Button(
            rect=(250, 250, 160, 40),
            text="Skip Phase",
            font=self.hud_font,
            bg_color=(200, 200, 200)
        )

    # -------------------- Event Handling --------------------

    def handle_event(self, event, game):
        if self.skip_button.is_clicked(event):
            return Screen.MOVEMENT

        if event.type == pygame.MOUSEBUTTONDOWN:
            square = get_square_from_mouse(pygame.mouse.get_pos())
            if square:
                self.handle_board_click(game, *square)

        return Screen.ATTACK

    # -------------------- Board Click Logic --------------------

    def handle_board_click(self, game, row, col):
        board = game.board
        piece = board.grid[row][col]
        current_player = game.get_current_player()

        # Step 1: If attacker already selected, attempt attack
        if self.selected_attacker:
            if (row, col) in self.valid_targets:
                self.resolve_attack(game, row, col)
            else:
                # Invalid attack: deselect attacker and show error
                self.trigger_error((row, col))
                self.selected_attacker = None
                self.valid_targets = []
            return

        # Step 2: Select a new piece if none selected
        if piece and piece.owner == current_player.color:
            if piece in self.used_attackers:
                self.trigger_error((row, col))  # cannot attack twice
                return
            # Valid piece: select and show targets
            self.selected_attacker = piece
            self.valid_targets = get_attack_targets(board, piece)
        else:
            # Not a friendly piece
            self.trigger_error((row, col))

    # -------------------- Resolve Attack --------------------

    def resolve_attack(self, game, row, col):
        attacker = self.selected_attacker
        defender = game.board.grid[row][col]

        defender.take_damage(attacker.attack)

        if defender.is_piece_dead():
            if defender.type == PieceType.KING:
                game.game_over(attacker.owner)
            game.board.remove_piece(defender)

        # Mark attacker as used
        self.used_attackers.add(attacker)
        self.attacks_left -= 1

        # Clear selection
        self.selected_attacker = None
        self.valid_targets = []

        if self.attacks_left <= 0:
            return Screen.MOVEMENT

    # -------------------- Drawing --------------------

    def draw_attack_highlights(self, screen, attacker, targets, board_x=0, board_y=0, TILE=TILE):
        HIGHLIGHT_SIZE = TILE // 3

        # Green highlight for selected attacker
        if attacker:
            inner_x = board_x + attacker.col * TILE + (TILE - HIGHLIGHT_SIZE) // 2
            inner_y = board_y + attacker.row * TILE + (TILE - HIGHLIGHT_SIZE) // 2
            pygame.draw.rect(screen, (0, 255, 0), pygame.Rect(inner_x, inner_y, HIGHLIGHT_SIZE, HIGHLIGHT_SIZE))

        # Yellow highlights for valid targets
        for r, c in targets:
            inner_x = board_x + c * TILE + (TILE - HIGHLIGHT_SIZE) // 2
            inner_y = board_y + r * TILE + (TILE - HIGHLIGHT_SIZE) // 2
            pygame.draw.rect(screen, (255, 200, 0), pygame.Rect(inner_x, inner_y, HIGHLIGHT_SIZE, HIGHLIGHT_SIZE))

        # Red overlay for pieces that already attacked
        for used_piece in self.used_attackers:
            overlay = pygame.Surface((TILE, TILE), pygame.SRCALPHA)
            overlay.fill((255, 0, 0, 100))  # semi-transparent red
            inner_x = board_x + used_piece.col * TILE
            inner_y = board_y + used_piece.row * TILE
            screen.blit(overlay, (inner_x, inner_y))

    def draw(self, screen, game):
        now = pygame.time.get_ticks()
        if self.error and now - self.error_start_time > self.ERROR_DURATION:
            self.error = False
            self.err_loc = None

        board_x, board_y = 0, 0
        panel_x, panel_w, panel_h = COLS*TILE, 200, ROWS*TILE

        screen.fill((240, 240, 240))
        draw_board(screen, board_x, board_y)
        draw_pieces(screen, game.board.grid, self.font, board_x, board_y)
        self.draw_attack_highlights(screen, self.selected_attacker, self.valid_targets, board_x, board_y, TILE)

        if self.error:
            draw_error(screen, self.err_loc, board_x, board_y)

        draw_panel(screen, self.hud_font, game, panel_x, panel_w, panel_h, phase="ATTACK", attacks_left=self.attacks_left)
        self.skip_button.draw(screen)

    # -------------------- Lifecycle --------------------

    def on_enter(self, screen, game):
        self.attacks_left = 3
        self.used_attackers = set()
        self.selected_attacker = None
        self.valid_targets = []
        self.error = False
        game.get_current_player().start_turn()

    def on_exit(self, screen, game):
        return None

    # -------------------- Helper --------------------

    def trigger_error(self, pos):
        self.error = True
        self.err_loc = pos
        self.error_start_time = pygame.time.get_ticks()
