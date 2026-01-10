import pygame
from Screens import Screen
from ui import Button, ROWS, COLS, TILE, draw_board, draw_error, draw_borders, draw_pieces, get_square_from_mouse
from AttackRules import get_attack_targets
from Pieces import PieceType

# -------------------- Utility Functions --------------------

def draw_panel(screen, font, game, x0, w, h, phase="Attack", attacks_left=0):
    pygame.draw.rect(screen, (255, 220, 220), pygame.Rect(x0, 0, w, h))
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
            rect=(COLS*TILE + 20, 200, 160, 40),
            text="Skip Attack",
            font=self.hud_font,
            bg_color=(200, 200, 200)
        )

    # -------------------- Event Handling --------------------

    def handle_event(self, event, game):
        if self.skip_button.is_clicked(event):
            return Screen.POKER

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
                # self.trigger_error((row, col))
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
            # inner_x = board_x + attacker.col * TILE + (TILE - HIGHLIGHT_SIZE) // 2
            # inner_y = board_y + attacker.row * TILE + (TILE - HIGHLIGHT_SIZE) // 2
            # pygame.draw.rect(screen, (0, 255, 0), pygame.Rect(inner_x, inner_y, HIGHLIGHT_SIZE, HIGHLIGHT_SIZE))
            draw_borders(screen, (attacker.row, attacker.col), (0, 100, 255), board_x, board_y)

        # Yellow highlights for valid targets
        for r, c in targets:
            # inner_x = board_x + c * TILE + (TILE - HIGHLIGHT_SIZE) // 2
            # inner_y = board_y + r * TILE + (TILE - HIGHLIGHT_SIZE) // 2
            # pygame.draw.rect(screen, (255, 200, 0), pygame.Rect(inner_x, inner_y, HIGHLIGHT_SIZE, HIGHLIGHT_SIZE))
            draw_borders(screen, (r,c), (255, 200, 0), board_x, board_y)

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
        game.switch_player()
        return None

    # -------------------- Helper --------------------

    def trigger_error(self, pos):
        self.error = True
        self.err_loc = pos
        self.error_start_time = pygame.time.get_ticks()
