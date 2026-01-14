import pygame
from Screens import Screen
from ui import Button, ROWS, COLS, TILE, draw_board, draw_error, draw_borders, draw_pieces, get_square_from_mouse, draw_stats
from AttackRules import get_attack_targets
from Pieces import PieceType


# ---- Attack UI colors  ----
PANEL_RED   = (255, 220, 220)   # your current panel bg
CARD_BG       = (55, 55, 55)
TEXT_MAIN     = (235, 235, 230)
TEXT_MUTED    = (170, 170, 170)
ACCENT_RED   = (255, 0, 0)
DIVIDER       = (90, 90, 90)

def draw_kv(screen, font, x, y, label, value,
            label_color=TEXT_MUTED, value_color=TEXT_MAIN,
            line_gap=18):
    label_surf = font.render(label, True, label_color)
    value_surf = font.render(value, True, value_color)
    screen.blit(label_surf, (x, y))
    screen.blit(value_surf, (x, y + line_gap))

def draw_panel(screen, font, game, x0, w, h, phase="ATTACK", attacks_left=0, exiting=False):
    # panel background (mint green)
    panel = pygame.Rect(x0, 0, w, h)
    pygame.draw.rect(screen, PANEL_RED, panel)

    # inner dark "card" container
    pad = 14
    card = pygame.Rect(panel.x + pad, panel.y + pad, panel.w - 2*pad, panel.h - 2*pad)
    pygame.draw.rect(screen, CARD_BG, card, border_radius=14)
    pygame.draw.rect(screen, (0, 0, 0), card, 2, border_radius=14)

    # accent strip at top
    accent = pygame.Rect(card.x, card.y, card.w, 5)
    pygame.draw.rect(screen, ACCENT_RED, accent, border_radius=14)

    player = game.get_current_player()

    # --- layout metrics ---
    left_x = card.x + 14
    y = card.y + 18

    # Title
    title = font.render(phase, True, ACCENT_RED)
    screen.blit(title, (left_x, y))
    y += 28

    # Divider
    pygame.draw.line(screen, DIVIDER, (card.x + 10, y), (card.right - 10, y), 2)
    y += 14

    # Row 1
    draw_kv(screen, font, left_x,  y, "PLAYER", player.color)
    
    y += 46

    # Row 2
    if exiting:
        next_player = game.get_next_player()
        draw_kv(screen, font, left_x,  y, "Turn Ending...", " ")
        y += 35
        draw_kv(screen, font, left_x,  y, "NEXT PLAYER:", next_player.color)


    else:
        draw_kv(screen, font, left_x,  y, "ATTACKS LEFT", str(attacks_left))

    # If you want, show something else on the right (optional)
    # draw_kv(screen, font, right_x, y, "TURN", str(player.turn_num))
    y += 46


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

        #exit vatiables
        self.exiting = False
        self.exit_start_time = 0
        self.EXIT_DELAY = 3000  # milliseconds


        self.skip_button = Button(
            rect=(COLS*TILE + 20, 200, 160, 40),
            text="Skip Attack",
            font=self.hud_font,
            bg_color=(200, 200, 200)
        )
        self.last_clicked = None


    #--------------------- Start exit time -------------------

    def start_exit(self):
        if not self.exiting:
         self.exiting = True
         self.exit_start_time = pygame.time.get_ticks()

    # -------------------- Event Handling --------------------

    def handle_event(self, event, game):
        
        if self.skip_button.is_clicked(event):
            self.start_exit()

        if event.type == pygame.MOUSEBUTTONDOWN and not self.exiting:

            square = get_square_from_mouse(pygame.mouse.get_pos())
            if square:
                self.handle_board_click(game, *square)
        return Screen.ATTACK

    # -------------------- Board Click Logic --------------------

    def handle_board_click(self, game, row, col):
        board = game.board
        piece = board.grid[row][col]
        current_player = game.get_current_player()

            # Step 1: If attacker already selected, attempt action
        if self.selected_attacker:
            target_piece = board.get_piece((row, col))

            if (row, col) in self.valid_targets:
                self.last_clicked = target_piece

                # Decide heal vs attack
                if target_piece.owner == self.selected_attacker.owner:
                    # Heal
                    target_piece.take_heal(self.selected_attacker.heal)
                else:
                    # Attack
                    target_piece.take_damage(self.selected_attacker.attack)
                    if target_piece.is_piece_dead():
                        board.remove_piece(target_piece)

                # Mark attacker as used
                self.used_attackers.add(self.selected_attacker)
                current_player.use_attack()

                # Clear selection
                self.selected_attacker = None
                self.valid_targets = []

            else:
                # Invalid click
                self.trigger_error((row, col))
                self.selected_attacker = None
                self.valid_targets = []

            return

        # Step 2: Select new attacker
        if piece:
            if piece.owner == current_player.color:
                if piece in self.used_attackers:
                    self.trigger_error((row, col))  # cannot attack twice
                    return
                self.selected_attacker = piece
                self.valid_targets = get_attack_targets(board, piece)
                self.last_clicked = piece
            else:
                # Not a friendly piece
                self.last_clicked = piece
                self.trigger_error((row, col))

    # -------------------- Resolve Attack --------------------

    def resolve_attack(self, game, row, col):
        attacker = self.selected_attacker
        defender = game.board.grid[row][col]

        defender.take_damage(attacker.attack)

        # Mark attacker as used
        self.used_attackers.add(attacker)
        game.get_current_player().use_attack()

        # Clear selection
        self.selected_attacker = None
        self.valid_targets = []

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

        draw_panel(screen, self.hud_font, game, panel_x, panel_w, panel_h, phase="ATTACK", attacks_left= game.get_current_player().attacks_left, exiting= self.exiting)
        self.skip_button.draw(screen)

        if self.last_clicked != None:
            draw_stats(screen, self.hud_font, self.last_clicked, panel_x + 14)

    # -------------------- Lifecycle --------------------

    def on_enter(self, screen, game):
        self.used_attackers = set()
        self.selected_attacker = None
        self.valid_targets = []
        self.error = False
        self.exiting = False

    def on_exit(self, screen, game):
        
        game.switch_player()
        return None

    # -------------------- Helper --------------------

    def trigger_error(self, pos):
        self.error = True
        self.err_loc = pos
        self.error_start_time = pygame.time.get_ticks()

    # -------------------- Updating --------------------

    def update(self, screen, game):
         
        if game.is_game_over():
            return Screen.GAME_OVER

        if not game.get_current_player().can_attack():
            self.start_exit()

        if self.exiting:
            now = pygame.time.get_ticks()
            if now - self.exit_start_time >= self.EXIT_DELAY:
                return Screen.POKER
        return Screen.ATTACK
