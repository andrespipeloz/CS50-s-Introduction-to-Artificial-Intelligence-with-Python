"""
Tic Tac Toe Player
"""

import math
import copy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    x_count = 0
    o_count = 0

    for row in range(len(board)):
        for col in range(len(board[row])):
            if board[row][col] == X:
                x_count += 1
            if board[row][col] == O:
                o_count += 1

    if x_count > o_count:
        return O
    else:
        return X


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    actions = set()

    for row in range(len(board)):
        for col in range(len(board)):
            if board[row][col] == EMPTY:
                actions.add((row, col))

    return actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    if action not in actions(board):
        raise Exception("Not valid action")

    i, j = action
    copy_of_board = copy.deepcopy(board)
    copy_of_board[i][j] = player(board)
    return copy_of_board


def line_winner(board, player):

    for row in range(len(board)):
        if board[row][0] == player and board[row][1] == player and board[row][2] == player:
            return True

    for col in range(len(board)):
        if board[0][col] == player and board[1][col] == player and board[2][col] == player:
            return True

    counter1 = 0
    for row in range(len(board)):
        for col in range(len(board[row])):
            if row == col and board[row][col] == player:
                counter1 += 1

    if counter1 == 3:
        return True

    counter2 = 0
    for row in range(len(board)):
        for col in range(len(board[row])):
            if (len(board) - row - 1) == col and board[row][col] == player:
                counter2 += 1

    if counter2 == 3:
        return True

    return False


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    if line_winner(board, X):
        return X

    if line_winner(board, O):
        return O


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) == X:
        return True

    if winner(board) == O:
        return True

    for row in range(len(board)):
        for col in range(len(board)):
            if board[row][col] == EMPTY:
                return False

    return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == X:
        return 1

    elif winner(board) == O:
        return -1
    else:
        return 0


def min_value(board):
    v = math.inf
    if terminal(board):
        return utility(board)
    for action in actions(board):
        v = min(v, max_value(result(board, action)))
    return v


def max_value(board):
    v = -math.inf
    if terminal(board):
        return utility(board)
    for action in actions(board):
        v = max(v, min_value(result(board, action)))
    return v


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board) == True:
        return None

    # If player is x
    elif player(board) == X:
        options = []
        # Add in option list a tuple of the action and the min_value of this value
        for action in actions(board):
            options.append([min_value(result(board, action)), action])
        # reverse the option list to get the option with the highest min_value, to get the action option that it should take
        return sorted(options, key=lambda x: x[0], reverse=True)[0][1]

    elif player(board) == O:
        options = []
        for action in actions(board):
            options.append([max_value(result(board, action)), action])
        return sorted(options, key=lambda x: x[0])[0][1]
