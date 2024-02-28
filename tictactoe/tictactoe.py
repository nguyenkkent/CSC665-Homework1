import math
import copy

# Use these constants to fill in the game board
X = "X"
O = "O"
EMPTY = None


def start_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns which player (either X or O) who has the next turn on a board.

    In the initial game state, X gets the first move. Subsequently, the player alternates with each additional move.
    Any return value is acceptable if a terminal board is provided as input (i.e., the game is already over).
    """
    xCounter, oCounter = 0, 0
    # scan the board
    for row in range(3):
        for col in range(3):
            if board[row][col] == X:
                xCounter += 1
            if board[row][col] == O:
                oCounter += 1

    return X if xCounter == oCounter else O


def actions(board):
    """
    Returns the set of all possible actions (i, j) available on the board.

    The actions function should return a set of all the possible actions that can be taken on a given board.
    Each action should be represented as a tuple (i, j) where i corresponds to the row of the move (0, 1, or 2)
    and j corresponds to the column of the move (also 0, 1, or 2).

    Possible moves are any cells on the board that do not already have an X or an O in them.

    Any return value is acceptable if a terminal board is provided as input.
    """
    possibleMoves = set()
    for row in range(3):
        for col in range(3):
            if board[row][col] is EMPTY:
                possibleMoves.add((row, col))

    return possibleMoves if len(possibleMoves) > 0 else None


def succ(board, action):
    """
    Returns the board that results from making move (i, j) on the board, without modifying the original board.

    If `action` is not a valid action for the board, you  should raise an exception.

    The returned board state should be the board that would result from taking the original input board, and letting
    the player whose turn it is make their move at the cell indicated by the input action.

    Importantly, the original board should be left unmodified. This means that simply updating a cell in `board` itself
    is not a correct implementation of this function. You’ll likely want to make a deep copy of the board first before
    making any changes.
    """
    if action not in actions(board):
        raise Exception("Invalid action")

    # create the future board with action
    successorBoard = copy.deepcopy(board)
    currentPlayer = player(board)
    row, col = action
    successorBoard[row][col] = currentPlayer

    return successorBoard

def winner(board):
    """
    Returns the winner of the game, if there is one.

    - If the X player has won the game, the function should return X.
    - If the O player has won the game, the function should return O.
    - If there is no winner of the game (either because the game is in progress, or because it ended in a tie), the
      function should return None.

    You may assume that there will be at most one winner (that is, no board will ever have both players with
    three-in-a-row, since that would be an invalid board state).
    """
    # check for winner in each row
    for row in board:
        if row[0] is not EMPTY and row[0] == row[1] == row[2]:
            return row[0]
    # check for winner in each column
    for col in range(3):
        if board[col] is not EMPTY and board[0][col] == board[1][col] == board[2][col]:
            return board[0][col]

    # check for winner in diagonals
    if board[0][0] is not EMPTY and board[0][0] == board[1][1] == board[2][2]:
        return board[0][0]
    if board[0][2] is not EMPTY and board[0][2] == board[1][1] == board[2][0]:
        return board[0][2]

    # tie
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.

    If the game is over, either because someone has won the game or because all cells have been filled without anyone
    winning, the function should return True.

    Otherwise, the function should return False if the game is still in progress.
    """
    result = winner(board)
    # X or O won
    if result is not None:
        return True

    # assertion: board is filled or is still on going

    # there are no more moves to make i.e. board is full
    for row in board:
        if EMPTY in row:
            return False

    # no winner yet and board is not full
    return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.

    You may assume utility will only be called on a board if terminal(board) is True.
    """
    result = winner(board)
    if result == X: return 1
    if result == O: return -1
    return 0

def minimax(board):
    """
    Returns the optimal action for the current player on the board.

    The move returned should be the optimal action (i, j) that is one of the allowable actions on the board.

    If multiple moves are equally optimal, any of those moves is acceptable.

    If the board is a terminal board, the minimax function should return None.
    """
    if terminal(board):
        return None

    currentPlayer = player(board)
    possibleActions = actions(board)

    if currentPlayer == X:
        value = float("-inf")
        optimalAction = None
        for action in possibleActions:
            newValue = recursionHelper(succ(board, action))
            if newValue > value:
                value = newValue
                optimalAction = action
        return optimalAction
    else:
        value = float("inf")
        optimalAction = None
        for action in possibleActions:
            newValue = recursionHelper(succ(board, action))
            if newValue < value:
                value = newValue
                optimalAction = action
        return optimalAction


# recursion function to determine winner
def recursionHelper(board):
    # board is in terminal state, return utility
    if terminal(board):
        return utility(board)

    currentPlayer = player(board)

    # max player's turn
    if currentPlayer == X:
        value = float("-inf")
        for action in actions(board):
            value = max(value, recursionHelper(succ(board, action)))
        return value
    # min player's turn
    else:
        value = float("inf")
        for action in actions(board):
            value = min(value, recursionHelper(succ(board, action)))
        return value