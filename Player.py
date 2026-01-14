from Deck import Deck
from Hand import Hand
from BonusStats import BonusStats

class Player:
    MAX_MOVES = 4
    MAX_ATTACKS = 4
    MAX_DISCARDS = 2

    def __init__(self, color):
        self.color = color
        self.deck = Deck()
        self.hand = Hand(self.deck.draw(7))
        self.start_turn()
        self.my_pieces = []
        self.poker_hand = None
        self.chips = 0
        self.bonus_stats = BonusStats()

    def start_turn(self):
        self.movements_left = self.MAX_MOVES
        self.attacks_left = self.MAX_ATTACKS
        self.discards_left = self.MAX_DISCARDS

    def can_move(self):
        return self.movements_left > 0

    def can_attack(self):
        return self.attacks_left > 0
    
    def can_discard(self):
        return self.discards_left > 0

    def use_move(self):
        if not self.can_move():
            raise RuntimeError("No moves left")
        self.movements_left -= 1

    def use_attack(self):
        if not self.can_attack():
            raise RuntimeError("No attacks left")
        self.attacks_left -= 1

    def use_discard(self):
        if not self.can_discard():
            raise RuntimeError("No discards left")
        self.discards_left -= 1
    
    def print_pieces(self):
        for piece in self.my_pieces:
            print(f"{piece.type.name} at ({piece.row}, {piece.col})")

        