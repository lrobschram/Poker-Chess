from HandEvaluator import evaluate_hand, HandRank
from Deck import Deck

def refill_deck(player):
    player.deck = Deck()
    player.deck.remove_cards(player.hand.cards)

def refill_to_seven(player):
    if (player.hand.size() < 7):
        amt_needed = 7 - player.hand.size()

        try:
            new_cards = player.deck.draw(amt_needed)

        except ValueError as e:
            refill_deck(player)
            new_cards = player.deck.draw(amt_needed)

        player.hand.add_cards(new_cards)


def pick_five_cards(hand):

    valid_input = False

    while(not valid_input):
        hand.print_hand()
        raw = input("Enter at most 5 card indices to play (or Enter to skip): ").strip() 

        if raw == "":
            return None

        indices = list(map(int, raw.split()))

        # Check if input has at most 5 cards selected
        if (len(indices) > 5):
            print("\nCannot select more than 5 cards! Try again")
            continue

        # Check if input has valid indices
        if any(i < 0 or i >= hand.size() for i in indices):
            print("\nOne or more indices are out of range — try again")
            continue

        valid_input = True

    return indices


def PokerPhase(player):

    # draw cards up to 7 
    refill_to_seven(player)
    
    # reshuffle deck if ran out of cards (TODO what if draw illegal poker hands? eg. 5 of a kind)

    # allow for 2 discards (or skip)

    # select cards to play poker hand (or skip?)
    chosen_indices = pick_five_cards(player.hand)
    
    # evaluate the hand
    if (chosen_indices != None):
        hand_rank = evaluate_hand([player.hand.cards[i] for i in chosen_indices])
    else:
        return None # return no piece if skipped play

    # discard played cards
    player.hand.discard(chosen_indices, player.deck)

    # return the piece earned 
    return hand_rank