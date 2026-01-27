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
    
    def print_deck(self):
        for i, card in enumerate(self.cards):
            print(f"{i}: {card}")
    
    def remove_cards(self, cards_to_remove):
        remove_set = {(c.rank, c.suit) for c in cards_to_remove}
        self.cards = [c for c in self.cards if (c.rank, c.suit) not in remove_set]

    def sort_by_suit(self):
        self.cards.sort(key=lambda card: (card.suit.value, card.rank.value), reverse=True)
    

