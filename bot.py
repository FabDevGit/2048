import re
import random
from multiprocessing import Pool
import time
import numpy as np
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

import logic
from puzzle import Game

sim_nb = 100

def start_web_game():
    """
    Open the browser, parse the board and hit the best arrow !
    """
    browser = webdriver.Chrome('/Users/lucasberbesson/Downloads/chromedriver')
    browser.get('https://gabrielecirulli.github.io/2048/')

    grid = browser.find_element_by_tag_name('body')
    direction = [Keys.LEFT, Keys.UP, Keys.RIGHT, Keys.DOWN]
    while True:
        board = parse_tile_array(browser.find_element_by_css_selector('.tile-container').get_attribute("innerHTML"))
        input = get_best_input(board)
        grid.send_keys(direction[input])
        time.sleep(0.1)


def get_score(board, first_move):
    """
    Given a board and a first_move, get a score by playing a lot of random games
    """
    sboard = board.copy()
    sboard, moved, score = logic.move(sboard, first_move)
    if not moved:
        return -1
    total_score = 0
    for i in range(sim_nb):
        game_score = score
        simulation_board = sboard.copy()
        simulation_board = logic.add_two_or_four(simulation_board)
        while logic.game_state(simulation_board) != "lose":
            simulation_board, moved, move_score = logic.move(simulation_board, random.randint(0, 3))
            if moved:
                simulation_board = logic.add_two_or_four(simulation_board)
            game_score += move_score
        total_score += game_score
    return total_score / sim_nb


def get_best_input(board):
    """
    Should I move the board left, right, up or down ?
    """
    with Pool(4) as p:
        results = p.starmap(get_score, [(board, 0), (board, 1), (board, 2), (board, 3)])
    return results.index(max(results))


def parse_tile_array(html_board):
    """
    Scrap the state of the board on the webpage
    """
    board = np.zeros((4, 4))
    pattern = re.compile('tile-(?P<value>\d+) tile-position-(?P<x>\d)-(?P<y>\d)')
    for tile in pattern.finditer(html_board):
        x = int(tile["x"]) - 1
        y = int(tile["y"]) - 1
        board[y][x] = int(tile["value"])
    return board


def export_matrix(matrix):
    """
    Save final board as csv file
    :param matrix:
    :return:
    """
    export = "{}, ".format(sim_nb)
    for i in range(4):
        for j in range(4):
            export += "{},".format(int(matrix[i][j]))
    with open('monte_carlo_results.csv', 'a') as fd:
        fd.write(export[:-1] + '\n')


def start_cli_game():
    game = Game()
    while game.game_state == "not over":
        input = get_best_input(game.matrix)
        game.key_down(input)
    export_matrix(game.matrix)


start_web_game()