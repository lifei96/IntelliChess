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
        hash_val = hash(board)
        if hash_val in self.eval_dict:
            return self.eval_dict[hash_val]
        eval_sum = 0
        for (x, y) in board.pieces:
            piece_name = board.pieces[x, y].name()
            is_red = board.pieces[x, y].is_red
            if is_red:
                eval_sum += self.pieces_eval[piece_name]
                eval_sum += self.position_eval[piece_name][x][y]
            else:
                eval_sum -= self.pieces_eval[piece_name]
                eval_sum -= self.position_eval[piece_name][x][9 - y]
        self.eval_dict[hash_val] = eval_sum
        return eval_sum
