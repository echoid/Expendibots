from NeCho.helper import *
from NeCho.agent import MinimaxAgent


class ExamplePlayer:

    def __init__(self, colour):

        self.colour = colour
        self.state = {
            "black": [[1, 0, 7], [1, 1, 7], [1, 3, 7], [1, 4, 7], [1, 6, 7], [1, 7, 7], [1, 0, 6], [1, 1, 6], [1, 3, 6],
                      [1, 4, 6], [1, 6, 6], [1, 7, 6]],
            "white": [[1, 0, 1], [1, 1, 1], [1, 3, 1], [1, 4, 1], [1, 6, 1], [1, 7, 1], [1, 0, 0], [1, 1, 0], [1, 3, 0],
                      [1, 4, 0], [1, 6, 0], [1, 7, 0]]
        }

    def action(self):

        possible_actions = available_actions(self.state, self.colour)

        #
        # # Action Ver 0: Choose random move
        # # return possible_actions[randrange(0, len(possible_actions))]
        #

        # # Action Ver 1: Greedy method
        # max_point = -9999
        # max_action = None
        # for possible_action in possible_actions:
        #
        #     # In the case using a 2D array, deepcopy must be used since a 2D array contains objects and we want the
        #     # value not by its reference pointer so that we can modify without affecting the original one
        #     candidate_board = deepcopy(self.state)
        #
        #     if possible_action[0] == 'BOOM':
        #         boom(candidate_board, possible_action[1])
        #     elif possible_action[0] == 'MOVE':
        #         move(candidate_board, possible_action[1], possible_action[2], possible_action[3], self.colour)
        #
        #     # calculate
        #     point = evaluate(candidate_board, self.colour)
        #     if point > max_point:
        #         max_point = point
        #         max_action = possible_action
        #
        # return max_action

        # # Action Ver 2: Minimax
        minimax_agent = MinimaxAgent(2, self.colour)
        return minimax_agent.choose_action(self.state)



    def update(self, colour, action):
        if action[0] == 'BOOM':
            boom(self.state, action[1])
        elif action[0] == 'MOVE':
            move(self.state, action[1], action[2], action[3], colour)
