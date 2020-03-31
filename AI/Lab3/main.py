import sys

from state import State
from computation import expand


def dfs():
    state_number = 0
    while True:
        state_number = state_number + 1
        print("Visited states: ", state_number)

        if not layer:
            return None

        current = layer.pop()  # get last item

        if sum(current.shore) == 6:
            return current

        print('Depth:', current.depth)
        print('current', current.shore)

        expand(current, layer, visited)
        visited.append(current)

        print()


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

    goal = dfs()

    if goal is None:
        print('\nCan`t find path!')
        sys.exit(-1)

    print('---------------------------------------------------------')
    print("\nSuccess: ", goal.shore)
    print("Depth: ", goal.depth)
    path = get_res(goal, '') + str(initial.shore)
    print("Path: ", path)
