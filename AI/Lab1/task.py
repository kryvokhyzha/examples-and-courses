from copy import deepcopy


class State:
    # array with the position of the people in the order w1, w2,... h1, h2, ... (0 for initial shore, 1 for goal shore)
    shore = None
    boat = 0  # position of the boat (0 for initial shore, 1 for goal shore)
    depth = 0  # equals path cost in this example because unit step cost = 1
    path = None  # array of States that lead to the current State

    def __init__(self, s=None, b=0):
        if s is None:
            s = []
        self.shore = s
        self.boat = b
        self.depth = 0
        self.path = []


def jealousy(current):
    """
    Check jealousy for current state.
    :param current:
    :return:
    """
    for i in range(0, noCouples):
        if current.shore[i] != current.shore[noCouples + i]:  # husband is not with his wife
            for j in range(noCouples, noCouples * 2):
                if current.shore[j] == current.shore[i]:  # another man is with the wife
                    return 1
    return 0


def change_position(bit):
    """
    Used to change position of people or the boat.
    :param bit:
    :return:
    """
    return abs(bit - 1)


def people_near_boat(state):
    """
    Get people on the same side as the boat.
    :param state:
    :return:
    """
    people = deepcopy(state.shore)
    for i in range(0, len(state.shore)):
        if state.shore[i] == state.boat:
            people[i] = 1
    return people


def visited(state):
    """
    Determines whether a State has already been visited.
    :param state:
    :return:
    """
    for searched_state in searched:
        if state.shore == searched_state.shore and state.boat == searched_state.boat:
            return True
    return False


def move(cap, state, movement, result, start):
    """
    Computes all possible moves from a current State with a certain boat capacity.
    :param cap:
    :param state:
    :param movement:
    :param result:
    :param start:
    :return:
    """
    for i in range(start, len(state.shore)):
        if people_near_boat(state)[i] == 1:  # if the person is on the same side as the boat
            movement.append(i)  # add the person to the list of possible moves
            if cap > 1:  # if there is more space in the boat
                # iterate; start for-loop with i to prevent duplicates (permutations)
                move(cap - 1, state, movement, result, i)
            if cap == 1:  # if the boat is full
                result.append(deepcopy(movement))  # add move to the result array
            movement.pop()  # when returning to the outer iteration, pop the last item
    return result  # return an array of possible moves


def expand(state):
    result = []
    # get all possible moves for the current State and capacity
    possible_moves = move(boat_capacity, state, [], result, 0)
    for pos_move in possible_moves:  # iterate through all possible state changes
        following = deepcopy(state)
        for person_idx in pos_move:
            following.shore[person_idx] = change_position(state.shore[person_idx])  # move persons
        following.boat = change_position(state.boat)  # move boat
        if visited(following):  # check if state was already visited
            continue
        elif jealousy(following):  # check if there is jealousy
            searched.append(following)
        else:
            following.depth = following.depth + 1  # increase depth
            following.path.append(state)  # add the parent node to the path
            frontier.append(following)  # add the node to the frontier


def dfs():
    no_states = 0
    while True:
        no_states = no_states + 1
        print("Visited states: ", no_states)

        current = frontier.pop()  # examine last item from frontier (LIFO)

        if sum(current.shore) == 6:  # goal check
            return current  # if heuristic function equals 0, the goal is reached

        expand(current)  # expand and add new states to frontier
        searched.append(current)  # add the current node to the closed list3
        print('current', current.shore)


if __name__ == '__main__':
    noCouples = 3
    boat_capacity = 2

    initial = State([], 0)
    frontier = []  # open list (frontier)
    searched = []  # closed list

    # the state will be treated as wife1, wife2, wife3, husband1, husband2, husband3
    initial.shore.extend([0 for _ in range(noCouples * 2)])

    print('Initial shore:', initial.shore)
    frontier.append(initial)  # add initial node to frontier

    goal = dfs()  # search with Depth-First-Search

    print("\nSuccess: ", goal.shore, " reached")
    print("Depth: ", goal.depth)
    path = []
    for item in goal.path:
        path.append(item.shore)
    print("Path: ", path)
