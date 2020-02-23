from copy import deepcopy
import time


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
    for i in range(0, noCouples):
        if current.shore[i] != current.shore[noCouples + i]:  # husband is not with his wife
            for j in range(noCouples, noCouples * 2):
                if current.shore[j] == current.shore[i]:  # another man is with the wife
                    return 1
    return 0


def alterbit(bit):  # used to change position of people or the boat
    return abs(bit - 1)


def isGood(state):  # people on the same side as the boat are "good"
    good_people = deepcopy(state.shore)
    for i in range(0, len(state.shore)):
        if state.shore[i] == state.boat:
            good_people[i] = 1
    return good_people


def h(state):  # the heuristic function equals the number of people who are not on the goal shore
    """
    Check if it is goal (sum of shore == 6 and boat == 1)

    :param state:
    :return:
    """
    result = len(state.shore)
    for i in state.shore:
        result = result - i
    return result


def visited(state, searched):  # determines whether a State has already been visited
    for k in range(0, len(searched)):
        if state.shore == searched[k].shore and state.boat == searched[k].boat:
            return True
    return False


def move(cap, state, movement, result, start):
    # computes all possible moves from a current State with a certain boat capacity
    for i in range(start, len(state.shore)):
        if isGood(state)[i] == 1:  # if the person is on the same side as the boat
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
    print('pos_m', possible_moves)
    for i in possible_moves:  # iterate through all possible state changes
        following = deepcopy(state)
        for j in i:
            following.shore[j] = alterbit(state.shore[j])  # move persons
        following.boat = alterbit(state.boat)  # move boat
        if visited(following, searched):  # check if state was already visited
            pass
        elif jealousy(following):  # check if there is jealousy
            searched.append(following)
        else:
            following.depth = following.depth + 1  # increase depth
            following.path.append(state)  # add the parent node to the path
            frontier.append(following)  # add the node to the frontier


def DFS():
    global noStates
    while True:
        noStates = noStates + 1
        print("Visited states: ", noStates)

        current = frontier.pop()  # examine last item from frontier (LIFO)

        if h(current) == 0:  # goal check
            return current  # if heuristic function equals 0, the goal is reached

        expand(current)  # expand and add new states to frontier
        searched.append(current)  # add the current node to the closed list3
        print('current', current.shore)


if __name__ == '__main__':
    noCouples = int(input("Enter the number of couples: "))
    boat_capacity = int(input("How many persons can the boat hold: "))

    time.perf_counter()

    couple = [0, 0]
    initial = State([], 0)
    goal = State([], 0)
    path = []
    frontier = []  # open list (frontier)
    searched = []  # closed list
    noStates = 0

    for i in range(0, noCouples):  # add couples on left side of the river
        initial.shore.extend(couple)  # the state will be treated as wife1, wife2, wife3, ... husband1, husband2, ...

    print('initial', initial.shore)
    frontier.append(initial)  # add initial node to frontier

    goal = DFS()  # search with Depth-First-Search

    print("\nSuccess: ", goal.shore, " reached")
    print("Depth: ", goal.depth)
    for i in goal.path:
        path.append(i.shore)
    print("Path: ", path)
    print("elapsed time: %.2fs" % time.perf_counter())