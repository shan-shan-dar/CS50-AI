"""
Tic Tac Toe Player
"""

from ast import ImportFrom
from cmath import inf
import copy
from curses import REPORT_MOUSE_POSITION
from logging import exception
import math
from random import randint
from re import M
import random

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY], [EMPTY, EMPTY, EMPTY], [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    Xs = 0
    Os = 0

    for row in board:
        for cell in row:
            if cell == X:
                Xs += 1
            elif cell == O:
                Os += 1

    if Xs == Os:
        return X
    else:
        return O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    solution = []

    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                solution.append((i, j))

    return solution


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    boardCopy = copy.deepcopy(board)

    i = action[0]
    j = action[1]

    if boardCopy[i][j] != EMPTY:
        raise Exception("Invalid Action")

    boardCopy[i][j] = player(boardCopy)

    return boardCopy


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # check horizontal
    for row in board:
        if row[0] == row[1] and row[0] == row[2] and row[0] != EMPTY:
            return row[0]

    # check vertical
    for i in range(3):
        if (
            board[0][i] == board[1][i]
            and board[0][i] == board[2][i]
            and board[0][i] != EMPTY
        ):
            return board[0][i]

    # check descending diagonal
    if (
        board[0][0] == board[1][1]
        and board[0][0] == board[2][2]
        and board[0][0] != EMPTY
    ):
        return board[0][0]

    # check ascending diagonal
    if (
        board[0][2] == board[1][1]
        and board[0][2] == board[2][0]
        and board[0][2] != EMPTY
    ):
        return board[0][2]

    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) != None:
        return True

    for row in board:
        for cell in row:
            if cell == EMPTY:
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


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """

    optimalMove = (None, None)

    if player(board) == X:
        v = -inf
        for action in actions(board):
            temp = minValue(result(board, action))

            if temp > v:
                v = temp
                optimalMove = action

            # For cases of equal utility, pick randomly
            if temp == v:
                if random.random() > 0.5:
                    v = temp
                    optimalMove = action

    else:
        v = inf
        for action in actions(board):
            temp = maxValue(result(board, action))

            if temp < v:
                v = temp
                optimalMove = action

            # For cases of equal utility, pick randomly
            if temp == v:
                if random.random() > 0.5:
                    v = temp
                    optimalMove = action

    return optimalMove


def minValue(board):

    v = inf

    if terminal(board):
        return utility(board)

    for action in actions(board):
        v = min(v, maxValue(result(board, action)))

    return v


def maxValue(board):

    v = -inf

    if terminal(board):
        return utility(board)

    for action in actions(board):
        v = max(v, minValue(result(board, action)))

    return v
