from copy import deepcopy

import my_player3_0_1
import host


def learn_loop():
    my_player_ = 1
    last_board_ = [[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0]]
    cur_board_ = [[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0]]

    black_player = my_player3_0_1.QLearner()
    white_player = my_player3_0_1.QLearner()

    host_GO = host.GO(5)

    black_state_action_list = []
    white_state_action_list = []

    for i in range(24):

        # black
        go = my_player3_0_1.Go(my_player_, last_board_, cur_board_)

        black_player.set_go(go)
        black_res = black_player.get_move()

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

        white_player.set_go(go)
        white_res = white_player.get_move()

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

    black_player.learn(black_state_action_list)
    white_player.learn(white_state_action_list)


for i in range(1000):
    learn_loop()
    print(i)




