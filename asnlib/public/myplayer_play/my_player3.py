# 6853115445: Ziyue Wang
import random
# from copy import deepcopy
import os
import math
import numpy as np

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
MIN_MAX_WIDTH = 28


def deepcopy(board):
    return np.asarray(board).tolist()


board_move_list_dict = {}  # speedup
board_next_board_dict = {}


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


magic_order = [(2, 2), (1, 2), (3, 2), (2, 3), (2, 1),
               (3, 3), (1, 1), (1, 3), (3, 1), (2, 4),
               (2, 0), (4, 2), (0, 2), (3, 0), (1, 4),
               (0, 1), (4, 3), (1, 0), (3, 4), (4, 1),
               (0, 3), (0, 0), (4, 4), (0, 4), (4, 0)]


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
        # randnum = random.randint(0, 100)
        # random.seed(randnum)
        # random.shuffle(self.move_list)
        # random.seed(randnum)
        # random.shuffle(self.next_board)

    def get_all_possible_move(self):
        """
        check all 0s and find all
          1. have liberty
          2. no liberty but can kill enemy and not violate KO rule
        :return: a list of possible moves on the board
        """
        board_str = board_string(self.cur_board)
        if board_str in board_move_list_dict:
            self.next_board = board_next_board_dict[board_str]
            return board_move_list_dict[board_str]

        move_list = []
        for i, j in magic_order:
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

        board_move_list_dict[board_str] = move_list
        board_next_board_dict[board_str] = self.next_board
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


