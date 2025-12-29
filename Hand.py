from Card import Card
from typing import List
from Deck import Deck

class Hand:

    def __init__(self, cards: List[Card]):
        self.cards = cards

    def discard(self, indices: List[int]):
        """
        Discard cards at the given indices and draw replacements.
        indices: list of positions (0–4)
        """
        if not indices:
            return

        if len(indices) > 5:
            raise ValueError("Cannot discard more than 5 cards")

        if len(set(indices)) != len(indices):
            raise ValueError("Duplicate discard indices")

        if any(i < 0 or i >= len(self.cards) for i in indices):
            raise IndexError("Invalid card index")

        # Remove cards in descending order to avoid index shifting
        for i in sorted(indices, reverse=True):
            self.cards.pop(i)
    
    def print_hand(self):
        for i, card in enumerate(self.cards):
            print(f"{i}: {card}")

    def get_cards(self):
        return self.cards
    
    def size(self):
        return len(self.cards)
    
    def add_cards(self, cards):
        self.cards.extend(cards)