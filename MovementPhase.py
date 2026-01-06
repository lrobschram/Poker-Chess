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



def ask_to_move(color, board, pieces_moved):

    letters = string.ascii_uppercase[:board.cols]

    while True:

        # grab user input and test if valid
        raw = input("Enter curr piece loc and place to move it to or Enter to skip (ie. A7 B6): ").strip().upper()

        if (raw == ""):
            print("Skipped remaining movements!")
            return None, None

        parts = raw.split()

        if (not valid_input(parts, letters)):
            print("Please enter valid spaces on the board - try again")
            continue

        curr_loc, new_loc = parts

        # check user has a piece at inputted loc
        curr_r = int(curr_loc[1])
        curr_c = letters.index(curr_loc[0])

        piece = board.get_piece( (curr_r, curr_c) )
        if (piece == None) or (piece.owner != color): 
            print("The piece must be owned by you - try again")
            continue
        if piece in pieces_moved:
            print("Piece already moved this turn - try again")
            continue

        # generate all legal moves for the piece
        all_moves = piece.get_raw_moves(board)
        print(f"All possible moves for {piece.type.name}:")
        print(all_moves)

        move = (int(new_loc[1]), letters.index(new_loc[0]))

        # check inputted new loc is in bounds and legal for the piece
        if (not board.in_bounds(move)):
            print("New position must be in bounds - try again")
            continue

        if move not in all_moves:
            print(f"{piece.type.name} is not allowed to move there")
            continue

        # make sure new spot is empty
        if (board.get_piece(move) != None) :
            print("A piece is already there - try again")
            continue

        return (curr_r, curr_c), move


def move_piece():
    return None


"""
    Walks through the Movement Phase for the inputed player

    (1) keeps track of remaining moves + pieces moved this turn
    (2) asks player to move one of their pieces and checks if move is valid
    (3) updates the board accordingly
"""
def MovementPhase(player, board):

    can_move = True
    pieces_moved = []

    # make sure player has movements left
    # TODO make sure there are pieces that can move
    while can_move:

        print(f"\n~~~Moves left: {player.movements_left}~~~")
        print(board)

        # ask which piece to move
        curr_loc, new_loc = ask_to_move(player.color, board, pieces_moved)

        # check if player skipped remaining movements ??
        if (curr_loc == None and new_loc == None):
            break

        # move the piece
        board.move_piece(curr_loc, new_loc)

        # store pieces already moved this turn
        pieces_moved.append( board.get_piece(new_loc) )

        player.use_move()
        
        can_move = player.can_move()