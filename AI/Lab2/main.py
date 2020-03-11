import numpy as np
from sys import maxsize

from node import Node


def recursive_best_first_search(initial_state):
    node = Node(initial_state)
    result, best_h = rbfs(node, maxsize)
    return result.find_solution()


def rbfs(node, h_limit):
    """
    http://chernykh.net/content/view/293/493/
    """
    if node.is_goal:
        return node, 0

    successors = []
    children = node.generate_child()

    if not len(children):
        return None, maxsize

    count = -1
    for child in children:
        count += 1
        successors.append((child.h, count, child))

    while len(successors):
        successors.sort()
        best = successors[0][2]
        if best.h > h_limit:
            return None, best.h
        if len(successors) > 1:
            alternative = successors[1][0]
        else:
            alternative = maxsize
        # print(best)
        result, best.h = rbfs(best, min(h_limit, alternative))
        # print(best.h)
        successors[0] = (best.h, successors[0][1], best)
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
