from collections import Counter
from enum import Enum, auto

class HandRank(Enum):
    HIGH_CARD = auto()
    PAIR = auto()
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

def chip_counter(cards):
    ranks = [card.rank.value for card in cards]
    chip_counter = 0;
    for rank in ranks:
        chip_counter += rank

    return chip_counter

def add_bonus (chips):
    noBonus = "commonUnit"
    smallBonus = "healthyUnit"
    mediumBonus = "strongUnit"
    largeBonus = "royalUnit"

    if(chips < 40):
        return noBonus
    elif (chips < 50 ):
         return smallBonus
    elif(chips < 60):
        return mediumBonus
    else: return largeBonus


def evaluate_hand(cards):
    """
    Returns:
        (HandRank, list[Card])   # ONLY the cards that form the poker hand
    """
    n = len(cards)
    if n == 0:
        raise ValueError("Hand cannot be empty")

    ranks = [c.rank.value for c in cards]
    suits = [c.suit for c in cards]
    rank_counts = Counter(ranks)

    # Map rank -> cards with that rank
    rank_to_cards = {}
    for c in cards:
        rank_to_cards.setdefault(c.rank.value, []).append(c)

    counts = sorted(rank_counts.values(), reverse=True)

    # --- Count-based hands ---
    if counts[:1] == [4]:
        quad_rank = max(rank_counts, key=lambda r: rank_counts[r])
        return HandRank.FOUR_KIND, rank_to_cards[quad_rank]

    if counts == [3, 2]:
        trip_rank = max(rank_counts, key=lambda r: (rank_counts[r], r))
        pair_rank = min(rank_counts, key=lambda r: (rank_counts[r], r))
        return HandRank.FULL_HOUSE, rank_to_cards[trip_rank] + rank_to_cards[pair_rank]

    if counts[:1] == [3]:
        trip_rank = max(rank_counts, key=lambda r: (rank_counts[r], r))
        return HandRank.THREE_KIND, rank_to_cards[trip_rank]

    if counts[:2] == [2, 2]:
        pair_ranks = sorted(
            [r for r, c in rank_counts.items() if c == 2],
            reverse=True
        )
        return (
            HandRank.TWO_PAIR,
            rank_to_cards[pair_ranks[0]] + rank_to_cards[pair_ranks[1]]
        )

    if counts[:1] == [2]:
        pair_rank = max(rank_counts, key=lambda r: (rank_counts[r], r))
        return HandRank.PAIR, rank_to_cards[pair_rank]

    # --- 5-card structure hands ---
    if n == 5:
        flush = len(set(suits)) == 1
        straight = is_straight([card.rank.value for card in cards])

        if straight and flush:
            return HandRank.STRAIGHT_FLUSH, cards

        if flush:
            return HandRank.FLUSH, cards

        if straight:
            return HandRank.STRAIGHT, cards

    # --- Default ---
    # High card = single highest card
    high = max(cards, key=lambda c: c.rank.value)
    return HandRank.HIGH_CARD, [high]