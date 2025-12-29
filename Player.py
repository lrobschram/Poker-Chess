from Deck import Deck
from Hand import Hand

class Player:

    def __init__(self, color):
        self.deck = Deck()
        self.hand = Hand(self.deck.draw(7))
        self.color = color