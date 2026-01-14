import pygame
import os
from Pieces import PieceType  # Import your enum

class SpriteManager:
    def __init__(self, assets_folder="assets"):
        self.assets_folder = assets_folder
        self.sprites = {}  # Key: (PieceType, color) -> Surface
        self.load_all_sprites()

    def load_all_sprites(self):
        """Load all PNGs from assets/ into cache. Prints loaded files."""
        if not os.path.exists(self.assets_folder):
            print(f"Warning: {self.assets_folder} folder not found!")
            return
        
        loaded_count = 0
        for filename in os.listdir(self.assets_folder):
            if not filename.endswith('.png'):
                continue
            name_parts = filename[:-4].split('_')  # e.g., ['white', 'king']
            if len(name_parts) != 2:
                print(f"Skipping invalid filename: {filename} (expected: color_type.png)")
                continue
            color, type_name = name_parts
            try:
                piece_type = PieceType[type_name.upper()]  # e.g., 'KING'
                path = os.path.join(self.assets_folder, filename)
                surface = pygame.image.load(path).convert_alpha()  # PNG with transparency
                surface = pygame.transform.scale(surface, (60, 60))  # Scale to fit 70px TILE
                self.sprites[(piece_type, color.title())] = surface  # Store as 'White'/'Black'
                print(f"Loaded: {filename} -> {piece_type} ({color})")
                loaded_count += 1
            except (KeyError, pygame.error) as e:
                print(f"Failed to load {filename}: {e}")
        
        print(f"Total sprites loaded: {loaded_count}")

    def get_sprite(self, piece_type: PieceType, color: str) -> pygame.Surface:  # 'color' param is actually 'owner'
        """Get cached image or a fallback colored square."""
        key = (piece_type, color)  # CHANGED: 'color' here is now passed as piece.owner (e.g., "White")
        if key in self.sprites:
            return self.sprites[key]
        # Fallback: Simple colored rect (for missing images)
        fallback = pygame.Surface((60, 60)).convert_alpha()
        fallback_color = (240, 240, 240) if color == "White" else (50, 50, 50)
        pygame.draw.rect(fallback, fallback_color, (0, 0, 60, 60))
        # Add a '?' text for debug
        font = pygame.font.SysFont(None, 24)
        text = font.render("?", True, (0, 0, 0))
        fallback.blit(text, (25, 18))
        return fallback