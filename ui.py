import pygame
from Card import Suit
import re

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


            tile_rect = pygame.Rect(x0 + c * TILE, y0 + r * TILE, TILE, TILE)

            # Get image safely (fallback to None if missing)
            image_obj = getattr(piece, 'image_obj', None)


            if image_obj is not None:
                # FIXED: Clear tile with background color FIRST (erases any old text)
                tile_color = (180, 180, 180) if (r + c) % 2 == 0 else (120, 120, 120)  # Match your draw_board colors
                pygame.draw.rect(screen, tile_color, tile_rect)
                
                # Draw the image on top (covers everything)
                image_obj.draw(screen, x0, y0)
            else:
                # TEXT FALLBACK: Only if no image (draw on clean tile)
                # Re-draw tile background for consistency
                tile_color = (180, 180, 180) if (r + c) % 2 == 0 else (120, 120, 120)
                pygame.draw.rect(screen, tile_color, tile_rect)
                
                text = font.render(piece.piece_initial(), True, (0, 0, 0))
                text_rect = text.get_rect(center=tile_rect.center)  # Center text better
                screen.blit(text, text_rect)


# draws the highlights as a border around the given tiles
def draw_borders(screen, pos, color, x0=0, y0=0):

    rect = pygame.Rect(x0 + pos[1]*TILE, y0 + pos[0]*TILE, TILE, TILE)
    pygame.draw.rect(screen, color, rect, 4)

# draws the highlights as little squares in the given tiles
def draw_highlights(screen, moves, color, x0=0, y0=0):
    HIGHLIGHT_SIZE = TILE // 3  # adjust size here

    for r, c in moves:
        inner_x = x0 + c*TILE + (TILE - HIGHLIGHT_SIZE) // 2
        inner_y = y0 + r*TILE + (TILE - HIGHLIGHT_SIZE) // 2

        inner_rect = pygame.Rect(inner_x, inner_y, HIGHLIGHT_SIZE, HIGHLIGHT_SIZE)
        pygame.draw.rect(screen, color, inner_rect)


def draw_error(screen, pos, x0=0, y0=0):
    rect = pygame.Rect(x0 + pos[1]*TILE, y0 + pos[0]*TILE, TILE, TILE)
    pygame.draw.rect(screen, (255, 0, 0), rect, 4)

def pretty_bonus(bonus: str) -> str:
    # "healthyUnit" -> "Healthy Unit"
    return re.sub(r"([a-z])([A-Z])", r"\1 \2", bonus).title()

def draw_stats(screen, font, piece, x0):
    bonus_text = pretty_bonus(piece.bonus)
    lines = [
        f"Piece Clicked: ",
        f"{piece.type.name}",
        f"{piece.owner}",
        f"{piece.attack} att",
        f"{piece.health} hp",
        f"{bonus_text}"
            ]
    
    y = 275
    for line in lines:
        text = font.render(line, True, (0, 0, 0))
        screen.blit(text, (x0 + 15, y))
        y += 25
    
    bar_width = 160
    bar_height = 14

    bar_x = x0 + 15
    bar_y = y + 10  # just below text

    ratio = max(0, min(1, piece.health / piece.max_health))

    green_width = int(bar_width * ratio)
    red_width = bar_width - green_width

    # Green = current HP
    pygame.draw.rect(
        screen,
        (0, 180, 0),
        (bar_x, bar_y, green_width, bar_height),
        border_radius=4
    )

    # Red = missing HP
    pygame.draw.rect(
        screen,
        (200, 0, 0),
        (bar_x + green_width, bar_y, red_width, bar_height)
    )

    # Outline
    pygame.draw.rect(
        screen,
        (0, 0, 0),
        (bar_x, bar_y, bar_width, bar_height),
        2,
        border_radius=4
    )

class Button:
    def __init__(self, rect, text, font, bg_color, text_color=(20,20,20), radius=10):
        self.rect = pygame.Rect(rect)
        self.text = text
        self.font = font
        self.bg_color = bg_color
        self.text_color = text_color
        self.radius = radius

        self.enabled = True
        self._pressed = False

        # optional: override these per-button if you want
        self.hover_color = None
        self.pressed_color = None
        self.disabled_color = (110, 110, 110)
        self.disabled_text_color = (170, 170, 170)

    def _shade(self, color, amt):
        # amt > 0 -> lighten, amt < 0 -> darken
        r, g, b = color
        def clamp(x): return max(0, min(255, x))
        return (clamp(r + amt), clamp(g + amt), clamp(b + amt))

    def draw(self, screen):
        mouse = pygame.mouse.get_pos()
        hovered = self.rect.collidepoint(mouse)

        # pick current colors
        if not self.enabled:
            bg = self.disabled_color
            fg = self.disabled_text_color
        else:
            bg = self.bg_color
            fg = self.text_color
            if self.pressed_color is None:
                pressed_bg = self._shade(bg, -25)
            else:
                pressed_bg = self.pressed_color

            if self.hover_color is None:
                hover_bg = self._shade(bg, +12)
            else:
                hover_bg = self.hover_color

            if self._pressed and hovered:
                bg = pressed_bg
            elif hovered:
                bg = hover_bg

        # subtle shadow
        shadow = self.rect.move(0, 3)
        pygame.draw.rect(screen, (0,0,0), shadow, border_radius=self.radius)

        # button body
        pygame.draw.rect(screen, bg, self.rect, border_radius=self.radius)

        # border
        border_col = (0,0,0) if self.enabled else (70,70,70)
        pygame.draw.rect(screen, border_col, self.rect, 2, border_radius=self.radius)

        # text (centered)
        text_surf = self.font.render(self.text, True, fg)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)

    def is_clicked(self, event):
        if not self.enabled:
            return False

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self._pressed = True

        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            was_pressed = self._pressed
            self._pressed = False
            if was_pressed and self.rect.collidepoint(event.pos):
                return True

        return False
    
class Card_ui:
    def __init__(self, pos, size, card_object, font):
        self.rect = pygame.Rect(pos[0], pos[1], size[0], size[1])
        self.card_object = card_object
        self.font = font
        self.card = card_object
    
    def draw(self, screen):
        mouse_pos = pygame.mouse.get_pos()
        hovered = self.rect.collidepoint(mouse_pos)

        # Card background
        pygame.draw.rect(screen, (255,255,255), self.rect, border_radius=8)

        # Card border, highlight if mouse hovers over card
        border_color = (0,0,0) if not hovered else (60, 120, 255)
        pygame.draw.rect(screen, border_color, self.rect, 2, border_radius=8)

        # Determine text color by suit
        if self.card_object.suit == Suit.HEARTS:
            text_color = (255, 0, 0)
        elif self.card_object.suit == Suit.DIAMONDS:
            text_color = (255, 165, 0)
        elif self.card_object.suit == Suit.CLUBS:
            text_color = (0, 0, 255)
        else: 
            text_color = (0, 0, 0)

        text_surf = self.font.render(str(self.card_object), True, text_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)

    def is_clicked(self, event):
        return (
            event.type == pygame.MOUSEBUTTONDOWN
            and self.rect.collidepoint(event.pos)
        ) 
    
    def move_to_y(self, y):
        self.rect.y = y
