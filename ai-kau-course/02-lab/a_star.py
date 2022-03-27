from node import Node


class AstarAlgorithm:

    def __init__(self, initial_state, parent=None, action=None, goal=None, h_strategy='misplaced'):
        self.initial_state = initial_state
        self.parent = parent
        self.action = action
        self.goal = goal
        self.h_strategy = h_strategy

    def fit(self):
        final_node = AstarAlgorithm.__algorithm_iter(
            init_node=Node(self.initial_state, self.parent, self.action, self.goal, self.h_strategy),
        )
        return final_node.find_solution()

    @staticmethod
    def __algorithm_iter(init_node):
        open_list = [init_node]
        open_hash_set = {init_node.hash_value}
        close_hash_set = set()

        while len(open_list) > 0:
            # find node with minimum Hypothesis-value
            node = min(open_list, key=lambda x: x.h)

            # remove node from open-list and add to close-list
            open_list.remove(node)
            open_hash_set.remove(node.hash_value)
            close_hash_set.add(node.hash_value)

            neighbors = node.generate_child()
            for n in neighbors:
                if n.hash_value in close_hash_set:
                    continue

                if n.hash_value not in open_hash_set:
                    open_list.append(n)
                    open_hash_set.add(n.hash_value)
                else:
                    open_node = open_list[open_list.index(n)]
                    if open_node.depth > n.depth:
                        open_list.remove(open_node)
                        open_list.append(n)
            for node in open_list:
                if node.is_goal:
                    return node
        return None
