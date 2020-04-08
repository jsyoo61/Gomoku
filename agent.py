import numpy as np
import pandas as pd

class Iterative_Deepening_Alpha_Beta():
    def __init__(self, env, player_index = None):
        self.env = env
        self.player_index = player_index
        self.opponent_index = self.env.player_info[self.env.player_info.index != player_index].index[0]
        self.action = None

        #### Evaluation of values ( domain dependent ) ####
        # Priority needed in iterative deepening alpha beta search, because of "Unknown" perception
        self.priority_max_value = ['lose', 'tie', 'unknown', 'win'] # Increasing Priority
        self.priority_min_value = ['lose', 'unknown', 'tie', 'win'] # Increasing Priority

    def perceive(self, winner):
        # Win
        if winner == self.player_index:
            return 'win'
        # Lose
        elif winner == self.opponent_index:
            return 'lose'
        # Tie
        else:
            return 'tie'

    # Iterative deepening alpha beta search
    def search(self, state):
        '''
        Iterative Deepening Alpha-Beta search.
        with skip criterion v <= alpha, v >= beta
        and fixed action choice.

        faster, since there's more skipping than "skip criterion v < alpha, v > beta"
        but provides less various actions since all equivalent actions are not searched,
        and an action is fixed as the one which gives its 1st maximum value.
        '''
        self.action = None
        self.max_depth = 2
        self.depth = 1
        self.actions = self.env.actions(state)

        # Shuffle actions to speed up search
        np.random.shuffle(self.actions)

        beta = self.priority_min_value[-1]
        v = self.priority_max_value[0]
        # Loop until v is maximum
        while(v != self.priority_max_value[-1]):
            print('searching with max_depth:%s'%(self.max_depth))
            # When alpha == v in the same node, then alpha & v will always be the same in that node
            # So omit alpha
            v = self.priority_max_value[0]
            # 1. Search for nodes that are not searched fully
            for action in self.actions:
                # 1] Get v_min
                # 1-1] Perform action
                self.env.board = state.copy()
                _, winner, done, _ = self.env.step(action, self.player_index)
                # 1-2] If next state is terminal state
                if done == True:
                    v_min = self.perceive(winner)
                # 1-3] Game goes on (Game didn't end)
                else:
                    v_min = self.min_value(self.env.board, v, beta)
                # 2] v = max(v, v_min) for priority_max,
                if self.priority_max_value.index(v) < self.priority_max_value.index(v_min):
                    v = v_min
                    self.action = action
            self.max_depth += 1
        return self.action

    def max_value(self, state, alpha, beta):
        # Assume current state is not terminal state
        v = self.priority_max_value[0]
        self.depth +=1

        # 1. Search only when (depth <= max_depth)
        if self.depth <= self.max_depth:
            for action in self.env.actions(state):
                # 1] Get v_min
                # 1-1] Perform action
                self.env.board = state.copy()
                _, winner, done, _ = self.env.step(action, self.player_index)
                # 1-2] If next state is terminal state
                if done == True:
                    v_min = self.perceive(winner)
                # 1-3] Game goes on (Game didn't end)
                else:
                    v_min = self.min_value(self.env.board, alpha, beta)

                # 2] v = max(v, v_min) for priority_max
                v = self.priority_max_value[max(self.priority_max_value.index(v), self.priority_max_value.index(v_min))]

                # 3] if v>=beta for priority_min, return v
                if self.priority_min_value.index(v) >= self.priority_min_value.index(beta):
                    self.depth -= 1
                    return v

                # 4] alpha = max(alpha, v) for priority_max
                alpha = self.priority_max_value[max(self.priority_max_value.index(alpha), self.priority_max_value.index(v))]
            # End of search
            self.depth -= 1
            return v

        # 2. Blocked by max_depth
        else:
            self.depth -= 1
            return 'unknown'

    def min_value(self, state, alpha, beta):
        # Assume current state is not terminal state
        v = self.priority_min_value[-1]
        self.depth +=1

        # 1. Search only when (depth <= max_depth)
        if self.depth <= self.max_depth:
            for action in self.env.actions(state):
                # 1] Get v_max
                # 1-1] Perform action
                self.env.board = state.copy()
                _, winner, done, _ = self.env.step(action, self.opponent_index)
                # 1-2] If next state is terminal state
                if done == True:
                    v_max = self.perceive(winner)
                # 1-3] Game goes on (Game didn't end)
                else:
                    v_max = self.max_value(self.env.board, alpha, beta)

                # 2] v = min(v, v_max) for priority_min
                v = self.priority_min_value[min(self.priority_min_value.index(v), self.priority_min_value.index(v_max))]

                # 3] if v<=alpha for priority_max, return v
                if self.priority_max_value.index(v) <= self.priority_max_value.index(alpha):
                    self.depth -= 1
                    return v

                # 4] beta = min(beta, v) for priority_min
                beta = self.priority_min_value[min(self.priority_min_value.index(beta), self.priority_min_value.index(v))]
            # End of search
            self.depth -= 1
            return v

        # 2. Blocked by max_depth
        else:
            self.depth -= 1
            return 'unknown'
