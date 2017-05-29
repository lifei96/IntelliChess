from ChessPiece import ChessPiece


class Shuai(ChessPiece):

    is_king = True

    def get_image_file_name(self):
        if self.selected:
            if self.is_red:
                return "images/RKS.gif"
            else:
                return "images/BKS.gif"
        else:
            if self.is_red:
                return "images/RK.gif"
            else:
                return "images/BK.gif"

    def can_move(self, board, dx, dy):
        # print 'king'
        nx, ny = self.x + dx, self.y + dy
        if nx < 0 or nx > 8 or ny < 0 or ny > 9:
            return False
        if (nx, ny) in board.pieces:
            if board.pieces[nx, ny].is_red == self.is_red:
                #print 'blocked by yourself'
                return False
        if dx == 0 and self.count_pieces(board, self.x, self.y, dx, dy) == 0 and ((nx, ny) in board.pieces) and board.pieces[nx, ny].is_king:
            return True
        if not (self.is_red and 3 <= nx <=5 and 0<= ny <=2) and not (self.is_red == False and 3 <= nx <= 5 and 7 <= ny <= 9):
            # print 'out of castle'
            return False
        if abs(dx) + abs(dy) !=1:
            # print 'too far'
            return False
        return True

    #below added by Fei Li

    def __init__(self, x, y, is_red):
        ChessPiece.__init__(self, x, y, is_red)
        self.name = 'Shuai'
        if self.is_red:
            self.ID = 0
        else:
            self.ID = 1
        self.dx = [0, 0, -1, 1]
        self.dy = [-1, 1, 0, 0]

    def get_moves(self, board):
        moves = []
        for i in range(4):
            if self.can_move(board, self.dx[i], self.dy[i]):
                moves.append((self.x, self.y, self.dx[i], self.dy[i]))
        if self.is_red:
            for nx in range(3, 6):
                for ny in range(7, 10):
                    if self.can_move(board, nx - self.x, ny - self.y):
                        moves.append((self.x, self.y, nx - self.x, ny - self.y))
        else:
            for nx in range(3, 6):
                for ny in range(0, 3):
                    if self.can_move(board, nx - self.x, ny - self.y):
                        moves.append((self.x, self.y, nx - self.x, ny - self.y))
        return moves
