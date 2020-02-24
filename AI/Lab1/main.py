def dfs(graph, start, visited):
    visited[start] = True
    print('-->', start)
    
    for node in graph[start]:
        if not visited[node]:
            dfs(graph, node, visited)
            print('-->', start)
    return visited


graph_struct = {'0': ['1', '2', '3'],
                '1': ['0', '2'],
                '2': ['0', '1', '4'],
                '3': ['0'],
                '4': ['2']}
visited = {key: False for key in graph_struct.keys()}

dfs(graph_struct, '0', visited)
