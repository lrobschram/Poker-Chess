import pygame
from Screens import Screen
from ui import Button, ROWS, COLS, TILE, draw_board, draw_error, draw_highlights, draw_pieces, get_square_from_mouse
from HandEvaluator import HandRank, add_bonus, chip_counter
from Pieces import Piece, PieceType




HAND_TO_PIECE = {
    HandRank.HIGH_CARD:     PieceType.WARRIOR,
    HandRank.PAIR:      PieceType.ARCHER,
    HandRank.TWO_PAIR:      PieceType.KNIGHT,
    HandRank.THREE_KIND:    PieceType.WIZARD,
    HandRank.STRAIGHT:      PieceType.CATAPULT,
    HandRank.FLUSH:         PieceType.HEALER,
    HandRank.FULL_HOUSE:    PieceType.DIREWOLF,
    HandRank.FOUR_KIND:     PieceType.JUGGERNAUT,
    HandRank.STRAIGHT_FLUSH: PieceType.QUEEN,
}

def calc_piece(hand_rank, player):

    piece_type = HAND_TO_PIECE.get(hand_rank)
    return Piece(piece_type, player.color)

def add_bonus_piece(piece, pieceBonus):
    if(pieceBonus == "commonUnit"):
        piece.addBonusHealth()
    elif(pieceBonus == "strongUnit"):
        piece.addBonusDamage()
    elif(pieceBonus == "royalUnit"):
        piece.addBonusDamage()
        piece.addBonusHealth()
    piece.bonus = pieceBonus
    



def draw_panel(screen, font, game, piece, x0, w, h):
    # panel background
    pygame.draw.rect(screen, (220, 220, 255), pygame.Rect(x0, 0, w, h))

    player = game.get_current_player()

    if piece != None:
        piece_text = piece.type.name.replace("_", " ").title()
        bonus_text = f"{piece.bonus}"
    else:
        piece_text = "Skipped"
        bonus_text = None

    lines = [
        f"Phase: Placement",
        f"Player: {player.color}",
        f"Piece created: {piece_text}", 
    ]

    if bonus_text != None:
        lines.append(bonus_text)

    y = 20
    for line in lines:
        text = font.render(line, True, (0, 0, 0))
        screen.blit(text, (x0 + 15, y))
        y += 35

class PlacementScreen:

    def __init__(self):
        self.font = pygame.font.SysFont("helvetica", 35)
        self.hud_font = pygame.font.SysFont("helvetica", 16)
        self.pos_spaces = []
        self.curr_piece = None
        self.error = False
        self.err_loc = None
        self.error_start_time = 0
        self.ERROR_DURATION = 500  # milliseconds (0.5 seconds)
        self.skip_button = Button(
            rect=(COLS*TILE + 20, 200, 160, 40),  # sidebar position
            text="Skip to Movement",
            font=self.hud_font,
            bg_color=(200, 200, 200)
            )
        
    def handle_event(self, event, game):

        player = game.get_current_player()
        
        if self.skip_button.is_clicked(event) or self.curr_piece == None:
            return Screen.MOVEMENT
        
        if event.type == pygame.MOUSEBUTTONDOWN:


            sq = get_square_from_mouse(event.pos, 0, 0)

            if sq in self.pos_spaces:
                game.board.place_piece(self.curr_piece, sq)
                player.my_pieces.append(self.curr_piece)

                return Screen.MOVEMENT

        
        return Screen.PLACEMENT
    
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
        draw_highlights(screen, self.pos_spaces, (0, 100, 255), board_x, board_y)

        if self.error:
            draw_error(screen, self.err_loc, board_x, board_y)
        draw_pieces(screen, game.board.grid, self.font, board_x, board_y)
        draw_panel(screen, self.hud_font, game, self.curr_piece, panel_x, panel_w, panel_h)
        self.skip_button.draw(screen)


    def on_enter(self, screen, game):

         # Initialize placement squares
        self.pos_spaces = []

        player = game.get_current_player()

        if player.poker_hand != None:
            piece = calc_piece(player.poker_hand, player)
            self.curr_piece = piece
            
            #calculate chips and add bonus 
            pieceBonusType = add_bonus(player.chips)
            add_bonus_piece(piece, pieceBonusType)
            

            if player.color == "Black":
                rows = [0, 1]
            else:  # White
                rows = [ROWS - 2, ROWS - 1]

            for r in rows:
                for c in range(COLS):
                    if game.board.get_piece((r, c)) is None:
                        self.pos_spaces.append((r, c))

        return None
    

    def on_exit(self, screen, game):
        self.curr_piece = None
        game.get_current_player().chips = 0
        return None