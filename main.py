from typing import Tuple, List, Type, Set, Optional
import sys
import solve, boards

Move = str # type alias for a move (really just a string representing a color)

def play(maxdepth: int = 3, board_file_name: str = "", seed: Optional[int] = None):
    """Function called by player. Runs the game"""
    board = boards.Board() # instantiate the board
    
    if len(board_file_name) != 0:
        board.create_from_file(board_file_name)
    else:
        board.create_random(seed=seed) # create a (random) board

    moves_remaining, opp_moves_remaining = True, True # initialize flags for moves remaining
    board.print_score()
    board.print_board()
    while not board.game_over():
        print("> ", end = "")
        move = get_move(board=board) # input the move from user
        if move == "q": # break if user quits
            break
        board = board.add_move(move=move, player=0) # add user move to the board
        solver = solve.Solver(player=1, maxdepth=maxdepth) # instantiate new solver
        opp_move, _ = solver.choose_move(board=board, depth=0) # choose move for opponent
        board = board.add_move(move=opp_move, player=1) # add opponent move to the board
        board.print_score() 
        board.print_board()
    value = board.get_board_value(player=0) # get score at end of game
    if value > 0:
        print("winner!")
    elif value == 0:
        print("draw")
    else:
        print("loser :(")
    play_again(maxdepth=maxdepth, seed=seed)

def get_move(board: boards.Board) -> Move:
    """Inputs a move from the player and validates the move"""
    potential_moves = board.get_potential_moves(0) # potential moves for the player
    if not bool(potential_moves): # if there aren't any moves to be made, just get legal moves
        potential_moves = board.get_legal_moves(0)
    valid_move = False # flag that we've gotten a valid move
    while not valid_move: # loop until we get a valid move from user
        move = input()  # input move
        valid_move = move in potential_moves or move == "q" # validate move
        if not valid_move:
            print(f"valid moves: {potential_moves}")
            print("> ", end = "")
    return move 

def play_again(maxdepth: int = 3, seed: Optional[int] = None):
    """Asks the user to play again and creates a new game if so"""
    print("play again? (y or n)") # ask user to play again
    print("> ", end = "")
    again = ""
    while again not in ("y", "n"): # prompt until they say yes or no
        again = input() 
        if again == "y":
            play(maxdepth=maxdepth, seed=seed)
        elif again != "n":
            return None

if __name__ == "__main__":
    if len(sys.argv) == 2:
        maxdepth = int(sys.argv[1])
        seed = None

    elif len(sys.argv) == 3:
        maxdepth = int(sys.argv[1])
        board_file_name = sys.argv[2]
        seed = None

    elif len(sys.argv) == 4:
        maxdepth = int(sys.argv[1])
        board_file_name = bool(sys.argv[2])
        seed = int(sys.argv[3])
    play(maxdepth=maxdepth, board_file_name = board_file_name, seed=seed)