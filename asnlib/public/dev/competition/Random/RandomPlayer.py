import random
# from copy import deepcopy
import os
import math
import numpy as np


class RandomPlayer:
    def __init__(self):
        self.go = None

    def set_go(self,go):
        self.go = go

    def get_move(self):
        if len(self.go.move_list) == 0:
            return "PASS"
        move_list = self.go.move_list
        random.shuffle(move_list)
        return move_list[0]

    def learn(self, state_action_list):
        pass

"""
constants
"""
BOARD_SIZE = 5
INPUT = "input.txt"
OUTPUT = "output.txt"
EMPTY = 0
BLACK = 1
WHITE = 2
MIN_MAX_DEPTH = 2
MIN_MAX_WIDTH = 26

path = os.path.split(os.path.realpath(__file__))[0]

def realfile(side):
    return path + "\\QvalueDB_" + str(side) + ".txt"

def deepcopy(board):
    return np.asarray(board).tolist()


# board_move_list_dict = {}  # speedup
# board_next_board_dict = {}


def flatten_board(board):
    """
    change 2D board to 1D list
    :param board: [][]
    :return: []
    """
    return [i for row in board for i in row]


def board_string(board):
    """
    get string form board
    :param board: [][]
    :return: ''
    """
    return ''.join(str(x) for x in flatten_board(board))


