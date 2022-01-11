import sys

from state import State
from computation import expand
from math import inf
from copy import deepcopy
import random


def stochastic_hill_climbing(layer):
    state_number = 0
    global_best_h = -1 * inf
    visited = []
    while True:
        state_number = state_number + 1
        print("Visited states: ", state_number)

        if not layer:
            return None

        best_state = get_randomly_best(layer, global_best_h)
        if best_state is None:
            return None

        if best_state.h < global_best_h:
            return None
        else:
            global_best_h = best_state.h

        if sum(best_state.shore) == 6:
            return best_state

        print('Depth:', best_state.depth)
        print('current', best_state.shore)

        layer = expand(best_state, layer, visited)
        visited.append(best_state)

        print()


def get_randomly_best(x, global_best):
    while True:
        if len(x) == 0:
            break
        elem = random.choice(x)
        if elem.h < global_best:
            x.remove(elem)
        else:
            return elem
    return None


def get_res(state, buffer):
    if state.prev_state is None:
        return buffer

    return get_res(state.prev_state, buffer + str(state.shore) + ' <- ')


if __name__ == '__main__':
    couples_number = 3
    boat_capacity = 2

    initial = State([], 0)
    init_layer = []  # open list

    initial.shore.extend([0 for _ in range(couples_number * 2)])

    print('Initial shore:', initial.shore)
    init_layer.append(initial)
    best_goal = None
    best_depth = inf
    for i in range(1000):
        print(f'---- Iteration {i+1}')
        goal = stochastic_hill_climbing(init_layer)
        if goal is None:
            continue
        if best_depth > goal.depth:
            best_goal = deepcopy(goal)
            best_depth = best_goal.depth
        print('---------------------------------------------------------')

    if best_goal is None:
        print('\nCan`t find path!')
        sys.exit(-1)

    print('---------------------------------------------------------')
    print("\nSuccess: ", best_goal.shore)
    print("Depth: ", best_goal.depth)
    path = get_res(best_goal, '') + str(initial.shore)
    print("Path: ", path)
