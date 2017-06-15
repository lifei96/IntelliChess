from AI_random import *
from AI_search import *
from AI_MCTS import *
from AI_MCTSV import *


class AIDict():

    AI = {}

    def __init__(self):
        self.AI = {'AI_random': AI_random(),
                   'AI_search': AI_search(),
                   'AI_MCTS': AI_MCTS(),
                   'AI_MCTSV': AI_MCTSV()}
