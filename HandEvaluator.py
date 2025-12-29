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

def is_straight(ranks):
    ranks = sorted(set(ranks))
    if len(ranks) != 5:
        return False

    # Ace-low straight (A-2-3-4-5)
    if ranks == [2, 3, 4, 5, 14]:
        return True

    return ranks == list(range(ranks[0], ranks[0] + 5))


def evaluate_hand(cards):
    n = len(cards)
    if n == 0:
        raise ValueError("Hand cannot be empty")

    ranks = [card.rank.value for card in cards]
    suits = [card.suit for card in cards]

    rank_counts = Counter(ranks)
    counts = sorted(rank_counts.values(), reverse=True)

    # --- Count-based hands (work with < 5 cards) ---
    if counts == [4, 1] or counts == [4]:
        return HandRank.FOUR_KIND
    if counts == [3, 2]:      # only possible if 5 cards
        return HandRank.FULL_HOUSE
    if counts == [3, 1, 1] or counts == [3, 1] or counts == [3]:
        return HandRank.THREE_KIND
    if counts == [2, 2, 1] or counts == [2, 2]:
        return HandRank.TWO_PAIR
    if counts == [2, 1, 1, 1] or counts == [2, 1] or counts == [2, 1, 1] or counts == [2]:
        return HandRank.ONE_PAIR

    # --- Only evaluate 5-card structure hands ---
    if n == 5:
        flush = len(set(suits)) == 1
        straight = is_straight(ranks)

        if straight and flush:
            return HandRank.STRAIGHT_FLUSH
        if flush:
            return HandRank.FLUSH
        if straight:
            return HandRank.STRAIGHT

    # default fallback
    return HandRank.HIGH_CARD
