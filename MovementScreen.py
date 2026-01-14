import pygame
from Screens import Screen
from ui import Button, ROWS, COLS, TILE, draw_board, draw_error, draw_highlights, draw_pieces, get_square_from_mouse, draw_stats, draw_borders


# ---- Movement UI colors (keep your green) ----
PANEL_GREEN   = (220, 255, 220)   # your current panel bg
CARD_BG       = (55, 55, 55)
TEXT_MAIN     = (235, 235, 230)
TEXT_MUTED    = (170, 170, 170)
ACCENT_GREEN   = (0, 255, 0)
DIVIDER       = (90, 90, 90)

def draw_kv(screen, font, x, y, label, value,
            label_color=TEXT_MUTED, value_color=TEXT_MAIN,
            line_gap=18):
    label_surf = font.render(label, True, label_color)
    value_surf = font.render(value, True, value_color)
    screen.blit(label_surf, (x, y))
    screen.blit(value_surf, (x, y + line_gap))

def draw_panel(screen, font, game, x0, w, h, skip_button=None):
    # panel background (mint green)
    panel = pygame.Rect(x0, 0, w, h)
    pygame.draw.rect(screen, PANEL_GREEN, panel)

    # inner dark "card" container
    pad = 14
    card = pygame.Rect(panel.x + pad, panel.y + pad, panel.w - 2*pad, panel.h - 2*pad)
    pygame.draw.rect(screen, CARD_BG, card, border_radius=14)
    pygame.draw.rect(screen, (0, 0, 0), card, 2, border_radius=14)

    # accent strip at top
    accent = pygame.Rect(card.x, card.y, card.w, 5)
    pygame.draw.rect(screen, ACCENT_GREEN, accent, border_radius=14)

    player = game.get_current_player()

    # --- layout metrics ---
    left_x = card.x + 14
    y = card.y + 18

    # Title
    title = font.render("MOVEMENT", True, ACCENT_GREEN)
    screen.blit(title, (left_x, y))
    y += 28

    # Divider
    pygame.draw.line(screen, DIVIDER, (card.x + 10, y), (card.right - 10, y), 2)
    y += 14

    # Row 1
    draw_kv(screen, font, left_x,  y, "PLAYER", player.color)
    
    y += 46

    # Row 2
    draw_kv(screen, font, left_x,  y, "MOVES LEFT", str(player.movements_left))

    # If you want, show something else on the right (optional)
    # draw_kv(screen, font, right_x, y, "TURN", str(player.turn_num))
    y += 46

    # Optional button placed nicely near bottom inside the card
    if skip_button is not None:
        btn_margin = 14
        btn_w = card.w - 2*btn_margin
        btn_h = 44
        btn_x = card.x + btn_margin
        btn_y = card.bottom - btn_margin - btn_h - 300

        skip_button.rect.topleft = (btn_x, btn_y)
        skip_button.rect.size = (btn_w, btn_h)
        skip_button.radius = 12  # if your Button supports it
        skip_button.draw(screen)

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
            text="Skip Movement",
            font=self.hud_font,
            bg_color=(200, 200, 200)
            )
        self.last_clicked = None

    """
        Handles the different events that can happen in the Movement phase
        (1) When player selects one of their pieces, 
            the board highlights legal spaces to move to
        (2) When player selects one of these highlighted places, move the piece there
        (3) Player only gets 3 moves or can click the 'Skip' button to move
            to the attack phase
        (4) Player can only move their own pieces once and cannot move opponents pieces,
            both events will cause a red error highlight to appear
    """
    def handle_event(self, event, game):

        if self.skip_button.is_clicked(event):
            return Screen.ATTACK

        if event.type == pygame.MOUSEBUTTONDOWN:

            sq = get_square_from_mouse(event.pos, 0, 0)
            if sq is None:
                return Screen.MOVEMENT
            row, col = sq

            # first time clicked, a piece is selected, highlight where it can move
            if not self.selected:
                piece = game.board.get_piece( (row, col) )

                if piece != None:

                    self.last_clicked = piece

                    # piece must belong to curr player and can only move once a turn
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

            # second time clicked, player chooses one of the highlighted spaces and move piece there
            else:
                if (game.board.get_piece((row, col)) == None):
                    if ((row, col) in self.pos_moves):

                        game.board.move_piece(self.curr_piece,(row, col))

                        new_piece = game.board.get_piece((row, col))
                        curr_player = game.get_current_player()

                        # promote piece if made it to the end of the board
                        if (curr_player.color == "White") and (row == 0):
                            new_piece.promote()
                        elif (curr_player.color == "Black") and (row == 7):
                            new_piece.promote()

                        self.pieces_moved.append(new_piece)
                        curr_player.use_move()
                else:
                    self.last_clicked = game.board.get_piece((row, col))

                self.selected = False
                self.curr_piece = None
                self.pos_moves = []

        return Screen.MOVEMENT

    """
        Draws the Movement screen
        Creates an 8x8 tile chess board with the current pieces + highlighted tiles on it
        Creates a sidebar with information about the phase (curr player, moves left, ect.)
    """
    def draw(self, screen, game):

        # error highlight only lasts 0.5 seconds
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

        draw_highlights(screen, self.pos_moves, (255, 200, 0), board_x, board_y)

        # Red overlay for pieces that already attacked
        for piece in self.pieces_moved:
            overlay = pygame.Surface((TILE, TILE), pygame.SRCALPHA)
            overlay.fill((255, 0, 0, 100))  # semi-transparent red
            inner_x = board_x + piece.col * TILE
            inner_y = board_y + piece.row * TILE
            screen.blit(overlay, (inner_x, inner_y))

        if self.error:
            draw_error(screen, self.err_loc, board_x, board_y)
        draw_pieces(screen, game.board.grid, self.font, board_x, board_y)
        draw_panel(screen, self.hud_font, game, panel_x, panel_w, panel_h)
        self.skip_button.draw(screen)

        if self.last_clicked != None:
            draw_stats(screen, self.hud_font, self.last_clicked, panel_x + 14)

        if self.curr_piece != None:
            draw_borders(screen, self.curr_piece, (0, 100, 255), board_x, board_y)
               

    """
        Sets up the Movement phase on entering
        Resets the amount of moves + clears pieces moved
    """
    def on_enter(self, screen, game):

        game.get_current_player().start_turn()
        self.pieces_moved = []

    def on_exit(self, screen, game):
        self.last_clicked = None
        return None
    
    def update(self, screen, game):

        if (not game.get_current_player().can_move()):
            return Screen.ATTACK
        
        return Screen.MOVEMENT