class Go:
    def __init__(self, my_player, last_board, cur_board):
        """
        Go game. For establishing the game.
        :param my_player: line 1
        :param last_board: line 2-6
        :param cur_board: line 7-11
        """
        # self.last_board = np.asarray(last_board)
        # self.cur_board = np.asarray(cur_board)
        self.last_board = last_board
        self.cur_board = cur_board
        self.my_player = my_player

        self.test_board = []  # be used when checking a place is possible or not NEED deepcopy and careful using

        self.next_board = []  # reserved for learning strategies' usage
        self.move_list = self.get_all_possible_move()

        # avoid always same search order
        randnum = random.randint(0, 100)
        random.seed(randnum)
        random.shuffle(self.move_list)
        random.seed(randnum)
        random.shuffle(self.next_board)

    def init(self, my_player, last_board, cur_board):
        self.__init__(my_player, last_board, cur_board)

    def get_all_possible_move(self):
        """
        check all 0s and find all
          1. have liberty
          2. no liberty but can kill enemy and not violate KO rule
        :return: a list of possible moves on the board
        """
        board_str = board_string(self.cur_board)
        # if board_str in board_move_list_dict:
        #     self.next_board = board_next_board_dict[board_str]
        #     return board_move_list_dict[board_str]

        move_list = []
        # for i, j in magic_order:
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
            # for all positions
                if self.cur_board[i][j] == EMPTY:  # can place
                    self.test_board = deepcopy(self.cur_board)
                    self.test_board[i][j] = self.my_player  # place new stone
                    cur_place = (i, j)
                    if self.check_if_has_liberty(cur_place):  # satisfy 1
                        self.check_if_kill_other(cur_place)
                        move_list.append(cur_place)
                        self.next_board.append(self.test_board)
                    else:
                        if self.check_if_kill_other(cur_place) and not self.check_violate_KO():  # satisfy 2
                            move_list.append(cur_place)
                            self.next_board.append(self.test_board)
                    self.test_board = []

        # board_move_list_dict[board_str] = move_list
        # board_next_board_dict[board_str] = self.next_board
        return move_list

    def check_if_has_liberty(self, place=(-1, -1)):
        """
        first rule of possibility. get all neighbor allies and check if someone has liberty after putting here.
        as long as someone of its allies has liberties, this place has liberties (this move is valid).

        it will also be used when checking if a move can kill someone.
        :param place: checking place
        :return: boolean, true if cur place and its neighbor allies still have liberties
        """
        neighbor_ally_list = self.get_all_neighbor_ally(place)
        for ally in neighbor_ally_list:
            if self.get_liberty(ally) > 0:
                return True
        return False

    def get_all_neighbor_ally(self, place=(-1, -1)):
        """
        use dfs, find all linking neighbors having same color with checking place
        :param place: checking place
        :return: a list of neighbor allies
        """
        stack = []
        visited_allies = set()
        stack.append(place)
        while stack:
            cur_frontier = stack.pop()
            visited_allies.add(cur_frontier)
            cur_neighbor_allies = self.get_neighbor_ally(cur_frontier)
            for ally in cur_neighbor_allies:
                if ally not in stack and ally not in visited_allies:
                    stack.append(ally)
        return list(visited_allies)

    def get_neighbor_ally(self, place=(-1, -1)):
        """
        dfs util method, find direct neighbor allies
        :param place: cur checking place
        :return: a list of up to 4 neighbor allies
        """
        cur_place_player = self.test_board[place[0]][place[1]]
        neighbors = self.get_neighbor(place)
        # ally_neighbors = list(filter(lambda neighbor: self.test_board[neighbor[0]][neighbor[1]] != cur_place_player, neighbors))
        # ally_neighbors = [x for x in neighbors if self.test_board[x[0]][x[1]] != cur_place_player]
        # print(ally_neighbors)
        ally_neighbors = []
        for neighbor in neighbors:
            neighbor_player = self.test_board[neighbor[0]][neighbor[1]]
            if neighbor_player == cur_place_player:
                ally_neighbors.append(neighbor)

        return ally_neighbors

    def get_neighbor(self, place=(-1, -1)):
        """
        simple getting direct neighbors
        :param place: cur checking place
        :return: a list of direct neighbors
        """
        neighbors = []
        x = place[0]
        y = place[1]
        a = x - 1
        b = x + 1
        c = y - 1
        d = y + 1
        # if place[0] > 0:
        #     neighbors.append((place[0] - 1, place[1]))
        # if place[0] < 4:
        #     neighbors.append((place[0] + 1, place[1]))
        # if place[1] > 0:
        #     neighbors.append((place[0], place[1] - 1))
        # if place[1] < 4:
        #     neighbors.append((place[0], place[1] + 1))
        if x > 0:
            neighbors.append((a, y))
        if x < 4:
            neighbors.append((b, y))
        if y > 0:
            neighbors.append((x, c))
        if y < 4:
            neighbors.append((x, d))
        return neighbors

    def get_corner_ally(self, place=(-1, -1)):
        """
        for connectivity calculation
        :param place: cur checking place
        :return: a list of direct neighbors
        """
        cur_place_player = self.test_board[place[0]][place[1]]
        corners = []
        if place[0] > 0 and place[1] > 0 \
                and self.test_board[place[0] - 1][place[1] - 1] == cur_place_player:
            corners.append((place[0] - 1, place[1] - 1))
        if place[0] < BOARD_SIZE - 1 and place[1] < BOARD_SIZE - 1 \
                and self.test_board[place[0] + 1][place[1] + 1] == cur_place_player:
            corners.append((place[0] + 1, place[1] + 1))
        if place[1] > 0 and place[0] < BOARD_SIZE - 1 \
                and self.test_board[place[0] + 1][place[1] - 1] == cur_place_player:
            corners.append((place[0] + 1, place[1] - 1))
        if place[1] < BOARD_SIZE - 1 and place[0] > 0 \
                and self.test_board[place[0] - 1][place[1] + 1] == cur_place_player:
            corners.append((place[0] - 1, place[1] + 1))
        return corners

    def get_jump_ally(self, place=(-1, -1)):
        """
        for connectivity calculation
        :param place: cur checking place
        :return: a list of direct neighbors
        """
        cur_place_player = self.test_board[place[0]][place[1]]
        jumps = []
        if place[0] > 1 \
                and self.test_board[place[0] - 2][place[1]] == cur_place_player:
            jumps.append((place[0] - 2, place[1]))
        if place[0] < BOARD_SIZE - 2 \
                and self.test_board[place[0] + 2][place[1]] == cur_place_player:
            jumps.append((place[0] + 2, place[1]))
        if place[1] > 1 \
                and self.test_board[place[0]][place[1] - 2] == cur_place_player:
            jumps.append((place[0], place[1] - 2))
        if place[1] < BOARD_SIZE - 2 \
                and self.test_board[place[0]][place[1] + 2] == cur_place_player:
            jumps.append((place[0], place[1] + 2))
        return jumps

    def get_liberty(self, place=(-1, -1)):
        """
        get liberties of cur place stone
        :param place: cur stone
        :return: num of liberties
        """
        neighbors = self.get_neighbor(place)
        liberty = [self.test_board[x[0]][x[1]] for x in neighbors].count(0)
        return liberty

    def check_if_kill_other(self, place=(-1, -1)):
        """
        if this place not possible because no liberty, it still possible if it can kill other
        get all not ally neighbors and check their liberty
        :param place: cur placing
        :return: boolean, true if some neighbors die after cur moving
        """
        neighbors = self.get_neighbor(place)
        neighbor_enemies = []
        for neighbor in neighbors:  # find not allies and empty, aka enemies
            neighbor_player = self.test_board[neighbor[0]][neighbor[1]]
            if not (neighbor_player == EMPTY or neighbor_player == self.my_player):
                neighbor_enemies.append(neighbor)

        killed_someone = False
        for enemy in neighbor_enemies:
            if not self.check_if_has_liberty(enemy):  # if some of enemies has no liberty
                self.remove_killed_stone(enemy)  # if can kill, kill, test_board now can compare with last_board
                killed_someone = True
        return killed_someone

    def check_violate_KO(self):
        """
        if the board will be same with last board then this move invalid.
        this only happens when kill some stone
        :return: boolean, true if violate KO rule
        """
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                if self.test_board[i][j] != self.last_board[i][j]:
                    return False
        return True

    def remove_killed_stone(self, place=(-1, -1)):
        """
        change killed place and its all neighbor allies to 0
        :param place: killed place
        :return: none
        """
        neighbors = self.get_all_neighbor_ally(place)
        for neighbor in neighbors:
            self.test_board[neighbor[0]][neighbor[1]] = 0