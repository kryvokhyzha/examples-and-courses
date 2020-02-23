from itertools import product, combinations_with_replacement, permutations


def dfs(graph, start, visited):
    visited[start] = True
    print(start)
    for node in graph[start]:
        if not visited[node]:
            dfs(graph, node, visited)
            print('*', node, start)
    return visited


prod = product(['0', '0', '0'], ['1', '1', '1'])
com = combinations_with_replacement('01', 6)
per = permutations('01', 6)
print(list(prod))
print(list(com))
print(list(per))

# graph = {'0': ['1', '2', '3'],
#          '1': ['0', '2'],
#          '2': ['0', '1', '4'],
#          '3': ['0'],
#          '4': ['2']}
# visited = {key: False for key in graph.keys()}

# dfs(graph, '0', visited)
