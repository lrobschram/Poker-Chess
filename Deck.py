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
    
    def remove_card(self, card):
        if card in self.cards:
            self.cards.remove(card)
        
    def remove_cards(self, cards):
        for card in cards:
            self.remove_card(card)

    def sort_by_suit(self):
        self.cards.sort(key=lambda card: (card.suit.value, card.rank.value), reverse=True)
    

