# Alpha-Beta search by Fei Li
import Const
from AI_base import *


class AI_search(AI_base):

    def __init__(self):
        AI_base.__init__(self)
        self.max_depth = 5
        self.visited = {}
        self.moves = {}

    def get_hash(self, board, is_red):
        return board.hash(is_red)

    def select_move(self, board, is_red):
        hash_val = self.get_hash(board, is_red)
        if hash_val in self.visited:
            return self.visited[hash_val]
        if len(board.pieces) > 18:
            value, move = self.dfs(board, self.max_depth - 1, -Const.inf, Const.inf, is_red)
        elif len(board.pieces) > 10:
            value, move = self.dfs(board, self.max_depth, -Const.inf, Const.inf, is_red)
        else:
            value, move = self.dfs(board, self.max_depth + 1, -Const.inf, Const.inf, is_red)
        self.visited[hash_val] = move
        return move

    def dfs(self, board, depth, alpha, beta, is_red):
        value = self.eval_board(board)
        if depth == 0 or value > Const.inf or value < -Const.inf:
            return value, None
        if is_red:
            bst_v = -Const.inf
            bst_m = None
            hash_val = self.get_hash(board, is_red)
            if hash_val in self.moves:
                moves = self.moves[hash_val]
            else:
                moves = board.get_all_moves(is_red)
                moves = sorted(moves, key=lambda x: self.eval_move(board, x, is_red), reverse=True)
                self.moves[hash_val] = moves
            for move in moves:
                nx = move[0] + move[2]
                ny = move[1] + move[3]
                removed_piece = None
                if (nx, ny) in board.pieces:
                    removed_piece = board.pieces[nx, ny]
                board.move(move[0], move[1], move[2], move[3], is_calc=True)
                hash_val = self.get_hash(board, not is_red)
                if hash_val not in self.visited:
                    cur_v, cur_m = self.dfs(board, depth - 1, alpha, beta, not is_red)
                    if cur_v > bst_v:
                        bst_v = cur_v
                        bst_m = move
                    if bst_v > alpha:
                        alpha = bst_v
                board.move(nx, ny, -move[2], -move[3], is_calc=True)
                if removed_piece is not None:
                    board.pieces[nx, ny] = removed_piece
                if beta <= alpha:
                    break
            return bst_v, bst_m
        else:
            bst_v = Const.inf
            bst_m = None
            moves = board.get_all_moves(is_red)
            moves = sorted(moves, key=lambda x: self.eval_move(board, x, is_red), reverse=True)
            for move in moves:
                nx = move[0] + move[2]
                ny = move[1] + move[3]
                removed_piece = None
                if (nx, ny) in board.pieces:
                    removed_piece = board.pieces[nx, ny]
                board.move(move[0], move[1], move[2], move[3], is_calc=True)
                hash_val = self.get_hash(board, not is_red)
                if hash_val not in self.visited:
                    cur_v, cur_m = self.dfs(board, depth - 1, alpha, beta, not is_red)
                    if cur_v < bst_v:
                        bst_v = cur_v
                        bst_m = move
                    if bst_v < beta:
                        beta = bst_v
                board.move(nx, ny, -move[2], -move[3], is_calc=True)
                if removed_piece is not None:
                    board.pieces[nx, ny] = removed_piece
                if beta <= alpha:
                    break
            return bst_v, bst_m
