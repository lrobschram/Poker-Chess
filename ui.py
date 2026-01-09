import pygame
from Card import Suit

class Button:
    def __init__(self, rect, text, font, bg_color, text_color=(0,0,0)):
        self.rect = pygame.Rect(rect)
        self.text = text
        self.font = font
        self.bg_color = bg_color
        self.text_color = text_color

    def draw(self, screen):
        pygame.draw.rect(screen, self.bg_color, self.rect, border_radius=6)

        text_surf = self.font.render(self.text, True, self.text_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)

    def is_clicked(self, event):
        return (
            event.type == pygame.MOUSEBUTTONDOWN
            and self.rect.collidepoint(event.pos)
        )
    
class Card_ui:
    def __init__(self, pos, card_object, font):
        self.rect = pygame.Rect(pos[0], pos[1], 80, 120)
        self.card_object = card_object
        self.font = font
    
    def draw(self, screen):
        mouse_pos = pygame.mouse.get_pos()
        hovered = self.rect.collidepoint(mouse_pos)

        # Card background
        pygame.draw.rect(screen, (255,255,255), self.rect, border_radius=8)

        # Card border, highlight if mouse hovers over card
        border_color = (0,0,0) if not hovered else (60, 120, 255)
        pygame.draw.rect(screen, border_color, self.rect, 2, border_radius=8)

        # Determine text color by suit
        if self.card_object.suit in (Suit.DIAMONDS, Suit.HEARTS):
            text_color = (255, 0, 0)
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
