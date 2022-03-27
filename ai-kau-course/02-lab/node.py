import numpy as np


class Node:
    def __init__(self, state, parent=None, action=None, goal=None, h_strategy=None):
        self.state = state
        self.parent = parent
        self.action = action
        self.goal = goal
        self.h_strategy = h_strategy
        self.hash_value = hash(self.state.tostring())

        if parent is not None:
            self.depth = parent.depth + 1
            self.h = self.__heuristic(mode=self.h_strategy)
            self.f = self.h + self.depth
        else:
            self.depth = 0
            self.h = 0
            self.f = 0

        if self.goal is None:
            self.goal = np.asarray([[1, 2, 3], [4, 0, 5], [6, 7, 8]])
        else:
            assert isinstance(self.goal, np.ndarray)
        self.is_goal = self.__is_goal()

    def __find_zero_pos(self):
        i, j = np.where(self.state == 0)
        return i[0], j[0]

    @staticmethod
    def __find_actions(i, j):
        legal_action = ['Up', 'Down', 'Left', 'Right']
        if i == 0:  # disable "up" action
            legal_action.remove('Up')
        elif i == 2:  # disable "down" action
            legal_action.remove('Down')
        if j == 0:
            legal_action.remove('Left')  # disable "left" action
        elif j == 2:
            legal_action.remove('Right')  # disable "right" action
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
            new_state = self.do_action(new_state, action)
            if self.parent is not None:
                if (new_state == self.parent.state).all():
                    continue
            children.append(
                Node(state=new_state, parent=self, action=action, goal=self.goal, h_strategy=self.h_strategy)
            )
        return children

    def __heuristic(self, mode):
        """
        Compute the heuristic value for current state.
        """
        assert mode in {'None', 'misplaced', 'manhattan'}

        if mode == 'manhattan':
            return np.sum(np.abs(self.state - self.goal))
        elif mode == 'misplaced':
            return np.sum(self.state != self.goal)
        elif mode == 'None':
            return 0

    def __is_goal(self):
        return (self.state == self.goal).all()

    def find_solution(self):
        solution = [(self.state, self.action)]
        one_of_parent = self
        acc_f = self.f
        while one_of_parent.parent is not None:
            acc_f += one_of_parent.f
            one_of_parent = one_of_parent.parent
            solution.append((one_of_parent.state, one_of_parent.action))
        solution[-1] = (solution[-1][0], 'Start')
        solution.reverse()
        return solution, len(solution), self.f, acc_f

    def __repr__(self):
        return 'Node: h = {}; depth = {}; state = {}'.format(self.f, self.depth, self.state)

    def __eq__(self, other):
        """Overrides the default implementation"""
        if isinstance(other, Node):
            return self.hash_value == other.hash_value
        return False

    def __ne__(self, other):
        """Overrides the default implementation"""
        return not self.__eq__(other)
