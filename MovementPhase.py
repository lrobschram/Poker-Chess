import string


def valid_input(parts, letters):
    if len(parts) != 2:
        return False

    for loc in parts:
        if len(loc) != 2:
            return False
        if loc[0] not in letters:
            return False
        if not loc[1].isdigit():
            return False

    return True



def ask_to_move(color, board):

    letters = string.ascii_uppercase[:board.cols]

    while True:

        # Grab user input and test if valid
        raw = input("Enter curr piece loc and place to move it to (ie. A7 B6): ").strip().upper()

        parts = raw.split()

        if (not valid_input(parts, letters)):
            print("Please enter valid spaces on the board - try again")
            continue

        curr_loc, new_loc = parts

        # Check user has a piece there
        curr_r = int(curr_loc[1])
        curr_c = letters.index(curr_loc[0])

        piece = board.get_piece( (curr_r, curr_c) )
        if (piece == None) or (piece.owner != color): 
            print("The piece must be owned by you - try again")
            continue

        # Generate all legal moves for the piece
        all_moves = piece.get_raw_moves(board)
        print(f"All possible moves for {piece.type}:")
        print(all_moves)

        move = (int(new_loc[1]), letters.index(new_loc[0]))

        if (not board.in_bounds(move)):
            print("New position must be in bounds - try again")
            continue

        if move not in all_moves:
            print(f"{piece.type} is not allowed to move there")
            continue

        return (curr_r, curr_c), move


def move_piece():
    return None


"""

"""
def MovementPhase(player, board):

    can_move = True

    # make sure player has movements left
    while can_move:

        print(board)

        # ask which piece to move
        curr_loc, new_loc = ask_to_move(player.color, board)

        # make sure choice is valid (in bounds, not same piece, right color, ect.)

        # move the piece
        move_piece()

        player.use_move()
        
        can_move = player.can_move()

    return None