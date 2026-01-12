import pygame
from Screens import Screen
from ui import Button, Card_ui
from Deck import Deck
from HandEvaluator import evaluate_hand, chip_counter
from Card import Rank, Suit

class CardCollectionScreen:
    def __init__(self):
        self.font = pygame.font.SysFont("dejavusans", 35)
        self.hud_font = pygame.font.SysFont("dejavusans", 18)
        self.card_size = (40, 75)
        self.back_button = Button(
            rect=(50, 100, 160, 40),  
            text="Back",
            font=self.hud_font,
            bg_color=(200, 200, 200)
            )

    def handle_event(self, event, game):
        return Screen.CARD_COLLECTION
    
    def draw(self, screen, game):
        screen.fill((100, 100, 100))

        self.back_button.draw(screen)

    def on_enter(self, screen, game):
        return None
    

    def on_exit(self, screen, game):
        return None