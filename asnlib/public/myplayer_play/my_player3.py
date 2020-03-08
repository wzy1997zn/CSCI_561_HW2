# 6853115445: Ziyue Wang
import random
from copy import deepcopy
import os

"""
constants
"""
BOARD_SIZE = 5
INPUT = "input.txt"
OUTPUT = "output.txt"
EMPTY = 0
BLACK = 1
WHITE = 2


class Go:
    def __init__(self, my_player, last_board, cur_board):
        """
        Go game. For establishing the game.
        :param my_player: line 1
        :param last_board: line 2-6
        :param cur_board: line 7-11
        """
        self.last_board = last_board
        self.cur_board = cur_board
        self.my_player = my_player

        self.test_board = []  # be used when checking a place is possible or not NEED deepcopy and careful using

        self.next_board = []  # reserved for learning strategies' usage
        self.move_list = self.get_all_possible_move()


    def get_all_possible_move(self):
        """
        check all 0s and find all
          1. have liberty
          2. no liberty but can kill enemy and not violate KO rule
        :return: a list of possible moves on the board
        """
        move_list = []
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):  # for all positions
                if self.cur_board[i][j] == EMPTY:  # can place
                    self.test_board = deepcopy(self.cur_board)
                    self.test_board[i][j] = self.my_player  # place new stone
                    cur_place = (i, j)
                    if self.check_if_has_liberty(cur_place):  # satisfy 1
                        move_list.append(cur_place)
                        self.next_board.append(self.test_board)
                    else:
                        if self.check_if_kill_other(cur_place) and not self.check_violate_KO():  # satisfy 2
                            move_list.append(cur_place)
                            self.next_board.append(self.test_board)
                    self.test_board = []

        randnum = random.randint(0, 100)
        random.seed(randnum)
        random.shuffle(move_list)
        random.seed(randnum)
        random.shuffle(self.next_board)
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
        if place[0] > 0:
            neighbors.append((place[0] - 1, place[1]))
        if place[0] < BOARD_SIZE - 1:
            neighbors.append((place[0] + 1, place[1]))
        if place[1] > 0:
            neighbors.append((place[0], place[1] - 1))
        if place[1] < BOARD_SIZE - 1:
            neighbors.append((place[0], place[1] + 1))
        return neighbors

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


class RandomPlayer:
    def __init__(self, move_list):
        self.move_list = move_list

    def get_move(self):
        if len(self.move_list) == 0:
            return "PASS"

        return self.move_list[0]


import numpy as np


