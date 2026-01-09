import pygame
from Screens import Screen
from ui import Button, Card_ui
from Deck import Deck
from Card import Card, Rank, Suit
from HandEvaluator import evaluate_hand

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


def draw_bottom_pannel(screen, font, game, hand_rank):
    bottom_y = 350
    bottom = pygame.Rect(0, bottom_y, screen.get_width(), screen.get_height() - bottom_y)
    pygame.draw.rect(screen, (255,255,255), bottom)

    player = game.get_current_player()
    lines = [
        f"Phase: POKER",
        f"Player: {player.color}",
        f"Discards left: {player.discards_left}", 
    ]

    x = 35
    for line in lines:
        text = font.render(line, True, (0, 0, 0))
        screen.blit(text, (bottom.x + x, bottom.y + 50))
        x += 150

    rank_text = font.render(f"Current selected poker hand: {hand_rank}", True, (0, 0, 0))
    screen.blit(rank_text, (bottom.x + 35, bottom.y + 100))

class PokerScreen:

    def __init__(self):
        self.font = pygame.font.SysFont("dejavusans", 35)
        self.hud_font = pygame.font.SysFont("dejavusans", 18)
        self.selected = False
        self.cards_selected = []
        self.cards_displayed = []
        self.base_y = 150
        self.selected_y = 110
        self.discard_enabled_color = (200, 200, 200)
        self.discard_disabled_color = (150, 150, 150)
        self.discard_button = Button(
            rect=(550, 400, 160, 40),  # sidebar position
            text="Discard Hand",
            font=self.hud_font,
            bg_color=self.discard_enabled_color
            )
        self.play_button = Button(
            rect=(550, 460, 160, 40),  # sidebar position
            text="Play Hand",
            font=self.hud_font,
            bg_color=(200, 200, 200)
            )


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


    def discard(self, game):
        player = game.get_current_player()
        indicies_to_dis = []

        for card_ui in self.cards_selected:
            indicies_to_dis.append(player.hand.cards.index(card_ui.card))

        player.hand.discard(indicies_to_dis)
        refill_to_seven(player)
        player.use_discard()

        self.display_cards(game)


    def handle_event(self, event, game):
        
        if self.discard_button.is_clicked(event):
            if (len(self.cards_selected) > 0) and (game.get_current_player().can_discard()):
                self.discard(game)

        if event.type == pygame.MOUSEBUTTONDOWN:
            for card_ui in self.cards_displayed:
                if card_ui.is_clicked(event):
                    self.toggle_card(card_ui)
                    break  # only toggle one card per click

        return Screen.POKER
    

    def draw(self, screen, game):
        screen.fill((100, 100, 100))

        player = game.get_current_player()

        if (len(self.cards_selected) > 0):
            hand_rank = evaluate_hand([card_ui.card for card_ui in self.cards_selected])
            curr_poker_hand = hand_rank.name
        else:
            curr_poker_hand = "No Cards Selected"
        
        draw_bottom_pannel(screen, self.hud_font, game, curr_poker_hand)

        if player.can_discard():
            self.discard_button.bg_color = self.discard_enabled_color
        else:
            self.discard_button.bg_color = self.discard_disabled_color

        self.discard_button.draw(screen)
        self.play_button.draw(screen)

        for card_ui in self.cards_displayed:
            card_ui.draw(screen)
        

    def on_enter(self, screen, game):
        refill_to_seven(game.get_current_player())
        self.display_cards(game)
        return None
    

    def on_exit(self, screen, game):
        return None