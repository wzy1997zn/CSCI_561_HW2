from copy import deepcopy
from multiprocessing import Pool, Manager
import multiprocessing

from competition.player1.my_player3_0_1 import QLearner as p1
from competition.player2.my_player3_0_1 import QLearner as p2
from competition.player3.my_player3_0_1 import QLearner as p3
from competition.player4.my_player3_0_1 import QLearner as p4
from competition.player5.my_player3_0_1 import QLearner as p5
from competition.player6.my_player3_0_1 import QLearner as p6
from competition.Random.RandomPlayer import RandomPlayer as p7
from competition.player1.my_player3_0_1 import Go as GO
import host

import time


black_player_pool = [p1,p2,p3,p4,p5,p6,p7]
white_player_pool = [p1,p2,p3,p4,p5,p6,p7]
player_count = len(black_player_pool)




def learn_loop(x, round, home_court, win_black, win_white, lock):
    # print("====================")
    # print("black:" + str(x))
    # print("white:" + str((x + 1 + round) % player_count))
    # print("====================")

    my_player_ = 1
    last_board_ = [[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0]]
    cur_board_ = [[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0]]

    # black_player = get_player(x)

    b_num = 0
    w_num = 0
    if home_court:
        b_num = x
        w_num = (x + 1 + round) % player_count
        print("====================")
        print("round:" + str(round))
        print("black:" + str(x))
        print("white:" + str((x + 1 + round) % player_count))
        print("====================")

    if not home_court:
        b_num = (x + 1 + round) % player_count
        w_num = x
        print("====================")
        print("round:" + str(round))
        print("black:" + str(b_num))
        print("white:" + str(w_num))
        print("====================")

    black_player = black_player_pool[b_num]()
    white_player = white_player_pool[w_num]()


    host_GO = host.GO(5)

    black_state_action_list = []
    white_state_action_list = []

    black_cur_board = None
    black_move = None
    black_res_board = None

    white_cur_board = None
    white_move = None
    white_res_board = None

    for i in range(12):

        # black
        interval_b = time.time()
        go = GO(my_player_, last_board_, cur_board_)

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

        black_cur_board = deepcopy(last_board_)
        black_move = black_res
        white_res_board = deepcopy(cur_board_)

        if white_cur_board is not None and white_move is not None and white_res_board is not None:
            white_state_action_list.append((white_cur_board, white_move, white_res_board))
        white_cur_board = None
        white_move = None
        white_res_board = None

        host_GO.visualize_board()
        print(time_b)

        # white
        interval_w = time.time()
        go = GO(2, last_board_, cur_board_)

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

        white_cur_board = deepcopy(last_board_)
        white_move = white_res
        black_res_board = deepcopy(cur_board_)

        if black_cur_board is not None and black_move is not None and black_res_board is not None:
            black_state_action_list.append((black_cur_board, black_move, black_res_board))
        black_cur_board = None
        black_move = None
        black_res_board = None

        host_GO.visualize_board()
        print(time_w)

    lock.acquire()
    winner = host_GO.judge_winner()
    if winner == 1:
        # with lock:
        win_black[b_num] += 1
    elif winner == 2:
        # with lock:
        win_white[w_num] += 1
    lock.release()

    black_player.learn(black_state_action_list)
    white_player.learn(white_state_action_list)


def tournament():
    # player_count = 2
    for season in range(1):
        print("season" + str(season))
        # learn_loop(0,0,True)
        for round in range(player_count):
            # black_random_learn()
            # white_random_learn()
            pool = Pool(processes=8)
            for x in range(player_count):
                pool.apply_async(learn_loop, args=(x, round, True, winblack, winwhite, lock))
                pool.apply_async(learn_loop, args=(x, round, False, winblack, winwhite, lock))
            pool.close()
            pool.join()
        with open("win_count.txt", 'w') as f:
            f.write(str(winblack) + "\n")
            f.write(str(winwhite) + "\n")
    print(winblack)
    print(winwhite)


def test():
    learn_loop(5, 1, False, winblack, winwhite, lock)
    print(winblack)
    print(winwhite)


if __name__ == "__main__":
    manager = Manager()
    winblack = manager.list([0] * player_count)
    winwhite = manager.list([0] * player_count)
    lock = manager.Lock()

    # tournament()
    test()







