import pygame
from Screens import Screen
from ui import Button, Card_ui
from Deck import Deck
from Card import Card, Rank, Suit

def refill_deck(player):

    # create a new deck object and remove the current cards in hand
    player.deck = Deck()
    player.deck.remove_cards(player.hand.cards)


def refill_to_seven(player):

    if (player.hand.size() < 7):
        amt_needed = 7 - player.hand.size()

        try:
            new_cards = player.deck.draw(amt_needed)

        # refill the deck if there are not enough cards to draw
        except ValueError as e:
            refill_deck(player)
            new_cards = player.deck.draw(amt_needed)

        player.hand.add_cards(new_cards)

class PokerScreen:

    def __init__(self):
        self.font = pygame.font.SysFont("dejavusans", 35)
        self.hud_font = pygame.font.SysFont("dejavusans", 18)
        self.selected = False
        self.cards_selected = []


    def handle_event(self, event, game):
        return Screen.POKER
    

    def draw(self, screen, game):
        screen.fill((0, 0, 0))
        test_card = Card_ui((250, 250), Card(Rank.ACE, Suit.HEARTS), self.font)
        test_card.draw(screen)
    

    def on_enter(self, screen, game):
        refill_to_seven(game.get_current_player())
        return None
    

    def on_exit(self, screen, game):
        return None