from AI_base import *
import random


class AI_random(AI_base):

    def __init__(self):
        AI_base.__init__(self)

    def select_move(self, board, is_red):
        moves = board.get_all_moves(is_red)
        if moves is not []:
            return random.choice(moves)
        else:
            return None
