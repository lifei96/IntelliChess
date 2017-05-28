import random


class AI_random():

    def __init__(self):
        pass

    def select_move(self, board, is_red):
        moves = board.get_all_moves(is_red)
        if moves is not []:
            return random.choice(moves)
        else:
            return None