class RandomPlayer:
    def __init__(self, move_list):
        self.move_list = move_list

    def get_move(self):
        if len(self.move_list) == 0:
            return "PASS"

        return self.move_list[0]


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
        self.q_values = {}
        self.q_values[BLACK] = self.init_q_values(1)  # <board_string, Q[][]>
        self.q_values[WHITE] = self.init_q_values(2)

    def set_go(self, go):
        """
        inject go into qlearner
        :param go: the game
        :return: none
        """
        self.go = go
        self.side = go.my_player

    def init_q_values(self, side):
        """
        read QvalueDB
        may be removed in next edition
        :return: none
        """
        q_values = {}
        file_name = "QvalueDB_" + str(side) + ".txt"
        if not os.path.exists(file_name):
            with open(file_name, 'w') as f:
                return q_values

        with open(file_name, 'r') as f:
            for line in f:
                data = line.split('|')
                board = data[0]
                q = np.asarray(list(map(float, data[1:])))
                q = np.reshape(q, (5, 5))
                q_values[board] = q
        return q_values

    def board_value(self, board):
        """
        get BLACK how better than WHITE
        BLACK - WHITE + KOMI
        :param board: calculating board
        :return: BLACK - WHITE + KOMI
        """
        flatten = flatten_board(board)
        board_value = flatten.count(1) - flatten.count(
            2) + QLearner.KOMI  # BLACK - WHITE + KOMI means BLACK how better than WHITE
        return board_value

    def R(self, board_before, board_after):
        """
        Reward in the Qlearn function
        R = afterValue - beforeValue
        :param board_before:
        :param board_after:
        :return:
        """
        R = self.board_value(board_after) - self.board_value(board_before)
        return R

    def Q(self, local_go):
        """
        get Q value map of a board
        I think initQ is a kind of heuristic, it shows what is important.
        Currently, initQ is a combine of "how many I can kill" and "how much more liberty can I have than the enemy".
        :param board:
        :return: 5*5 map of Qvalue
        """
        board = local_go.cur_board
        board_str = board_string(board)
        if board_str not in self.q_values[local_go.my_player]:
            # init Q
            q_val = np.zeros((BOARD_SIZE, BOARD_SIZE))

            for i_move in range(len(local_go.move_list)):
                black_liberty_sum = 0
                white_liberty_sum = 0
                black_sum = 0
                white_sum = 0
                move = local_go.move_list[i_move]
                local_go.test_board = local_go.next_board[i_move]
                for i in range(BOARD_SIZE):
                    for j in range(BOARD_SIZE):
                        # self.go.test_board = deepcopy(self.go.cur_board)
                        # if self.go.test_board[i][j] == BLACK:
                        #     black_liberty_sum += 1
                        # if self.go.test_board[i][j] == WHITE:
                        #     white_liberty_sum += 1
                        is_black_liberty = False
                        is_white_liberty = False
                        if local_go.test_board[i][j] == EMPTY:
                            for place in local_go.get_neighbor((i, j)):
                                neighbor = local_go.test_board[place[0]][place[1]]
                                if neighbor == BLACK:
                                    is_black_liberty = True
                                if neighbor == WHITE:
                                    is_white_liberty = True
                        if is_black_liberty:
                            black_liberty_sum += 1
                        if is_white_liberty:
                            white_liberty_sum += 1

                q_val[move[0]][move[1]] = (self.init_value + (black_liberty_sum - white_liberty_sum) / 40)
                kill_reward = self.board_value(local_go.test_board) - self.board_value(board)
                q_val[move[0]][move[1]] += kill_reward / 2

                neighbor_ally_list = local_go.get_all_neighbor_ally(move)
                liberty = 0
                for ally in neighbor_ally_list:
                    liberty += local_go.get_liberty(ally)
                q_val[move[0]][move[1]] += liberty / 20

                # with the same deviations, less of the other's liberty is better.
                # better connection give higher score
                move_neighbor = math.ceil(len(local_go.get_neighbor_ally(move)) / 4) / 10
                move_corner = math.ceil(len(local_go.get_corner_ally(move)) / 4) / 18
                move_jump = math.ceil(len(local_go.get_jump_ally(move)) / 4) / 30
                move_connection = move_neighbor + move_corner + move_jump

                fill_self_punishment = 0
                if len(local_go.get_neighbor(move)) == len(local_go.get_neighbor_ally(move)):
                    fill_self_punishment = -0.9
                    # avoid suicide?
                    # if liberty == 1:
                    #     fill_self_punishment = -10
                if local_go.my_player == BLACK:
                    # q_val[move[0]][move[1]] -= white_liberty_sum / 50
                    q_val[move[0]][move[1]] += move_connection
                    q_val[move[0]][move[1]] += fill_self_punishment

                    q_val[move[0]][move[1]] += kill_reward * 0.1  # try to kill to win KOMI
                else:
                    # q_val[move[0]][move[1]] += black_liberty_sum / 50
                    q_val[move[0]][move[1]] -= move_connection
                    q_val[move[0]][move[1]] -= fill_self_punishment

            self.q_values[local_go.my_player][board_str] = q_val
        return self.q_values[local_go.my_player][board_str]

    def find_max_action(self):
        """
        Black move strategy
        :return: (x,y)
        """
        move_list = self.go.move_list
        # shuffle(move_list)
        if len(move_list) <= MIN_MAX_WIDTH:
            return self.find_max_by_alpha_beta()
        else:
            cur_board_Q = self.Q(self.go)
            return self.find_max_by_Q(move_list, cur_board_Q)

    def find_min_action(self):
        """
        White move strategy
        :return: (x,y)
        """
        move_list = self.go.move_list

        if len(move_list) <= MIN_MAX_WIDTH:
            return self.find_min_by_alpha_beta()
        else:
            cur_board_Q = self.Q(self.go)
            return self.find_min_by_Q(move_list, cur_board_Q)

    def find_max_by_Q(self, move_list, cur_board_Q):
        """
        if the number of branch is more than width limit, use Qvalue to find action.
        :param move_list:
        :param cur_board_Q:
        :return:
        """
        # cur_board_Q = self.Q(self.go.cur_board)
        max_next_Q = -np.inf
        max_action = ()
        for action in move_list:
            next_Q = cur_board_Q[action[0]][action[1]]
            if next_Q > max_next_Q:
                max_next_Q = next_Q
                max_action = action
        return max_action, max_next_Q

    def find_min_by_Q(self, move_list, cur_board_Q):
        """
        if the number of branch is more than width limit, use Qvalue to find action.
        :param move_list:
        :param cur_board_Q:
        :return:
        """
        min_next_Q = np.inf
        min_action = ()

        for action in move_list:
            next_Q = cur_board_Q[action[0]][action[1]]
            if next_Q < min_next_Q:
                min_next_Q = next_Q
                min_action = action
        return min_action, min_next_Q

    def find_max_by_alpha_beta(self):
        """
        if there are not too much branches, use min-max
        :return:
        """
        max_action, max_next_Q = self.max_value(self.go.last_board, self.go.cur_board, -np.inf, np.inf, 0)
        return max_action, max_next_Q

    def find_min_by_alpha_beta(self):
        """
        if there are not too much branches, use min-max
        :return:
        """
        min_action, min_next_Q = self.min_value(self.go.last_board, self.go.cur_board, -np.inf, np.inf, 0)
        return min_action, min_next_Q

    def max_value(self, last_board, cur_board, alpha, beta, step):
        """
        max step implement
        if too deep, return an estimated solution by Qvalue.
        same in min step
        :param last_board: for KO test
        :param cur_board: get possible actions
        :param step: pass step to limit depth
        """
        go_test = Go(1, last_board, cur_board)
        move_list = go_test.move_list
        if len(move_list) == 0:
            return "PASS", self.board_value(cur_board)
        if len(move_list) + step * 4 > MIN_MAX_WIDTH or step > MIN_MAX_DEPTH + int(BOARD_SIZE - len(move_list) ** 0.5):
            move, Q = self.find_max_by_Q(move_list, self.Q(go_test))
            return move, Q + self.board_value(cur_board)
        v = -np.inf
        max_action = ()
        for i in range(len(move_list)):
            action = move_list[i]
            next_board = go_test.next_board[i]
            min_action, min_value = self.min_value(cur_board, next_board, alpha, beta, step + 1)
            if min_value > v:
                v = min_value
                max_action = action
            if v >= beta:
                return action, v
            alpha = max(alpha, v)
        return max_action, v

    def min_value(self, last_board, cur_board, alpha, beta, step):
        """
        min step implement
        :param last_board: for KO test
        :param cur_board: get possible actions
        :param step: pass step to limit depth
        """
        go_test = Go(2, last_board, cur_board)
        move_list = go_test.move_list
        if len(move_list) == 0:
            return "PASS", self.board_value(cur_board)
        if len(move_list) + step * 4 > MIN_MAX_WIDTH or step > MIN_MAX_DEPTH + int(BOARD_SIZE - len(move_list) ** 0.5):
            move, Q = self.find_min_by_Q(move_list, self.Q(go_test))
            return move, Q + self.board_value(cur_board)
        v = np.inf
        min_action = ()
        for i in range(len(move_list)):
            action = move_list[i]
            next_board = go_test.next_board[i]
            max_action, max_value = self.max_value(cur_board, next_board, alpha, beta, step + 1)
            if max_value < v:
                v = max_value
                min_action = action
            if v <= alpha:
                return action, v
            beta = max(beta, v)
        return min_action, v

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
        """
        different move for black and white
        :return:
        """
        if self.side == BLACK:
            max_action, max_next_Q = self.find_max_action()
            # if max_next_Q < -1:
            #     self.visual()
            #     return "PASS"
            return max_action
        else:
            min_action, min_next_Q = self.find_min_action()
            # if min_next_Q > 1:
            #     self.visual()
            #     return "PASS"
            return min_action

    def learn(self, state_action_list):
        """
        record all Qvalues of reached (state,action)
        :param state_action_list: state_action_state, for calcuate qvalue
        :return:
        """
        state_action_list.reverse()
        update_qvalues = {}
        for state_action_state in state_action_list:
            board_before, move, board_after = state_action_state
            go1 = Go(self.side, board_before, board_before)
            go2 = Go(self.side, board_after, board_after)
            q_t = self.Q(go1)
            q_t1 = self.Q(go2)
            # q_t = self.q_values[self.board_string(board_before)]
            # q_t1 = self.q_values[self.board_string(board_after)]
            max_q_value = np.max(q_t1)

            q_t[move[0]][move[1]] = (1 - self.alpha) * q_t[move[0]][move[1]] \
                                    + self.alpha * (self.R(board_before, board_after) + self.gamma * max_q_value)

            self.q_values[self.side][board_string(board_before)] = q_t
            update_qvalues[board_string(board_before)] = q_t

        self.q_values[self.side] = self.init_q_values(self.side)
        for kv in update_qvalues.items():
            self.q_values[self.side][kv[0]] = kv[1]

        file_name = "QvalueDB_" + str(self.side) + ".txt"
        with open(file_name, 'w') as f:
            for kv in self.q_values[self.side].items():
                if np.where(kv[1] != 0)[0].shape[0] != 0:
                    string = kv[0] + '|' + '|'.join(str(x) for x in flatten_board(kv[1])) + "\n"
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
    # my_player_ = 1
    # last_board_ = [
    #     [0, 0, 0, 0, 0],
    #     [0, 2, 1, 1, 0],
    #     [0, 0, 0, 1, 0],
    #     [0, 0, 2, 1, 0],
    #     [0, 0, 0, 2, 0]
    # ]
    # cur_board_ = [
    #     [0, 0, 0, 0, 0],
    #     [0, 2, 1, 1, 0],
    #     [0, 0, 0, 1, 0],
    #     [0, 0, 2, 1, 0],
    #     [0, 2, 0, 2, 0]
    # ]
    # go = Go(my_player_, last_board_, cur_board_)
    # result = get_result(go)
    # write(result)
