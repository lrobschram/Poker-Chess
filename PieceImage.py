import pygame
from Pieces import Piece  # For type hints (ensure this import is here)

class PieceImage:
    def __init__(self, piece: Piece, sprite_manager):
        self.piece = piece
        self.sprite_manager = sprite_manager
        self.image = self.sprite_manager.get_sprite(piece.type, piece.owner)  # Correct: local 'piece'
        # TODO: Add self.overlay for bonuses (e.g., green border) later

    def draw(self, screen, board_x=0, board_y=0):
        """Draw the piece image centered in its board tile."""
        if not self.piece:  # Skip if piece is dead/removed
            return
        
        tile_size = 70  # From your ui.py TILE
        img_x = board_x + self.piece.col * tile_size + (tile_size - self.image.get_width()) // 2
        img_y = board_y + self.piece.row * tile_size + (tile_size - self.image.get_height()) // 2
        screen.blit(self.image, (img_x, img_y))
        # TODO: Blit overlay here if bonus applied

    def update(self):
        """Refresh image (e.g., after promote() or bonus change)."""
        # FIXED: Use self.piece.owner (instance attr), not 'piece' (undefined local)
        self.image = self.sprite_manager.get_sprite(self.piece.type, self.piece.owner)