class QLearner:
    """
    Qlearner for Little-GO
    Q(state_i, action_i) <-- (1-alpha)*Q(state_i, action_i) + alpha * (R_state_i_action_i + gamma * max_action_Q(state_i+1, action))
    state--     board
    action--    move
    R--         value deviation after move
    Q--         Q value: The expectation of the reward of performing action_i when state_i
    alpha--     learning rate
    gamma--     future confidence
    """

    KOMI = -2.5  # Komi BLACK's goal is get higher value, WHITE's goal is get lower value

    def __init__(self, alpha=.7, gamma=.9, init_value=0):
        self.go = None
        self.side = None
        self.alpha = alpha
        self.gamma = gamma
        self.init_value = init_value
        self.q_values = self.init_q_values()  # <board_string, Q[][]>

    def set_go(self, go):
        self.go = go
        self.side = go.my_player

    def init_q_values(self):
        q_values = {}

        if not os.path.exists('QvalueDB.txt'):
            with open("QvalueDB.txt", 'w') as f:
                return q_values

        with open("QvalueDB.txt", 'r') as f:
            for line in f:
                data = line.split('|')
                board = data[0]
                q = np.asarray(list(map(float, data[1:])))
                q = np.reshape(q, (5, 5))
                q_values[board] = q
        return q_values

    def flatten_board(self, board):
        return [i for row in board for i in row]

    def board_string(self, board):
        return ''.join(str(x) for x in self.flatten_board(board))

    def board_value(self, board):
        flatten_board = self.flatten_board(board)
        board_value = flatten_board.count(1) - flatten_board.count(
            2) + QLearner.KOMI  # BLACK - WHITE + KOMI means BLACK how better than WHITE
        return board_value

    def R(self, board_before, board_after):
        R = self.board_value(board_after) - self.board_value(board_before)
        return R

    def Q(self, board):
        board_string = self.board_string(board)
        if board_string not in self.q_values:
            # init Q
            q_val = np.zeros((5, 5))

            # current init Q is 0
            # what if set 0.5 * total liberty deviation as a part of init Q?

            for i_move in range(len(self.go.move_list)):
                black_liberty_sum = 0
                white_liberty_sum = 0
                move = self.go.move_list[i_move]
                self.go.test_board = self.go.next_board[i_move]
                for i in range(BOARD_SIZE):
                    for j in range(BOARD_SIZE):
                        # self.go.test_board = deepcopy(self.go.cur_board)
                        if self.go.test_board[i][j] == BLACK:
                            black_liberty_sum += self.go.get_liberty((i,j))
                        if self.go.test_board[i][j] == WHITE:
                            white_liberty_sum += self.go.get_liberty((i,j))

                q_val[move[0]][move[1]] = (self.init_value + (black_liberty_sum - white_liberty_sum)/20)
            self.q_values[board_string] = q_val
        return self.q_values[board_string]

    def find_max_action(self):
        move_list = self.go.move_list
        # shuffle(move_list)
        max_next_Q = -np.inf
        max_action = ()
        cur_board_Q = self.Q(self.go.cur_board)
        for action in move_list:
            next_Q = cur_board_Q[action[0]][action[1]]
            if next_Q > max_next_Q:
                max_next_Q = next_Q
                max_action = action
        return max_action, max_next_Q

    def find_min_action(self):
        move_list = self.go.move_list

        min_next_Q = np.inf
        min_action = ()
        cur_board_Q = self.Q(self.go.cur_board)
        for action in move_list:
            next_Q = cur_board_Q[action[0]][action[1]]
            if next_Q < min_next_Q:
                min_next_Q = next_Q
                min_action = action
        return min_action, min_next_Q

    def visual(self):
        """
        copy from host, remove before submit
        :return:
        """
        board = self.go.cur_board
        print('-' * len(board) * 2)
        print(self.side)
        print('-' * len(board) * 2)
        for i in range(len(board)):
            for j in range(len(board)):
                if board[i][j] == 0:
                    print(' ', end=' ')
                elif board[i][j] == 1:
                    print('X', end=' ')
                else:
                    print('O', end=' ')
            print()
        print('-' * len(board) * 2)

    def get_move(self):
        if self.side == BLACK:
            max_action, max_next_Q = self.find_max_action()
            if max_next_Q < -1:
                self.visual()
                return "PASS"
            return max_action
        else:
            min_action, min_next_Q = self.find_min_action()
            if min_next_Q > 1:
                self.visual()
                return "PASS"
            return min_action

    def learn(self, state_action_list):
        for state_action_state in state_action_list:
            board_before, move, board_after = state_action_state
            q_t = self.Q(board_before)
            q_t1 = self.Q(board_after)
            max_q_value = np.max(q_t1)

            q_t[move[0]][move[1]] = (1 - self.alpha) * q_t[move[0]][move[1]] \
                                  + self.alpha * (self.R(board_before, board_after) + self.gamma * max_q_value)

            self.q_values[self.board_string(board_before)] = q_t

        with open("QvalueDB.txt", 'a') as f:
            for kv in self.q_values.items():
                if np.where(kv[1] != 0)[0].shape[0] != 0:
                    string = kv[0] + '|' + '|'.join(str(x) for x in self.flatten_board(kv[1])) + "\n"
                    f.write(string)


def get_result(go):
    strategy = QLearner()
    strategy.set_go(go)
    result = strategy.get_move()
    return result


def read():
    with open(INPUT, 'r') as f:
        lines = f.readlines()
        my_player = int(lines[0])
        last_board = []
        cur_board = []
        for i in range(1, BOARD_SIZE + 1):
            cur_line = [int(x) for x in lines[i].strip()]
            last_board.append(cur_line)
        for i in range(BOARD_SIZE + 1, BOARD_SIZE + BOARD_SIZE + 1):
            cur_line = [int(x) for x in lines[i].strip()]
            cur_board.append(cur_line)
        return my_player, last_board, cur_board


def write(result):
    with open(OUTPUT, 'w') as f:
        if result == 'PASS':
            f.write("PASS")
        else:
            out_result = f'{result[0]},{result[1]}'
            f.write(out_result)


if __name__ == '__main__':
    my_player_, last_board_, cur_board_ = read()

    go = Go(my_player_, last_board_, cur_board_)
    result = get_result(go)
    write(result)