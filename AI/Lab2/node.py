import numpy as np


class Node:
    def __init__(self, state, parent=None, action=None, goal=None, h_mode='misplaced'):
        self.state = state
        self.parent = parent
        self.action = action
        self.goal = goal
        if parent is not None:
            self.depth = parent.depth + 1
        else:
            self.depth = 0

        if self.goal is None:
            self.goal = np.array([[1, 2, 3], [4, 0, 5], [6, 7, 8]])
        else:
            assert isinstance(self.goal, np.array)

        self.h = self.__heuristic(mode=h_mode)
        self.is_goal = self.__is_goal()

    def __find_zero_pos(self):
        i, j = np.where(self.state == 0)
        return i[0], j[0]

    @staticmethod
    def __find_actions(i, j):
        legal_action = ['Up', 'Down', 'Left', 'Right']
        if i == 0:  # up is disable
            legal_action.remove('Up')
        elif i == 2:  # down is disable
            legal_action.remove('Down')
        if j == 0:
            legal_action.remove('Left')
        elif j == 2:
            legal_action.remove('Right')
        return legal_action

    @staticmethod
    def do_action(new_state, action):
        shape = new_state.shape
        new_state = np.reshape(new_state, (1, 9))[0]
        x = np.where(new_state == 0)[0]
        if action == 'Up':
            new_state[x], new_state[x - 3] = new_state[x - 3], new_state[x]
        elif action == 'Down':
            new_state[x], new_state[x + 3] = new_state[x + 3], new_state[x]
        elif action == 'Left':
            new_state[x], new_state[x - 1] = new_state[x - 1], new_state[x]
        elif action == 'Right':
            new_state[x], new_state[x+1] = new_state[x+1], new_state[x]
        new_state = np.reshape(new_state, shape)
        return new_state

    def generate_child(self):
        children = []
        i, j = self.__find_zero_pos()
        legal_actions = self.__find_actions(i, j)

        for action in legal_actions:
            new_state = self.state.copy()
            self.do_action(new_state, action)
            children.append(Node(new_state, self, action))
        return children

    def __heuristic(self, mode):
        """
        Compute the heuristic value for current state.
        """
        assert mode in {'manhattan', 'misplaced'}

        if mode == 'manhattan':
            return np.sum(np.abs(self.state - self.goal)) + self.depth
        elif mode == 'misplaced':
            return np.sum(self.state != self.goal) + self.depth

    def __is_goal(self):
        return (self.state == self.goal).all()

    def find_solution(self):
        solution = [(self.state, self.action)]
        path = self
        while path.parent is not None:
            path = path.parent
            solution.append((path.state, path.action))
        solution[-1] = (solution[-1][0], 'Start')
        solution.reverse()
        return solution, self.depth

    def __repr__(self):
        return 'Node: depth = {}; state = {}'.format(self.depth, self.state)
