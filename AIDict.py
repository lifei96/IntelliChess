from AI_random import *
from AI_search import *


class AIDict():

    AI = {}

    def __init__(self):
        self.AI = {'AI_random': AI_random(),
                   'AI_search': AI_search()}
