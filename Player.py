from Deck import Deck
from Hand import Hand
import MovementRules
import AttackRules

class Player:
    MAX_MOVES = 3
    MAX_ATTACKS = 2

    def __init__(self, color):
        self.color = color
        self.deck = Deck()
        self.hand = Hand(self.deck.draw(7))
        self.start_turn()

    def start_turn(self):
        self.movements_left = self.MAX_MOVES
        self.attacks_left = self.MAX_ATTACKS

    def can_move(self):
        return self.movements_left > 0

    def can_attack(self):
        return self.attacks_left > 0

    def use_move(self):
        if not self.can_move():
            raise RuntimeError("No moves left")
        self.movements_left -= 1

    def use_attack(self):
        if not self.can_attack():
            raise RuntimeError("No attacks left")
        self.attacks_left -= 1

        