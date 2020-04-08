from state import State
from computation import expand
from math import inf
from copy import deepcopy


def hill_climbing():
    state_number = 0
    global_best_score = -1 * inf
    while True:
        state_number = state_number + 1
        print("Visited states: ", state_number)

        if not layer:
            return None

        best_idx = get_idx_of_best_state()
        if best_idx is None:
            return None

        best_state = layer.pop(best_idx)

        if best_state.h < global_best_score:
            return None
        else:
            global_best_score = best_state.h

        if sum(best_state.shore) == 6:
            return best_state

        print('Depth:', best_state.depth)
        print('current', best_state.shore)

        expand(best_state, layer, visited)
        visited.append(best_state)

        print()


def get_idx_of_best_state():
    best_h = -1 * inf
    best_idx = None
    for idx, state in enumerate(layer):
        if state.h >= best_h:
            best_h = state.h
            best_idx = idx

    if best_idx is not None:
        return best_idx
    else:
        return None


def get_res(state, buffer):
    if state.prev_state is None:
        return buffer

    return get_res(state.prev_state, buffer + str(state.shore) + ' <- ')


if __name__ == '__main__':
    couples_number = 3
    boat_capacity = 2

    initial = State([], 0)
    layer = []  # open list
    visited = []  # closed list

    initial.shore.extend([0 for _ in range(couples_number * 2)])

    print('Initial shore:', initial.shore)
    layer.append(initial)

    goal = hill_climbing()

    if goal is None:
        print('\nCan`t find path!')
        sys.exit(-1)

    print('---------------------------------------------------------')
    print("\nSuccess: ", goal.shore)
    print("Depth: ", goal.depth)
    path = get_res(goal, '') + str(initial.shore)
    print("Path: ", path)
