import time
from multiprocessing.pool import Pool

import logic
from tkinter import *
from logic import *
from random import *

SIZE = 500
GRID_LEN = 4
GRID_PADDING = 10

BACKGROUND_COLOR_GAME = "#92877d"
BACKGROUND_COLOR_CELL_EMPTY = "#9e948a"
BACKGROUND_COLOR_DICT = {
    2: "#eee4da", 4: "#ede0c8", 8: "#f2b179", 16: "#f59563", \
    32: "#f67c5f", 64: "#f65e3b", 128: "#edcf72", 256: "#edcc61", \
    512: "#edc850", 1024: "#edc53f", 2048: "#edc22e"
}
CELL_COLOR_DICT = {
    2: "#776e65", 4: "#776e65", 8: "#f9f6f2", 16: "#f9f6f2", \
    32: "#f9f6f2", 64: "#f9f6f2", 128: "#f9f6f2", 256: "#f9f6f2", \
    512: "#f9f6f2", 1024: "#f9f6f2", 2048: "#f9f6f2"
}
FONT = ("Verdana", 40, "bold")

KEY_UP_ALT = "\'\\uf700\'"
KEY_DOWN_ALT = "\'\\uf701\'"
KEY_LEFT_ALT = "\'\\uf702\'"
KEY_RIGHT_ALT = "\'\\uf703\'"

KEY_UP = "'w'"
KEY_DOWN = "'s'"
KEY_LEFT = "'a'"
KEY_RIGHT = "'d'"


class Game():

    def __init__(self):

        self.matrix = np.zeros((4, 4))
        self.matrix = logic.add_two_or_four(self.matrix)
        self.matrix = logic.add_two_or_four(self.matrix)

    def key_down(self, key):
        """
         # 0: left, 1: up, 2: right, 3: down
        """
        self.matrix, moved, score = logic.move(self.matrix, key)
        if moved:
            self.matrix = logic.add_two_or_four(self.matrix)

    @property
    def game_state(self):
        return logic.game_state(self.matrix)


def get_score(board, first_move):
    sboard = board.copy()
    sboard, moved, score = logic.move(sboard, first_move)
    if not moved:
        return -1
    total_score = 0
    for i in range(100):
        game_score = score
        simulation_board = sboard.copy()
        simulation_board = logic.add_two_or_four(simulation_board)
        while logic.game_state(simulation_board) != "lose":
            simulation_board, moved, move_score = logic.move(simulation_board, randint(0, 3))
            if moved:
                simulation_board = logic.add_two_or_four(simulation_board)
            game_score += move_score
        total_score += game_score
    return total_score / 100


def get_best_input(board):
    with Pool(4) as p:
        results = p.starmap(get_score, [(board, 0), (board, 1), (board, 2), (board, 3)])
    return results.index(max(results))


class GameGrid(Frame):
    def __init__(self):
        Frame.__init__(self)

        self.grid()
        self.master.title('2048')

        self.grid_cells = []
        self.init_grid()
        self.init_matrix()
        self.update_grid_cells()
        self.auto_solve()

    def init_grid(self):
        background = Frame(self, bg=BACKGROUND_COLOR_GAME, width=SIZE, height=SIZE)
        background.grid()
        for i in range(GRID_LEN):
            grid_row = []
            for j in range(GRID_LEN):
                cell = Frame(background, bg=BACKGROUND_COLOR_CELL_EMPTY, width=SIZE / GRID_LEN, height=SIZE / GRID_LEN)
                cell.grid(row=i, column=j, padx=GRID_PADDING, pady=GRID_PADDING)
                # font = Font(size=FONT_SIZE, family=FONT_FAMILY, weight=FONT_WEIGHT)
                t = Label(master=cell, text="", bg=BACKGROUND_COLOR_CELL_EMPTY, justify=CENTER, font=FONT, width=4,
                          height=2)
                t.grid()
                grid_row.append(t)

            self.grid_cells.append(grid_row)

    def gen(self):
        return randint(0, GRID_LEN - 1)

    def init_matrix(self):
        self.matrix = np.zeros((4, 4))

        self.matrix = logic.add_two_or_four(self.matrix)
        self.matrix = logic.add_two_or_four(self.matrix)

    def update_grid_cells(self):
        for i in range(GRID_LEN):
            for j in range(GRID_LEN):
                new_number = self.matrix[i][j]
                if new_number == 0:
                    self.grid_cells[i][j].configure(text="", bg=BACKGROUND_COLOR_CELL_EMPTY)
                else:
                    self.grid_cells[i][j].configure(text=str(new_number), bg=BACKGROUND_COLOR_DICT[new_number],
                                                    fg=CELL_COLOR_DICT[new_number])
        self.update_idletasks()

    def auto_solve(self):
        while True:
            input = get_best_input(self.matrix)
            self.matrix, moved, score = logic.move(self.matrix, input)

            if moved:
                self.matrix = logic.add_two_or_four(self.matrix)
                self.update_grid_cells()
                moved = False
            self.update()
