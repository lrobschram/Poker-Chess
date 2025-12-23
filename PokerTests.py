from Deck import Deck
from Hand import Hand
from HandEvaluator import evaluate_hand, HandRank

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

def main():

    deck = Deck()
    hand = Hand(deck.draw(5))

    print("Initial hand:")
    hand.print_hand()
    print(str(evaluate_hand(hand.cards)))

    prompt_discard(hand, deck)
    
    print("\nAfter discard:")
    hand.print_hand()
    print(str(evaluate_hand(hand.cards)))

if __name__ == "__main__":
    main()