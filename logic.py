import random
import time
import numpy as np


def add_two_or_four(mat):
    zeros = np.argwhere(mat == 0)
    if zeros.any():
        zero_tile = random.choice(zeros)
        new_tile = np.random.random()
        if new_tile < 0.9:
            mat[zero_tile[0]][zero_tile[1]] = 2
        else:
            mat[zero_tile[0]][zero_tile[1]] = 4
    return mat


def game_state(mat):
    for i in range(3):  # intentionally reduced to check the row on the right and below
        for j in range(3):  # more elegant to use exceptions but most likely this will be their solution
            if mat[i][j] == mat[i + 1][j] or mat[i][j + 1] == mat[i][j]:
                return 'not over'
    for i in range(4):  # check for any zero entries
        for j in range(4):
            if mat[i][j] == 0:
                return 'not over'
    for k in range(3):  # to check the left/right entries on the last row
        if mat[3][k] == mat[3][k + 1]:
            return 'not over'
    for j in range(3):  # check up/down entries on last column
        if mat[j][3] == mat[j + 1][3]:
            return 'not over'
    return 'lose'


def move_left(col):
    new_col = np.zeros((4))
    j = 0
    score = 0
    previous = None
    for i in range(4):
        if col[i] != 0:
            if previous == None:
                previous = col[i]
            else:
                if previous == col[i]:
                    new_col[j] = 2 * col[i]
                    score += new_col[j]
                    previous = None
                else:
                    new_col[j] = previous
                    previous = col[i]
                j += 1
    if previous != None:
        new_col[j] = previous
    return new_col, score


def move(board, direction):
    # 0: left, 1: up, 2: right, 3: down
    rotated_board = np.rot90(board, direction)
    cols = [rotated_board[i, :] for i in range(4)]
    new_cols = []
    tscore = 0
    for col in cols:
        new_col = np.zeros((4))
        j = 0
        previous = None
        for i in range(4):
            if col[i] != 0:
                if previous == None:
                    previous = col[i]
                else:
                    if previous == col[i]:
                        new_col[j] = 2 * col[i]
                        tscore += new_col[j]
                        previous = None
                    else:
                        new_col[j] = previous
                        previous = col[i]
                    j += 1
        if previous != None:
            new_col[j] = previous
        new_cols.append(new_col)
    new_board = np.array(new_cols)
    new_board = np.rot90(new_board, -direction)
    if (new_board == board).all():
        moved = False
    else:
        moved = True
    return new_board, moved, tscore
