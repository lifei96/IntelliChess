import Const
from AI_base import *


class AI_search(AI_base):

    max_depth = 3

    visited = {}

    def __init__(self):
        AI_base.__init__(self)

    def select_move(self, board, is_red):
        hash_val = hash(board)
        if (hash_val, is_red) in self.visited:
            return self.visited[(hash_val, is_red)]
        value, move = self.dfs(board, self.max_depth, -Const.inf, Const.inf, is_red)
        self.visited[(hash_val, is_red)] = move
        return move

    def dfs(self, board, depth, alpha, beta, is_red):
        value = self.eval_board(board)
        if depth == 0 or value > Const.inf or value < -Const.inf:
            return value, None
        if is_red:
            bst_v = -Const.inf
            bst_m = None
            moves = board.get_all_moves(is_red)
            moves = sorted(moves, key=lambda x: self.eval_move(board, x), reverse=True)
            for move in moves:
                new_board = self.next_board(board, move)
                hash_val = hash(new_board)
                if (hash_val, not is_red) in self.visited:
                    continue
                cur_v, cur_m = self.dfs(new_board, depth - 1, alpha, beta, not is_red)
                if cur_v > bst_v:
                    bst_v = cur_v
                    bst_m = move
                if bst_v > alpha:
                    alpha = bst_v
                if beta <= alpha:
                    break
            return bst_v, bst_m
        else:
            bst_v = Const.inf
            bst_m = None
            moves = board.get_all_moves(is_red)
            moves = sorted(moves, key=lambda x: self.eval_move(board, x), reverse=True)
            for move in moves:
                new_board = self.next_board(board, move)
                hash_val = hash(new_board)
                if (hash_val, not is_red) in self.visited:
                    continue
                cur_v, cur_m = self.dfs(new_board, depth - 1, alpha, beta, not is_red)
                if cur_v < bst_v:
                    bst_v = cur_v
                    bst_m = move
                if bst_v < beta:
                    beta = bst_v
                if beta <= alpha:
                    break
            return bst_v, bst_m
