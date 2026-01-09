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
        self.cards_displayed = []
        self.base_y = 150
        self.selected_y = 110


    def toggle_card(self, card_ui):
        if card_ui in self.cards_selected:
            # deselect
            self.cards_selected.remove(card_ui)
            card_ui.move_to_y(self.base_y)
        else:
            # select (only if room)
            if len(self.cards_selected) >= 5:
                return
            self.cards_selected.append(card_ui)
            card_ui.move_to_y(self.selected_y)


    def display_cards(self, game):
        self.cards_displayed = []
        self.cards_selected = []  # reset selection when re-displaying

        card_offset = 0
        for card in game.get_current_player().hand.cards:
            ui_card = Card_ui((30 + card_offset, 150), card, self.font)
            self.cards_displayed.append(ui_card)
            card_offset += 100


    def handle_event(self, event, game):
        if event.type == pygame.MOUSEBUTTONDOWN:
            for card_ui in self.cards_displayed:
                if card_ui.is_clicked(event):
                    self.toggle_card(card_ui)
                    break  # only toggle one card per click

        return Screen.POKER
    

    def draw(self, screen, game):
        screen.fill((100, 100, 100))
        for card_ui in self.cards_displayed:
            card_ui.draw(screen)
        

    def on_enter(self, screen, game):
        refill_to_seven(game.get_current_player())
        self.display_cards(game)
        return None
    

    def on_exit(self, screen, game):
        return None