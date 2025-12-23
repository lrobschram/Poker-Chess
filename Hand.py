from Card import Card, Suit, Rank
from typing import List
from Deck import Deck

class Hand:

    def __init__(self, cards: List[Card]):
        if len(cards) != 5:
            raise ValueError("A hand must start with exactly 5 cards")
        self.cards = cards

    def discard(self, indices: List[int], deck: Deck):
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

        # Draw replacements
        new_cards = deck.draw(len(indices))
        self.cards.extend(new_cards)
    
    def print_hand(self):
        for i, card in enumerate(self.cards):
            print(f"{i}: {card}")

    def get_cards(self):
        return self.cards