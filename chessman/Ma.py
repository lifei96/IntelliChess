from ChessPiece import ChessPiece


class Ma(ChessPiece):

    def get_image_file_name(self):
        if self.selected:
            if self.is_red:
                return "images/RNS.gif"
            else:
                return "images/BNS.gif"
        else:
            if self.is_red:
                return "images/RN.gif"
            else:
                return "images/BN.gif"

    def can_move(self, board, dx, dy):
        x, y = self.x, self.y
        nx, ny = x+dx, y+dy
        if nx < 0 or nx > 8 or ny < 0 or ny > 9:
            return False
        if dx == 0 or dy == 0:
            #print 'no straight'
            return False
        if abs(dx) + abs(dy) !=3:
            #print 'not normal'
            return False
        if (nx, ny) in board.pieces:
            if board.pieces[nx, ny].is_red == self.is_red:
                #print 'blocked by yourself'
                return False
        if (x if abs(dx) ==1 else x+dx/2, y if abs(dy) ==1 else y+ (dy/2)) in board.pieces:
            #print 'blocked'
            return False
        return True

    #below added by Fei Li

    def __init__(self, x, y, is_red):
        ChessPiece.__init__(self, x, y, is_red)
        self.name = 'Ma'
        if self.is_red:
            self.ID = 8
        else:
            self.ID = 9
        self.dx = [-1, -1, 1, 1, -2, -2, 2, 2]
        self.dy = [-2, 2, -2, 2, -1, 1, -1, 1]

    def get_moves(self, board):
        moves = []
        for i in range(8):
            if self.can_move(board, self.dx[i], self.dy[i]):
                moves.append((self.x, self.y, self.dx[i], self.dy[i]))
        return moves
