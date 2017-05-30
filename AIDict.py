from AI_random import *
from AI_search import *
from AI_MCTS import *

class AIDict():

    AI = {}

    def __init__(self):
        self.AI = {'AI_random': AI_random(),
                   'AI_search': AI_search(),
                   'AI_MCTS': AI_MCTS()}
