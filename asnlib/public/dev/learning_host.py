from copy import deepcopy

import my_player3_0_1
import host

import time
from qlearns.divide_2.my_player3_0_2 import QLearner as q2

def learn_loop(i):
    my_player_ = 1
    last_board_ = [[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0]]
    cur_board_ = [[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0]]

    black_player = my_player3_0_1.QLearner()
    white_player = my_player3_0_1.QLearner()
    if i % 3 == 1:
        black_player = q2()
    elif i % 3 == 2:
        white_player = q2()

    host_GO = host.GO(5)

    black_state_action_list = []
    white_state_action_list = []

    black_move = []
    white_move = []

    for i in range(12):

        # black
        interval_b = time.time()
        go = my_player3_0_1.Go(my_player_, last_board_, cur_board_)

        black_player.set_go(go)
        black_res = black_player.get_move()
        # blakc_Q = True if len(go.move_list) >= 5 else False
        time_b = time.time() - interval_b
        if black_res == "PASS":
            print("black pass")
            break

        host_GO.set_board(1, last_board_, cur_board_)
        last_board_ = deepcopy(cur_board_)
        host_GO.place_chess(black_res[0], black_res[1], 1)
        host_GO.died_pieces = host_GO.remove_died_pieces(2)

        cur_board_ = host_GO.board

        black_state_action_list.append((last_board_, black_res, deepcopy(cur_board_)))

        host_GO.visualize_board()
        print(time_b)

        # white
        interval_w = time.time()
        go = my_player3_0_1.Go(2, last_board_, cur_board_)

        white_player.set_go(go)
        white_res = white_player.get_move()
        # white_Q = True if len(go.move_list) >= 5 else False
        time_w = time.time() - interval_w
        if white_res == "PASS":
            print("white pass")
            break

        host_GO.set_board(2, last_board_, cur_board_)
        last_board_ = deepcopy(cur_board_)
        host_GO.place_chess(white_res[0], white_res[1], 2)
        host_GO.died_pieces = host_GO.remove_died_pieces(1)

        cur_board_ = host_GO.board

        white_state_action_list.append((last_board_, white_res, deepcopy(cur_board_)))

        host_GO.visualize_board()
        print(time_w)

    if i % 3 == 0:
        black_player.learn(black_state_action_list)
        white_player.learn(white_state_action_list)
    elif i % 3 == 1:
        white_player.learn(white_state_action_list)
    else:
        black_player.learn(black_state_action_list)
    # with open("Black_action.txt", 'a') as f:
    #     for kv in black_move:
    #         string = ''.join(str(x) for x in black_player.flatten_board(kv[0])) + '|' + str(kv[1][0]) + ',' + str(kv[1][1]) + "\n"
    #         f.write(string)
    #
    # with open("White_action.txt", 'a') as f:
    #     for kv in white_move:
    #         string = ''.join(str(x) for x in black_player.flatten_board(kv[0])) + '|' + str(kv[1][0]) + ',' + str(kv[1][1]) + "\n"
    #         f.write(string)


def black_random_learn():
    my_player_ = 1
    last_board_ = [[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0]]
    cur_board_ = [[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0]]

    black_player = my_player3_0_1.QLearner()
    # white_player = my_player3_0_1.QLearner()

    host_GO = host.GO(5)

    black_state_action_list = []
    # white_state_action_list = []

    black_move = []
    # white_move = []

    for i in range(12):

        # black
        go = my_player3_0_1.Go(my_player_, last_board_, cur_board_)

        black_player.set_go(go)
        black_res = black_player.get_move()
        # blakc_Q = True if len(go.move_list) >= 5 else False

        if black_res == "PASS":
            print("black pass")
            break

        host_GO.set_board(1, last_board_, cur_board_)
        last_board_ = deepcopy(cur_board_)
        host_GO.place_chess(black_res[0], black_res[1], 1)
        host_GO.died_pieces = host_GO.remove_died_pieces(2)

        cur_board_ = host_GO.board

        black_state_action_list.append((last_board_, black_res, deepcopy(cur_board_)))

        host_GO.visualize_board()

        # white
        go = my_player3_0_1.Go(2, last_board_, cur_board_)

        # white_player.set_go(go)
        # white_res = white_player.get_move()
        # white_Q = True if len(go.move_list) >= 5 else False
        white_player = my_player3_0_1.RandomPlayer(go.move_list)
        white_res = white_player.get_move()

        if white_res == "PASS":
            print("white pass")
            break

        host_GO.set_board(2, last_board_, cur_board_)
        last_board_ = deepcopy(cur_board_)
        host_GO.place_chess(white_res[0], white_res[1], 2)
        host_GO.died_pieces = host_GO.remove_died_pieces(1)

        cur_board_ = host_GO.board
        # if white_Q:
        #     white_state_action_list.append((last_board_, white_res, deepcopy(cur_board_)))
        # else:
        #     white_move.append((last_board_, white_res))
        host_GO.visualize_board()

    black_player.learn(black_state_action_list)
    # white_player.learn(white_state_action_list)


def white_random_learn():
    my_player_ = 1
    last_board_ = [[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0]]
    cur_board_ = [[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0]]

    # black_player = my_player3_0_1.QLearner()
    white_player = my_player3_0_1.QLearner()

    host_GO = host.GO(5)

    # black_state_action_list = []
    white_state_action_list = []

    # black_move = []
    white_move = []

    for i in range(12):

        # black
        go = my_player3_0_1.Go(my_player_, last_board_, cur_board_)

        # black_player.set_go(go)
        # black_res = black_player.get_move()
        # blakc_Q = True if len(go.move_list) >= 5 else False
        black_player = my_player3_0_1.RandomPlayer(go.move_list)
        black_res = black_player.get_move()

        if black_res == "PASS":
            print("black pass")
            break

        host_GO.set_board(1, last_board_, cur_board_)
        last_board_ = deepcopy(cur_board_)
        host_GO.place_chess(black_res[0], black_res[1], 1)
        host_GO.died_pieces = host_GO.remove_died_pieces(2)

        cur_board_ = host_GO.board
        # if blakc_Q:
        #     black_state_action_list.append((last_board_, black_res, deepcopy(cur_board_)))
        # else:
        #     black_move.append((last_board_, black_res))
        host_GO.visualize_board()

        # white
        go = my_player3_0_1.Go(2, last_board_, cur_board_)

        white_player.set_go(go)
        white_res = white_player.get_move()
        # white_Q = True if len(go.move_list) >= 5 else False

        if white_res == "PASS":
            print("white pass")
            break

        host_GO.set_board(2, last_board_, cur_board_)
        last_board_ = deepcopy(cur_board_)
        host_GO.place_chess(white_res[0], white_res[1], 2)
        host_GO.died_pieces = host_GO.remove_died_pieces(1)

        cur_board_ = host_GO.board

        white_state_action_list.append((last_board_, white_res, deepcopy(cur_board_)))

        host_GO.visualize_board()

    # black_player.learn(black_state_action_list)
    white_player.learn(white_state_action_list)

for j in range(10):
    # for i in range(10):
    #     black_random_learn()
    #     # white_random_learn()
    #     # learn_loop()
    #     print(i)
    #
    # for i in range(10):
    #     # black_random_learn()
    #     white_random_learn()
    #     # learn_loop()
    #     print(i)

    for i in range(100):
        # black_random_learn()
        # white_random_learn()
        learn_loop(i)
        print(i)


