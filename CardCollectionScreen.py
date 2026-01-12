import pygame
from Screens import Screen
from ui import Button, Card_ui
from Deck import Deck
from HandEvaluator import evaluate_hand, chip_counter
from Card import Rank, Suit

def get_color(suit):
        
    # Determine text color by suit
        if suit == Suit.HEARTS:
            return (255, 0, 0)
        elif suit == Suit.DIAMONDS:
            return (255, 165, 0)
        elif suit == Suit.CLUBS:
            return (0, 0, 255)
        else: 
            return (0, 0, 0)

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
        
    def display_cards(self, game, screen):
        player = game.get_current_player()

        player.deck.sort_by_suit()

        x_offset = 0
        y_offset = 0
        curr_suit = player.deck.cards[0].suit
        suit_counter = 0

        for card in player.deck.cards:

            if card.suit != curr_suit:

                if suit_counter != 13:
                    text_color = get_color(curr_suit)
                    suit_amt = self.hud_font.render(f"{suit_counter}{curr_suit.value} left", True, text_color)
                    screen.blit(suit_amt, (15 + x_offset, 110 + y_offset))

                x_offset = 0
                y_offset += 105
                curr_suit = card.suit
                suit_counter = 0

            ui_card = Card_ui((10 + x_offset, 90 + y_offset), self.card_size, card, self.hud_font)

            ui_card.draw(screen)

            x_offset += 55
            suit_counter += 1

        if suit_counter != 13:
                    text_color = get_color(curr_suit)
                    suit_amt = self.hud_font.render(f"{suit_counter}{curr_suit.value} left", True, text_color)
                    screen.blit(suit_amt, (15 + x_offset, 110 + y_offset))


    def handle_event(self, event, game):

        if self.back_button.is_clicked(event):
            return Screen.POKER

        return Screen.CARD_COLLECTION
    
    def draw(self, screen, game):
        screen.fill((100, 100, 100))

        player = game.get_current_player()

        title_text = self.font.render(f"Cards Left in Deck:  {len(player.deck.cards)} / 52", True, (0, 0, 0))
        screen.blit(title_text, (235, 30))

        self.back_button.draw(screen)

        self.display_cards(game, screen)

    def on_enter(self, screen, game):
        return None
    

    def on_exit(self, screen, game):
        player = game.get_current_player()
        player.deck.shuffle()

    def update(self, screen, game):
        return Screen.CARD_COLLECTION