from Deck import Deck
from Hand import Hand
from HandEvaluator import evaluate_hand, HandRank
from Player import Player
from PokerPhase import PokerPhase, refill_to_seven

def prompt_discard(hand, deck):
    """
    Prompts the user to discard cards by index.
    Input format: space-separated indices, or empty to keep all.
    Example: '0 2 4'
    """
    while True:
        try:
            raw = input("Enter card indices to discard (or press Enter to keep): ").strip()

            if raw == "":
                return

            indices = list(map(int, raw.split()))

            hand.discard(indices, deck)
            return

        except (ValueError, IndexError) as e:
            print(f"Invalid input: {e}")
            print("Try again.\n")


def test_discard():
        
        deck = Deck()
        hand = Hand(deck.draw(5))

        print("Initial hand:")
        hand.print_hand()
        print(str(evaluate_hand(hand.cards)))

        prompt_discard(hand, deck)
        
        print("\nAfter discard:")
        hand.print_hand()
        print(str(evaluate_hand(hand.cards)))


def test_poker_phase():

    player = Player()
    hand_rank = PokerPhase(player)

    if (hand_rank == None):
        print("SKIPPED PLAY")
    else:
        print(hand_rank.name)


def test_refilling_deck():

    player = Player() 
    player.deck.cards = player.deck.cards[:2]    # reduce deck to 2
    player.hand.discard([2, 3, 4, 5, 6])    # reduce hand to 2

    print("CURR DECK:")
    player.deck.print_deck()

    print("CURR HAND:")
    player.hand.print_hand()

    refill_to_seven(player)

    print("Hand size:", player.hand.size())      # should be 7
    print("Deck remaining:", player.deck.remaining())   # should be 47


def main():
    test_refilling_deck()

if __name__ == "__main__":
    main()