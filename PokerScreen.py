import pygame
from Screens import Screen
from ui import Button, Card_ui
from Deck import Deck
from HandEvaluator import evaluate_hand, chip_counter
from Card import Rank, Suit


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


def draw_bottom_pannel(screen, font, game, hand_rank, chips):
    
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

    rank_text = font.render(f"Poker Hand: {hand_rank}", True, (0, 0, 0))
    screen.blit(rank_text, (bottom.x + 35, bottom.y + 100))

    chip_text = font.render(f"Chip Count: {chips}", True, (0, 0, 0))
    screen.blit(chip_text, (bottom.x + 375 , bottom.y + 100))


class PokerScreen:

    def __init__(self):
        self.font = pygame.font.SysFont("dejavusans", 35)
        self.hud_font = pygame.font.SysFont("dejavusans", 18)
        self.selected = False
        self.cards_selected = []
        self.cards_displayed = []
        self.base_y = 150
        self.selected_y = 110
        self.card_size = (80, 120)
        self.button_enabled_color = (200, 200, 200)
        self.button_disabled_color = (150, 150, 150)
        self.discard_button = Button(
            rect=(550, 400, 160, 40),  
            text="Discard Hand",
            font=self.hud_font,
            bg_color=self.button_enabled_color
            )
        self.play_button = Button(
            rect=(550, 460, 160, 40), 
            text="Play Hand",
            font=self.hud_font,
            bg_color=self.button_enabled_color
            )
        self.sort = Rank
        self.sort_button = Button(
            rect=(100, 500, 160, 40), 
            text="Play Hand",
            font=self.hud_font,
            bg_color=self.button_enabled_color
            )
        self.cards_to_count = []
        self.full_deck_button = Button(
            rect=(20, 30, 160, 40),  
            text="Cards left in deck",
            font=self.hud_font,
            bg_color=(200, 200, 200)
            )


    def toggle_card(self, card_ui):
        card = card_ui.card

        if card in self.cards_selected:
            self.cards_selected.remove(card)
            card_ui.move_to_y(self.base_y)
        else:
            if len(self.cards_selected) >= 5:
                return
            self.cards_selected.append(card)
            card_ui.move_to_y(self.selected_y)


    def display_cards(self, game):
        player = game.get_current_player()

        # remember which Cards were selected
        selected_cards = set(self.cards_selected)

        self.cards_displayed = []

        if self.sort == Rank:
            player.hand.sort_by_rank()
        else:
            player.hand.sort_by_suit()

        card_offset = 0
        for card in player.hand.cards:

            ui_card = Card_ui((50 + card_offset, self.base_y), self.card_size, card, self.font)


            # re-apply selection
            if card in selected_cards:
                ui_card.move_to_y(self.selected_y)

            self.cards_displayed.append(ui_card)
            card_offset += 100


    def discard(self, game, card_ui_list):
        player = game.get_current_player()
        indicies_to_dis = []

        # takes indicies of selected cards and discards them
        for card in self.cards_selected:
            indicies_to_dis.append(player.hand.cards.index(card))

        player.hand.discard(indicies_to_dis)
        self.cards_selected = []
        refill_to_seven(player)

        self.display_cards(game)


    def calc_poker_hand(self):
        if (len(self.cards_selected) > 0):
            rank, cards_counted = evaluate_hand(self.cards_selected)
            self.cards_to_count = cards_counted
            return rank
        else:
            return None


    """
        Handles the different events that can happen in the Poker phase
        (1) Player can select up to 5 cards
        (2) Player can discard the selected cards up to 2 times
        (3) Player can play the selected cards, which discards rest of the cards as well
        (4) Player can skip Poker phase to keep their hand for next turn
    """
    def handle_event(self, event, game):

        player = game.get_current_player()
        
        # discard curr selected cards + use discard when discard button clicked 
        if self.discard_button.is_clicked(event):
            if (len(self.cards_selected) > 0) and (player.can_discard()):
                self.discard(game, self.cards_selected)
                player.use_discard()

        # calc poker hand and switch to placement screen when play button clicked
        if self.play_button.is_clicked(event):
            hand_rank = self.calc_poker_hand()
            player.poker_hand = hand_rank
            player.chips = chip_counter(self.cards_to_count)

            if len(self.cards_selected) > 0:
                self.discard(game, self.cards_displayed)

            return Screen.PLACEMENT
        
        if self.sort_button.is_clicked(event):
            if self.sort == Rank:
                self.sort = Suit
            else:
                self.sort = Rank
            
            self.display_cards(game)

        # toggle card when clicked on
        if event.type == pygame.MOUSEBUTTONDOWN:
            for card_ui in self.cards_displayed:
                if card_ui.is_clicked(event):
                    self.toggle_card(card_ui)
                    break  # only toggle one card per click

        return Screen.POKER
    
    """
        Draws the Poker screen
        Places cards in the center of the screen with selected cards raised
        Highlights the card when mouse hovers over it
        Creates a bottom pannel with player info and discard + play/skip buttons
    """
    def draw(self, screen, game):
        screen.fill((100, 100, 100))

        player = game.get_current_player()

        hand_rank = self.calc_poker_hand()
        if (hand_rank != None):
            curr_poker_hand = hand_rank.name.replace("_", " ").title()
        else:
            curr_poker_hand = "No Cards Selected"

        chips = chip_counter(self.cards_to_count)
        
        # grey out the discard button when none selected or out of discards
        if player.can_discard() and len(self.cards_selected) > 0:
            self.discard_button.bg_color = self.button_enabled_color
        else:
            self.discard_button.bg_color = self.button_disabled_color

        # turn play into skip when no cards selected
        if len(self.cards_selected) > 0:
            self.play_button.text = "Play"
        else:
            chips = 0
            self.play_button.text = "Skip"

        draw_bottom_pannel(screen, self.hud_font, game, curr_poker_hand, chips)
        self.discard_button.draw(screen)
        self.play_button.draw(screen)

        if self.sort == Rank:
            self.sort_button.text = "Sort by Suit"
        else:
            self.sort_button.text = "Sort by Rank"

        self.sort_button.draw(screen)

        self.full_deck_button.draw(screen)

        for card_ui in self.cards_displayed:
            card_ui.draw(screen)
        

    def on_enter(self, screen, game):
        player = game.get_current_player()
        player.start_turn()
        refill_to_seven(player)
        self.display_cards(game)
    

    def on_exit(self, screen, game):
        return None