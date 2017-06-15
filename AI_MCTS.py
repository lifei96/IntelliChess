# MCTS with UCB equation by Fei Li
import Const
from AI_base import *
import time
import math
import random


class AI_MCTS(AI_base):

    def __init__(self, C=0.9, time_limit=5, R=15, E=5):
        AI_base.__init__(self)
        self.C = C
        self.time_limit = time_limit
        self.R = R
        self.E = E
        self.V = {}
        self.N = {}
        self.moves = {}
        self.expanded_pos = {}
        self.expanded = set()
        self.visited = set()
        self.seq = set()
        self.vis = set()

    def select_move(self, board, is_red):
        return self.UCT_search(board, is_red)

    def get_node(self, board, is_red):
        return board.hash(is_red)

    def update(self, node, v_delta, n_delta):
        self.V[node] += v_delta
        self.N[node] += n_delta

    def UCB(self, node, next_node, is_red):
        if is_red:
            return float(self.V[next_node]) / self.N[next_node] \
                   + self.C * math.sqrt(math.log(self.N[node]) / self.N[next_node])
        else:
            return float(self.N[next_node] - self.V[next_node]) / self.N[next_node] \
                   + self.C * math.sqrt(math.log(self.N[node]) / self.N[next_node])

    def best_move(self, board, is_red):
        best_m = None
        best_UCB = None
        node = self.get_node(board, is_red)
        if node not in self.moves:
            moves = board.get_all_moves(is_red)
            moves = sorted(moves, key=lambda x: self.eval_move(board, x, is_red), reverse=True)
            self.moves[node] = moves
            self.expanded_pos[node] = 0
        for move in self.moves[node]:
            nx = move[0] + move[2]
            ny = move[1] + move[3]
            removed_piece = None
            if (nx, ny) in board.pieces:
                removed_piece = board.pieces[nx, ny]
            board.move(move[0], move[1], move[2], move[3], is_calc=True)
            next_node = self.get_node(board, not is_red)
            if next_node not in self.visited and next_node in self.N and node in self.N:
                cur_UCB = self.UCB(node, next_node, is_red)
                if best_m is None or cur_UCB > best_UCB:
                    best_m = move
                    best_UCB = cur_UCB
            board.move(nx, ny, -move[2], -move[3], is_calc=True)
            if removed_piece is not None:
                board.pieces[nx, ny] = removed_piece
        #print best_UCB
        return best_m

    def UCT_search(self, board, is_red):
        node = self.get_node(board, is_red)
        self.visited.add(node)
        if node not in self.V or node not in self.N:
            self.V[node] = 0
            self.N[node] = 0
        cnt = 0
        START_TIME = time.clock()
        while time.clock() - START_TIME < self.time_limit:
            cnt += 1
            self.seq.clear()
            self.selection(board, is_red)
        print cnt
        print len(self.expanded)
        return self.best_move(board, is_red)

    def selection(self, board, is_red):
        node = self.get_node(board, is_red)
        self.seq.add(node)
        if node not in self.expanded:
            v_delta, n_delta = self.expansion(board, is_red)
            for pre_node in self.seq:
                self.update(pre_node, v_delta, n_delta)
        else:
            move = self.best_move(board, is_red)
            if move is None:
                return
            nx = move[0] + move[2]
            ny = move[1] + move[3]
            removed_piece = None
            if (nx, ny) in board.pieces:
                removed_piece = board.pieces[nx, ny]
            board.move(move[0], move[1], move[2], move[3], is_calc=True)
            self.selection(board, not is_red)
            board.move(nx, ny, -move[2], -move[3], is_calc=True)
            if removed_piece is not None:
                board.pieces[nx, ny] = removed_piece

    def expansion(self, board, is_red):
        v_delta = 0
        n_delta = 0
        node = self.get_node(board, is_red)
        ter = self.terminate(board)
        if ter == -1:
            if node not in self.moves:
                moves = board.get_all_moves(is_red)
                moves = sorted(moves, key=lambda x: self.eval_move(board, x, is_red), reverse=True)
                self.moves[node] = moves
                self.expanded_pos[node] = 0
            cur_pos = self.expanded_pos[node]
            max_pos = len(self.moves[node])
            for i in range(self.E):
                if cur_pos + i >= max_pos:
                    break
                move = self.moves[node][cur_pos + i]
                nx = move[0] + move[2]
                ny = move[1] + move[3]
                removed_piece = None
                if (nx, ny) in board.pieces:
                    removed_piece = board.pieces[nx, ny]
                board.move(move[0], move[1], move[2], move[3], is_calc=True)
                next_node = self.get_node(board, not is_red)
                if next_node not in self.visited and next_node not in self.seq:
                    res = self.simulation(board, not is_red, 0)
                    if res != -1:
                        v_delta += res
                        n_delta += 1
                        if next_node not in self.V or next_node not in self.N:
                            self.V[next_node] = 0
                            self.N[next_node] = 0
                        self.V[next_node] += res
                        self.N[next_node] += 1
                    else:
                        v_delta += 0.5
                        n_delta += 1
                board.move(nx, ny, -move[2], -move[3], is_calc=True)
                if removed_piece is not None:
                    board.pieces[nx, ny] = removed_piece
            self.expanded_pos[node] = min(cur_pos + self.E, max_pos)
            if self.expanded_pos[node] == max_pos:
                self.expanded.add(node)
        elif ter == 0:
            n_delta = 1
        else:
            v_delta = 1
            n_delta = 1
        return v_delta, n_delta

    def simulation(self, board, is_red, cnt):
        if cnt > self.R:
            return -1
        node = self.get_node(board, is_red)
        self.vis.clear()
        self.vis.add(node)
        ter = self.terminate(board)
        if ter == -1:
            for i in range(10):
                move = self.pick(board, is_red)
                nx = move[0] + move[2]
                ny = move[1] + move[3]
                removed_piece = None
                if (nx, ny) in board.pieces:
                    removed_piece = board.pieces[nx, ny]
                board.move(move[0], move[1], move[2], move[3], is_calc=True)
                next_node = self.get_node(board, not is_red)
                if next_node not in self.visited and next_node not in self.seq and next_node not in self.vis:
                    res = self.simulation(board, not is_red, cnt + 1)
                    board.move(nx, ny, -move[2], -move[3], is_calc=True)
                    if removed_piece is not None:
                        board.pieces[nx, ny] = removed_piece
                    return res
                board.move(nx, ny, -move[2], -move[3], is_calc=True)
                if removed_piece is not None:
                    board.pieces[nx, ny] = removed_piece
            return -1
        else:
            return ter

    def pick(self, board, is_red):
        node = self.get_node(board, is_red)
        if node not in self.moves:
            moves = board.get_all_moves(is_red)
            moves = sorted(moves, key=lambda x: self.eval_move(board, x, is_red), reverse=True)
            self.moves[node] = moves
            self.expanded_pos[node] = 0
        if self.eval_move(board, self.moves[node][0], is_red) > Const.inf:
            return self.moves[node][0]
        tot = len(self.moves[node])
        rand_res = random.random()
        if rand_res < 0.3:
            stop = min(int(tot * 0.4 + 1.0), tot)
            return self.moves[node][random.randrange(0, stop)]
        elif rand_res < 0.7:
            stop = min(int(tot * 0.8 + 1.0), tot)
            return self.moves[node][random.randrange(0, stop)]
        else:
            stop = tot
            return self.moves[node][random.randrange(0, stop)]

    def terminate(self, board):
        red_king = False
        green_king = False
        for x, y in board.pieces:
            if board.pieces[x, y].is_king:
                if board.pieces[x, y].is_red:
                    red_king = True
                else:
                    green_king = True
        if red_king and green_king:
            return -1
        if red_king:
            return 1
        return 0

    def next_board(self, board, move):
        new_board = board.deepcopy()
        new_board.move(move[0], move[1], move[2], move[3], is_calc=True)
        return new_board

    def eval_board(self, board):
        hash_val = board.hash(True)
        if hash_val in self.eval_dict:
            return self.eval_dict[hash_val]
        eval_sum = 0
        piece_num = len(board.pieces)
        for (x, y) in board.pieces:
            piece_name = board.pieces[x, y].name
            is_red = board.pieces[x, y].is_red
            if is_red:
                eval_sum += self.pieces_eval[piece_name] * (min(2, 32.0 / piece_num))
                eval_sum += self.position_eval[piece_name][x][y] * (max(0.5, piece_num / 32.0))
            else:
                eval_sum -= self.pieces_eval[piece_name] * (min(2, 32.0 / piece_num))
                eval_sum -= self.position_eval[piece_name][x][9 - y] * (max(0.5, piece_num / 32.0))
        self.eval_dict[hash_val] = eval_sum
        return eval_sum

    def eval_move(self, board, move, is_red):
        val = self.position_eval[board.pieces[move[0], move[1]].name][move[0] + move[2]][move[1] + move[3]]*10
        if is_red:
            val += move[3] * 10 + abs(move[2])
        else:
            val += -move[3] * 10 + abs(move[2])
        if (move[0] + move[2], move[1] + move[3]) in board.pieces:
            piece_name = board.pieces[move[0] + move[2], move[1] + move[3]].name
            val += self.pieces_eval[piece_name] * 10
        return val
