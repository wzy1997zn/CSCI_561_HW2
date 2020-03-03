# 6853115445: Ziyue Wang

"""
constants
"""
BOARD_SIZE = 5


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
