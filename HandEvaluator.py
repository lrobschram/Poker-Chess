from collections import Counter
from enum import Enum, auto

class HandRank(Enum):
    HIGH_CARD = auto()
    ONE_PAIR = auto()
    TWO_PAIR = auto()
    THREE_KIND = auto()
    STRAIGHT = auto()
    FLUSH = auto()
    FULL_HOUSE = auto()
    FOUR_KIND = auto()
    STRAIGHT_FLUSH = auto()

def evaluate_hand(cards):
    ranks = sorted(card.rank.value for card in cards)
    suits = [card.suit for card in cards]

    rank_counts = Counter(ranks)
    counts = sorted(rank_counts.values(), reverse=True)

    is_flush = len(set(suits)) == 1
    is_straight = ranks == list(range(ranks[0], ranks[0] + 5))

    if is_straight and is_flush:
        return HandRank.STRAIGHT_FLUSH
    if counts == [4, 1]:
        return HandRank.FOUR_KIND
    if counts == [3, 2]:
        return HandRank.FULL_HOUSE
    if is_flush:
        return HandRank.FLUSH
    if is_straight:
        return HandRank.STRAIGHT
    if counts == [3, 1, 1]:
        return HandRank.THREE_KIND
    if counts == [2, 2, 1]:
        return HandRank.TWO_PAIR
    if counts == [2, 1, 1, 1]:
        return HandRank.ONE_PAIR
    return HandRank.HIGH_CARD
