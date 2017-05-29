from ChessPiece import ChessPiece


class Xiang(ChessPiece):

    def get_image_file_name(self):
        if self.selected:
            if self.is_red:
                return "images/RBS.gif"
            else:
                return "images/BBS.gif"
        else:
            if self.is_red:
                return "images/RB.gif"
            else:
                return "images/BB.gif"

    def can_move(self, board, dx, dy):
        x,y = self.x, self.y
        nx, ny = x + dx, y + dy
        if nx < 0 or nx > 8 or ny < 0 or ny > 9:
            return False
        if (nx, ny) in board.pieces:
            if board.pieces[nx, ny].is_red == self.is_red:
                #print 'blocked by yourself'
                return False
        if (self.is_red and ny > 4) or (self.is_red== False and ny <5):
            #print 'no river cross'
            return False

        if abs(dx)!=2 or abs(dy)!=2:
            #print 'not normal'
            return False
        sx, sy = dx/abs(dx), dy/abs(dy)
        if (x+sx, y+sy) in board.pieces:
            #print 'blocked'
            return False
        return True

    #below added by Fei Li

    def __init__(self, x, y, is_red):
        ChessPiece.__init__(self, x, y, is_red)
        self.name = 'Xiang'
        if self.is_red:
            self.ID = 4
        else:
            self.ID = 5
        self.dx = [-2, -2, 2, 2]
        self.dy = [-2, 2, -2, 2]

    def get_moves(self, board):
        moves = []
        for i in range(4):
            if self.can_move(board, self.dx[i], self.dy[i]):
                moves.append((self.x, self.y, self.dx[i], self.dy[i]))
        return moves
