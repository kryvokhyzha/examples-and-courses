import itertools


def is_jealousy(current, couples_number=3):
    """
    Check jealousy for current state.

    Args:
        current:
        couples_number:

    Returns:

    """
    for i in range(0, couples_number):
        # husband is not with his wife
        if current[i] != current[couples_number + i]:
            for j in range(couples_number, couples_number * 2):
                # another man is with the wife
                if current[j] == current[i]:
                    return True
    return False


full_list = []
for i in range(0, 7):
    my_list = [1]*i + [0]*(6 - i)
    my_list = list(itertools.permutations(my_list))
    full_list.extend(my_list)

full_list = list(set(full_list))
full_list = [list(i) for i in full_list]
result = []
for i in full_list:
    mask = is_jealousy(i)
    if not mask:
        result.append(i)

print(result)
print(len(result))
