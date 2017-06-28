from ChessBoard import *
from ChessView import *
from AIDict import *
import time
import Const
import argparse
import numpy as np


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
    time_red = []
    time_green = []

    def __init__(self):
        self.view = ChessView(self)
        self.view.showMsg("Red")
        self.view.draw_board(self.board)
        self.view.root.update()

    def start(self, game_mode, AI_red=None, AI_green=None):
        # below added by Fei Li
        self.game_mode = game_mode
        if game_mode == 1:
            if AI_red in self.AI_dict.AI:
                self.AI_red = self.AI_dict.AI[AI_red]
                print '-----Round %d-----' % self.cur_round
                self.perform_AI(self.AI_red)
                self.view.draw_board(self.board)
                self.change_player(not self.player_is_red)
            else:
                self.view.showMsg('Please enter a correct AI name')
                self.view.draw_board(self.board)
                self.view.root.update()
                self.quit()
                return
        elif game_mode == 2:
            if AI_red in self.AI_dict.AI and AI_green in self.AI_dict.AI:
                self.AI_red = self.AI_dict.AI[AI_red]
                self.AI_green = self.AI_dict.AI[AI_green]
                print '-----Round %d-----' % self.cur_round
                self.perform_AI(self.AI_red)
                self.view.draw_board(self.board)
            else:
                self.view.showMsg('Please enter correct AI names')
                self.view.draw_board(self.board)
                self.view.root.update()
                self.quit()
                return
        else:
            print '-----Round %d-----' % self.cur_round
        self.view.start()

    def callback(self, event):
        if self.game_mode == 1 and self.player_is_red:
            return
        if self.game_mode == 2:
            return
        rx, ry = real_coord(event.x), real_coord(event.y)
        change = self.board.select(rx, ry, self.player_is_red)
        self.view.draw_board(self.board)
        if self.check_end(self.board):
            self.view.root.update()
            self.quit()
            return
        if change:
            performed = self.change_player(not self.player_is_red)
            if performed:
                self.view.draw_board(self.board)
                if self.check_end(self.board):
                    self.view.root.update()
                    self.quit()
                    return
                self.change_player(not self.player_is_red)

    # below added by Fei Li

    def quit(self):
        time.sleep(Const.end_delay)
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
            self.view.root.update()
            print '*****\n*****'
            with open('GameLog.txt', 'a') as f:
                if len(self.time_red) > 0:
                    avg_red = np.mean(self.time_red)
                else:
                    avg_red = 0.0
                if len(self.time_green) > 0:
                    avg_green = np.mean(self.time_green)
                else:
                    avg_green = 0.0
                f.write('%d\t%d\t%f\t%f\n' % (0, self.cur_round, avg_red, avg_green))
            return True
        elif not green_king:
            print '*****\n*****'
            self.view.showMsg('*****Red Wins at Round %d*****' % self.cur_round)
            self.view.root.update()
            print '*****\n*****'
            with open('GameLog.txt', 'a') as f:
                if len(self.time_red) > 0:
                    avg_red = np.mean(self.time_red)
                else:
                    avg_red = 0.0
                if len(self.time_green) > 0:
                    avg_green = np.mean(self.time_green)
                else:
                    avg_green = 0.0
                f.write('%d\t%d\t%f\t%f\n' % (1, self.cur_round, avg_red, avg_green))
            return True
        elif self.cur_round >= 200:
            print '*****\n*****'
            self.view.showMsg('*****Draw at Round %d*****' % self.cur_round)
            self.view.root.update()
            print '*****\n*****'
            with open('GameLog.txt', 'a') as f:
                if len(self.time_red) > 0:
                    avg_red = np.mean(self.time_red)
                else:
                    avg_red = 0.0
                if len(self.time_green) > 0:
                    avg_green = np.mean(self.time_green)
                else:
                    avg_green = 0.0
                f.write('%f\t%d\t%f\t%f\n' % (0.5, self.cur_round, avg_red, avg_green))
            return True
        return False

    def change_player(self, player_now):
        self.player_is_red = player_now
        if player_now:
            self.cur_round += 1
            print '-----Round %d-----' % self.cur_round
        self.view.showMsg("Red" if self.player_is_red else "Green")
        self.view.root.update()
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
        print '...AI is calculating...'
        START_TIME = time.clock()
        move = AI.select_move(self.board, self.player_is_red)
        time_used = time.clock() - START_TIME
        print '...Use %fs...' % time_used
        if self.player_is_red:
            self.time_red.append(time_used)
        else:
            self.time_green.append(time_used)
        if move is not None:
            self.board.move(move[0], move[1], move[2], move[3])
        else:
            self.view.showMsg('Can not move')
            self.view.root.update()
            if self.player_is_red:
                print '*****\n*****'
                self.view.showMsg('*****Red can not move at Round %d*****' % self.cur_round)
                self.view.root.update()
                print '*****\n*****'
            else:
                print '*****\n*****'
                self.view.showMsg('*****Green can not move at Round %d*****' % self.cur_round)
                self.view.root.update()
                print '*****\n*****'

    def game_mode_2(self):
        self.change_player(not self.player_is_red)
        self.view.draw_board(self.board)
        self.view.root.update()
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
                    nargs='?', default=0, type=float, required=False,
                    help='Set how many seconds you want to delay after each move')
parser.add_argument('-ed', dest='end_delay', action='store',
                    nargs='?', default=3, type=float, required=False,
                    help='Set how many seconds you want to delay after the end of game')
args = parser.parse_args()

Const.delay = args.delay
Const.end_delay = args.end_delay

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
