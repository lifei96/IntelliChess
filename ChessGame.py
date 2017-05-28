from ChessBoard import *
from ChessView import *
from AIDict import *
import time
import Const
import argparse


def real_coord(x):
    if x <= 50:
        return 0
    else:
        return (x-50)/40 + 1


def board_coord(x):
    return 30 + 40*x


class ChessGame:

    board = ChessBoard()
    player_is_red = True
    cur_round = 1
    game_mode = 0  # 0:HUMAN VS HUMAN 1:HUMAN VS AI 2:AI VS AI
    AI_red = None
    AI_green = None
    AI_dict = AIDict()

    def __init__(self):
        self.view = ChessView(self)
        self.view.showMsg("Red")
        self.view.draw_board(self.board)

    def start(self, game_mode, AI_red=None, AI_green=None):
        # below added by Fei Li
        self.game_mode = game_mode
        if game_mode == 1:
            if AI_red in self.AI_dict.AI:
                self.AI_red = self.AI_dict.AI[AI_red]
                self.perform_AI(self.AI_red)
                self.view.draw_board(self.board)
                self.change_player(not self.player_is_red)
            else:
                self.view.showMsg('Please enter a correct AI name')
                self.quit()
                return
        elif game_mode == 2:
            if AI_red in self.AI_dict.AI and AI_green in self.AI_dict.AI:
                self.AI_red = self.AI_dict.AI[AI_red]
                self.AI_green = self.AI_dict.AI[AI_green]
                self.perform_AI(self.AI_red)
                self.view.draw_board(self.board)
            else:
                self.view.showMsg('Please enter correct AI names')
                self.quit()
                return
        self.view.start()

    def callback(self, event):
        if self.game_mode == 1 and self.player_is_red:
            return
        if self.game_mode == 2:
            return
        # print event.x, event.y
        rx, ry = real_coord(event.x), real_coord(event.y)
        change = self.board.select(rx, ry, self.player_is_red)
        self.view.draw_board(self.board)
        if self.check_end(self.board):
            self.view.root.update()
            time.sleep(Const.delay)
            self.quit()
            return
        if change:
            performed = self.change_player(not self.player_is_red)
            if performed:
                self.view.draw_board(self.board)
                if self.check_end(self.board):
                    self.view.root.update()
                    time.sleep(Const.delay)
                    self.quit()
                    return
                self.change_player(not self.player_is_red)

    # below added by Fei Li

    def quit(self):
        self.view.quit()

    def check_end(self, board):
        red_king = False
        green_king = False
        pieces = board.pieces
        for (x, y) in pieces.keys():
            if pieces[x, y].is_king:
                if pieces[x, y].is_red:
                    red_king = True
                else:
                    green_king = True
        if not red_king:
            print '*****\n*****'
            self.view.showMsg('*****Green Wins at Round %d*****' % self.cur_round)
            print '*****\n*****'
            return True
        elif not green_king:
            print '*****\n*****'
            self.view.showMsg('*****Red Wins at Round %d*****' % self.cur_round)
            print '*****\n*****'
            return True
        return False

    def change_player(self, player_now):
        self.player_is_red = player_now
        if player_now:
            self.cur_round += 1
        self.view.showMsg("Red" if self.player_is_red else "Green")
        if self.game_mode == 0:
            return False
        if self.game_mode == 1:
            if self.player_is_red:
                self.perform_AI(self.AI_red)
                return True
            return False
        elif self.game_mode == 2:
            if self.player_is_red:
                self.perform_AI(self.AI_red)
            else:
                self.perform_AI(self.AI_green)
            return True
        return False

    def perform_AI(self, AI):
        move = AI.select_move(self.board, self.player_is_red)
        if move is not None:
            self.board.move(move[0], move[1], move[2], move[3])
        else:
            self.view.showMsg('Can not move')
            self.quit()

    def game_mode_2(self):
        self.change_player(not self.player_is_red)
        self.view.draw_board(self.board)
        if self.check_end(self.board):
            return True
        return False


parser = argparse.ArgumentParser(description='Chinese Chess with AI')
parser.add_argument('-m', dest='mode', action='store',
                    nargs='?', default=0, type=int, choices=[0, 1, 2], required=True,
                    help='0: HUMAN VS HUMAN, 1: HUMAN VS AI, 2: AI VS AI')
parser.add_argument('-a', dest='ai', action='store',
                    nargs='*', default=[], type=str, required=False, help='Choose AI used in the game')
parser.add_argument('-d', dest='delay', action='store',
                    nargs='?', default=1, type=float, required=False,
                    help='Set how many seconds you want to delay after each move')
args = parser.parse_args()

Const.delay = args.delay

if args.mode == 0:
    if len(args.ai) != 0:
        print 'Please do not enter AI names'
    else:
        game = ChessGame()
        game.start(args.mode)
elif args.mode == 1:
    if len(args.ai) != 1:
        print 'Please enter an AI name'
    else:
        game = ChessGame()
        game.start(args.mode, AI_red=args.ai[0])
else:
    if len(args.ai) != 2:
        print 'Please enter two AI names'
    else:
        game = ChessGame()
        game.start(args.mode, AI_red=args.ai[0], AI_green=args.ai[1])
