# 6853115445: Ziyue Wang

"""
constants
"""
BOARD_SIZE = 5
INPUT = "input.txt"
OUTPUT = "output.txt"


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
        self.move_list = self.get_all_possible_move(self)

        self.test_board = []  # be used when checking a place is possible or not NEED deepcopy and careful using

    def get_all_possible_move(self):
        """
        check all 0s and find all
          1. have liberty
          2. no liberty but can kill enemy and not violate KO rule
        :return: a list of possible moves on the board
        """

        pass

    def check_if_no_liberty(self, place=(-1,-1)):
        """
        first rule of possibility. get all neighbor ally and check if someone has liberty after putting here.
        it will also be used when checking if a move can kill someone.
        :param place: checking place
        :return: boolean, true if cur place and its neighbor allies still have liberties
        """

        pass

    def get_all_neighbor_ally(self, place=(-1,-1)):
        """
        use dfs, find all linking neighbors having same color with checking place
        :param place: checking place
        :return: a list of neighbor allies
        """

        pass

    def get_neighbor_ally(self, place=(-1,-1)):
        """
        dfs util method, find direct neighbor allies
        :param place: cur checking place
        :return: a list of up to 4 neighbor allies
        """
        pass

    def get_neighbor(self, place=(-1,-1)):
        """
        simple getting direct neighbors
        :param place: cur checking place
        :return: a list of direct neighbors
        """
        pass

    def get_liberty(self, place=(-1,-1)):
        """
        get liberties of cur place stone
        :param place: cur stone
        :return: num of liberties
        """

    def check_if_kill_other(self,place=(-1,-1)):
        """
        if this place not possible because no liberty, it still possible if it can kill other
        get all not ally neighbors and check their liberty
        :param place: cur placing
        :return: boolean, true if some neighbors die after cur moving
        """
        pass

    def check_KO(self):
        """
        if the board will be same with last board then this move invalid.
        this only happens when kill some stone
        :return: boolean, true if violate KO rule
        """
        pass


class RandomPlayer:
    def __init__(self, move_list):
        self.move_list = move_list

    def get_move(self):
        from random import choice
        return choice(self.move_list)


def get_result(go):
    strategy = RandomPlayer(go.move_list)
    result = strategy.get_move()
    return result


def read():
    with open(INPUT, 'r') as f:
        lines = f.readlines()
        my_player = int(lines[0])
        last_board = []
        cur_board = []
        for i in range(1,BOARD_SIZE+1):
            cur_line = [int(x) for x in lines[i].strip()]
            last_board.append(cur_line)
        for i in range(BOARD_SIZE+1, BOARD_SIZE+BOARD_SIZE+1):
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
        f.close()


if __name__ == '__main__':
    my_player, last_board, cur_board = read()
    print()
