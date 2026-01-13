import pygame
from Screens import Screen
from ui import Button, Card_ui
from Deck import Deck
from HandEvaluator import evaluate_hand, chip_counter
from Card import Rank, Suit


TABLE_GREEN = (35, 135, 100)   
PANEL_BG    = (18, 65, 50)   
TEXT_MAIN     = (225, 225, 220)
TEXT_LIGHT  = (210, 210, 205)
CARD_BG       = (55, 55, 55)
TEXT_MUTED    = (170, 170, 170)
ACCENT_GOLD   = (210, 180, 90)

BTTN_PRIMARY = (210, 180, 90)     
BTTN_PRIMARY_TEXT = (20, 20, 20)
BTTN_SECONDARY = (200, 200, 200)
BTTN_SECONDARY_TEXT = (25, 25, 25)

BTN_W = 190
BTN_H = 44
BTN_GAP = 12

RIGHT_PAD = 20
STACK_Y = 290   # height area right above your bottom panel


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


def draw_kv(screen, font, x, y, label, value, label_color, value_color):
    # label on top, value below (nice UI hierarchy)
    label_surf = font.render(label, True, label_color)
    value_surf = font.render(value, True, value_color)
    screen.blit(label_surf, (x, y))
    screen.blit(value_surf, (x, y + 18))  # spacing depends on font size

def draw_bottom_pannel(screen, font, game, hand_rank, chips, discard_btn, play_btn):
    bottom_y = 350
    bottom = pygame.Rect(0, bottom_y, screen.get_width(), screen.get_height() - bottom_y)

    pygame.draw.rect(screen, PANEL_BG, bottom)

    pad = 18
    card = pygame.Rect(bottom.x + pad, bottom.y + pad, bottom.width - 2*pad, bottom.height - 2*pad)
    pygame.draw.rect(screen, CARD_BG, card, border_radius=12)
    pygame.draw.rect(screen, (0, 0, 0), card, 2, border_radius=12)

    accent = pygame.Rect(card.x, card.y, card.width, 5)
    pygame.draw.rect(screen, ACCENT_GOLD, accent, border_radius=12)

    player = game.get_current_player()

    # ---------- Right-side button stack INSIDE the bottom panel ----------
    BTN_W, BTN_H = 190, 44
    BTN_GAP = 12
    right_pad = 18

    stack_x = card.right - right_pad - BTN_W
    # vertically center stack in the card
    stack_total_h = BTN_H*2 + BTN_GAP
    stack_y = card.y + (card.height - stack_total_h)//2

    discard_btn.rect.topleft = (stack_x, stack_y)
    play_btn.rect.topleft    = (stack_x, stack_y + BTN_H + BTN_GAP)

    # divider between info area and buttons
    divider_x = stack_x - 18
    pygame.draw.line(screen, (80, 80, 80), (divider_x, card.y + 14), (divider_x, card.bottom - 14), 2)

    # ---------- Left info area ----------
    info_x = card.x + 18
    info_w = divider_x - info_x - 18

    # row 1: phase + player (since discards moved out)
    draw_kv(screen, font, info_x, card.y + 18, "PHASE", "POKER", TEXT_MUTED, TEXT_MAIN)
    draw_kv(screen, font, info_x + info_w//2, card.y + 18, "PLAYER", player.color, TEXT_MUTED, TEXT_MAIN)

    # horizontal divider
    pygame.draw.line(screen, (80, 80, 80), (card.x + 14, card.y + 62), (divider_x - 14, card.y + 62), 2)

    # row 2: poker hand + chip count next to it
    row2_y = card.y + 75
    hand_label = font.render("POKER HAND", True, TEXT_MUTED)
    screen.blit(hand_label, (info_x, row2_y))

    hand_value = font.render(str(hand_rank), True, ACCENT_GOLD)
    screen.blit(hand_value, (info_x, row2_y + 18))

    # chips placed right of hand value
    chip_x = info_x + info_w//2
    chip_label = font.render("CHIPS", True, TEXT_MUTED)
    screen.blit(chip_label, (chip_x, row2_y))

    chip_value = font.render(str(chips), True, TEXT_MAIN)
    screen.blit(chip_value, (chip_x, row2_y + 18))

    # chip icon dot
    pygame.draw.circle(screen, ACCENT_GOLD, (chip_x - 14, row2_y + 36), 6)
    pygame.draw.circle(screen, (0, 0, 0), (chip_x - 14, row2_y + 36), 6, 2)

    # finally draw buttons (so they appear on top)
    discard_btn.draw(screen)
    play_btn.draw(screen)


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
        self.cards_to_count = []
        self.sort = Rank
        self.button_enabled_color = (200, 200, 200)
        self.button_disabled_color = (150, 150, 150)

        
        self.discard_button = Button(
            rect=(20, 290, 160, 40),  
            text="Discard Hand",
            font=self.hud_font,
            bg_color=self.button_enabled_color
            )
        
        self.play_button = Button(
            rect=(555, 290, 160, 44),
            text="Play Hand",
            font=self.hud_font,
            bg_color=BTTN_PRIMARY,
            text_color=BTTN_PRIMARY_TEXT,
            radius=12
            )

        self.sort_button = Button(
            rect=(555, 30, 190, 44), 
            text="Play Hand",
            font=self.hud_font,
            bg_color=self.button_enabled_color,
            radius=12
            )

        self.full_deck_button = Button(
            rect=(20, 30, 190, 44),  
            text="Cards left in deck",
            font=self.hud_font,
            bg_color=(200, 200, 200),
            radius=12
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

            ui_card = Card_ui((40 + card_offset, self.base_y), self.card_size, card, self.font)


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

        if self.full_deck_button.is_clicked(event):
            return Screen.CARD_COLLECTION
        
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
                player.bonus_stats.record_play(player.chips)

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
        screen.fill(TABLE_GREEN)

        player = game.get_current_player()

        info = self.hud_font.render(f"Discards Left: {player.discards_left}", True, TEXT_LIGHT)
        screen.blit(info, (screen.get_width() - 20 - info.get_width(), 310))

        hand_rank = self.calc_poker_hand()
        if (hand_rank != None):
            curr_poker_hand = hand_rank.name.replace("_", " ").title()
        else:
            curr_poker_hand = "No Cards Selected"

        chips = chip_counter(self.cards_to_count)
        
        # grey out the discard button when none selected or out of discards
        self.discard_button.enabled = (player.can_discard() and len(self.cards_selected) > 0)

        # turn play into skip when no cards selected
        if len(self.cards_selected) > 0:
            self.play_button.text = "Play Hand"
        else:
            chips = 0
            self.play_button.text = "Skip Hand"

        draw_bottom_pannel(
            screen,
            self.hud_font,
            game,
            curr_poker_hand,
            chips,
            self.discard_button,
            self.play_button
        )

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
        refill_to_seven(player)
        self.display_cards(game)
    

    def on_exit(self, screen, game):
        return None

    def update(self, screen, game):
        return Screen.POKER