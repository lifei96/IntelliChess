# Base class for AI by Fei Li
import board_eval


class AI_base:

    pieces_eval = board_eval.strength
    position_eval = board_eval.position

    eval_dict = {}

    def __init__(self):
        pass

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
        val = (self.position_eval[board.pieces[move[0], move[1]].name][move[0] + move[2]][move[1] + move[3]] -
               self.position_eval[board.pieces[move[0], move[1]].name][move[0]][move[1]])*10
        if is_red:
            val += move[3] * 10 + abs(move[2])
        else:
            val += -move[3] * 10 + abs(move[2])
        if (move[0] + move[2], move[1] + move[3]) in board.pieces:
            piece_name = board.pieces[move[0] + move[2], move[1] + move[3]].name
            val += self.pieces_eval[piece_name] * 10
        return val
