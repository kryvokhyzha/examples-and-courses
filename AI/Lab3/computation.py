from copy import deepcopy


def is_not_valid(current):
    """
    Check condition for current state.
    Args:
        current:
        couples_number:
    Returns:
    """
    cp = [change_position(s) for s in current.shore]

    if sum(current.shore[:3]) == sum(current.shore[3:]) or \
            (sum(current.shore[:3]) >= 0 and sum(current.shore[3:]) == 0) or \
            (sum(current.shore[:3]) == 0 and sum(current.shore[3:]) >= 0) or \
            (sum(cp[:3]) >= 0 and sum(cp[3:]) == 0) or \
            (sum(cp[:3]) == 0 and sum(cp[3:]) >= 0) or \
            sum(cp[:3]) == sum(cp[3:]):
        print(current.shore, '-', 'X')
        return False
    print(current.shore, '-', 'is not good way')
    return True


def change_position(bit):
    """
    Used to change position of people or the boat.
    Args:
        bit:
    Returns:
    """
    return abs(bit - 1)


def people_near_boat(state):
    """
    Get people on the same side as the boat.
    Args:
        state:
    Returns:
    """
    people = deepcopy(state.shore)
    for i in range(0, len(state.shore)):
        if state.shore[i] == state.boat:
            people[i] = True
        else:
            people[i] = False
    return people


def is_visited(state, visited):
    """
    Determines whether a State has already been visited.
    Args:
        state:
        visited:
    Returns:
    """
    for visited_state in visited:
        if state.shore == visited_state.shore and state.boat == visited_state.boat:
            return True
    return False


def move(cap, state, movement, result, start):
    """
    Computes all possible moves from a current State with a certain boat capacity.
    Args:
        cap:
        state:
        movement:
        result:
        start:
    Returns:
    """
    for i in range(start, len(state.shore)):
        if people_near_boat(state)[i]:
            movement.append(i)
            if cap > 1:
                # without duplicates (permutations)
                move(cap - 1, state, movement, result, i)
            if cap == 1:
                result.append(deepcopy(movement))
            movement.pop()
    return result


def expand(state, layer, visited, couples_number=3, boat_capacity=2):
    """
    Expand and add new states to layer.
    Args:
        state:
        layer:
        visited:
        couples_number:
        boat_capacity:
    Returns:
    """
    result = []

    # get all possible moves for the current State and capacity
    possible_moves = move(boat_capacity, state, [], result, 0)
    for pos_move in possible_moves:
        # create next state
        following_state = deepcopy(state)

        # move one or two person
        if len(set(pos_move)) == 1:
            following_state.shore[pos_move[0]] = change_position(state.shore[pos_move[0]])
        else:
            for person_idx in pos_move:
                following_state.shore[person_idx] = change_position(state.shore[person_idx])

        # move boat
        following_state.boat = change_position(state.boat)

        if is_visited(following_state, visited):
            continue
        elif is_not_valid(following_state):
            visited.append(following_state)
        else:
            following_state.depth += + 1
            following_state.prev_state = state
            layer.append(following_state)
