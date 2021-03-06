'''
Paritially of this agent code is from https://github.com/haryoa/evo-pawness written by Haryo AW
We copied and modified only for the sake of Minimax Agent for a better use
'''

from NeCho.helper import available_actions, evaluate, is_over, new_state


class MinimaxABAgent:

    def __init__(self, max_depth, colour):

        self.max_depth = max_depth
        self.colour = colour

    def choose_action(self, state):

        eval_score, selected_action = self._minimax(0, state, self.colour, float('-inf'), float('inf'))

        return selected_action

    def _minimax(self, current_depth, state, colour, alpha, beta):

        if current_depth == self.max_depth or is_over(state):
            return evaluate(state, self.colour), ""

        possible_actions = available_actions(state, colour)

        best_value = float('-inf') if colour == self.colour else float('inf')
        action = possible_actions[-1]

        for possible_action in possible_actions:

            candidate_state = new_state(state, colour, possible_action)

            eval_child, action_child = self._minimax(current_depth + 1, candidate_state,
                                                     -colour, alpha, beta)

            if colour == self.colour and best_value < eval_child:
                best_value = max(best_value, eval_child)
                action = possible_action
                alpha = max(alpha, best_value)
                if beta <= alpha:
                    break

            elif (colour != self.colour) and best_value > eval_child:
                best_value = min(best_value, eval_child)
                action = possible_action
                beta = min(beta, best_value)
                if beta <= alpha:
                    break

        return best_value, action
