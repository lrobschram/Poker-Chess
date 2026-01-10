import pygame
from Screens import Screen
from ui import Button, ROWS, COLS, TILE, draw_board, draw_error, draw_highlights, draw_pieces, get_square_from_mouse, draw_stats


def draw_panel(screen, font, game, x0, w, h):
    # panel background
    pygame.draw.rect(screen, (220, 255, 220), pygame.Rect(x0, 0, w, h))

    player = game.get_current_player()
    lines = [
        f"Phase: Movement",
        f"Player: {player.color}",
        f"Moves left: {player.movements_left}", 
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
                self.pos_moves = []

        if (not game.get_current_player().can_move()):
            return Screen.ATTACK
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
            draw_stats(screen, self.hud_font, self.last_clicked, panel_x)
            
            

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