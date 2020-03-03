
BOARD_SIZE = 5

class Go:
    def __init__(self, last_board, cur_board, my_player):
        self.last_board = last_board
        self.cur_board = cur_board
        self.my_player = my_player

    def get_all_possible_move(self):
        pass

    def check_if_no_liberty(self, place=(-1,-1)):
        # first rule of possibility. get all neighbor ally and check if someone has liberty after putting here.
        pass
    
    def get_liberty(self, place=(-1,-1)):

    def check_if_kill_other(self,place=(-1,-1)):
        # if this place not possible because no liberty, it still possible if it can kill other
        pass

    def check_KO(self,place=(-1,-1)):
        # if the board will be same with last board then this move invalid.
        # this only happens when kill some stone
        pass