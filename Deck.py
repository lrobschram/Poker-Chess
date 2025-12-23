import random
from Card import Card, Suit, Rank


class Deck:
    def __init__(self):
        self.cards = [
            Card(rank, suit)
            for suit in Suit
            for rank in Rank
        ]
        self.shuffle()

    def shuffle(self):
        random.shuffle(self.cards)

    def draw(self, n=1):
        if n > len(self.cards):
            raise ValueError("Not enough cards left in deck")

        drawn = self.cards[:n]
        self.cards = self.cards[n:]
        return drawn

    def remaining(self):
        return len(self.cards)
