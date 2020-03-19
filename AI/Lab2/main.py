import numpy as np
from sys import maxsize

from node import Node


def recursive_best_first_search(initial_state):
    node = Node(initial_state)
    result, best_h = rbfs(node, maxsize, 0)
    return result.find_solution()


def rbfs(node, h_limit, iter):
    if node.is_goal:
        return node, None

    iter += 1

    successors = node.generate_child()

    if not len(successors):
        return None, maxsize

    for s in successors:
        s.h = max(s.h, node.h)

    while len(successors):
        successors.sort(key=lambda x: x.h)
        best = successors[0]
        if best.h > h_limit:
            return None, best.h
        if len(successors) > 1:
            alternative = successors[1].h
        else:
            alternative = maxsize
        # print(best)
        result, best.h = rbfs(best, min(h_limit, alternative), iter)
        # print(best.h)
        if result is not None:
            return result, best.h
    return None, None


if __name__ == '__main__':
    a = [[2, 8, 1], [3, 6, 4], [7, 0, 5]]
    # a = [[0, 1, 3], [4, 2, 5], [6, 7, 8]]

    a = np.array(a)

    RBFS, depth = recursive_best_first_search(a)
    for i in RBFS:
        print(i)
    print('Depth:', depth)
