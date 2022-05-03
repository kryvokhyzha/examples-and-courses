from node import Node


class AstarAlgorithm:
    """
    1. Добавить стартовую клетку в открытый список (при этом её значения G, H и F равны 0).
    2. Повторять следующие шаги:
        - Ищем в открытом списке клетку с наименьшим значением величины F, делаем её текущей.
        - Удаляем текущую клетку из открытого списка и помещаем в закрытый список.
        - Для каждой из соседних, к текущей клетке, клеток:
            - Если клетка непроходима или находится в закрытом списке, игнорируем её.
            - Если клетка не в открытом списке, то добавляем её в открытый список, при этом рассчитываем для неё значения G, H и F, и также устанавливаем ссылку родителя на текущую клетку.
            - Если клетка находится в открытом списке, то сравниваем её значение G со значением G таким, что если бы к ней пришли через текущую клетку. Если сохранённое в проверяемой клетке значение G больше нового, то меняем её значение G на новое, пересчитываем её значение F и изменяем указатель на родителя так, чтобы она указывала на текущую клетку.
        - Останавливаемся, если:
            - В открытый список добавили целевую клетку (в этом случае путь найден).
            - Открытый список пуст (в этом случае к целевой клетке пути не существует).
    3. Сохраняем путь, двигаясь назад от целевой точки, проходя по указателям на родителей до тех пор, пока не дойдём до стартовой клетки.
    
    Sources:
        https://vitalissius.github.io/A-Star-Pathfinding-for-Beginners/
    """

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
            # find node with minimum f-value
            node = min(open_list, key=lambda x: x.f)

            # remove node from open-list and add to close-list
            open_list.remove(node)
            open_hash_set.remove(node.hash_value)
            close_hash_set.add(node.hash_value)

            # generate childs of this state
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
