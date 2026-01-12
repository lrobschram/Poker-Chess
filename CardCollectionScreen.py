import pygame
from Screens import Screen
from ui import Button, Card_ui
from Deck import Deck
from HandEvaluator import evaluate_hand, chip_counter
from Card import Rank, Suit

class CardCollectionScreen:
    def __init__(self):
        self.font = pygame.font.SysFont("dejavusans", 35)
        self.hud_font = pygame.font.SysFont("dejavusans", 20)
        self.card_size = (50, 70)
        self.back_button = Button(
            rect=(20, 30, 160, 40),  
            text="Back",
            font=self.hud_font,
            bg_color=(200, 200, 200)
            )
        self.cards_displayed = []
        
    def display_cards(self, game):
        player = game.get_current_player()

        self.cards_displayed = []

        player.deck.sort_by_suit()

        x_offset = 0
        y_offset = 0
        card_count = 0
        for card in player.deck.cards:

            ui_card = Card_ui((20 + x_offset, 90 + y_offset), self.card_size, card, self.hud_font)

            self.cards_displayed.append(ui_card)
            x_offset += 60
            card_count += 1

            if card_count % 12 == 0:
                x_offset = 0
                y_offset += 105

    def handle_event(self, event, game):

        if self.back_button.is_clicked(event):
            return Screen.POKER

        return Screen.CARD_COLLECTION
    
    def draw(self, screen, game):
        screen.fill((100, 100, 100))

        title_text = self.font.render(f"Cards Left in Deck", True, (0, 0, 0))
        screen.blit(title_text, (235, 30))

        self.back_button.draw(screen)

        for card_ui in self.cards_displayed:
            card_ui.draw(screen)

    def on_enter(self, screen, game):
        self.display_cards(game)
    

    def on_exit(self, screen, game):
        player = game.get_current_player()
        player.deck.shuffle()