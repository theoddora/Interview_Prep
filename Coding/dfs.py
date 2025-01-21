from typing import List

def dfs(graph: List[List[int]]):
    graphNodes = len(graph)
    
    color = ['W'] * graphNodes
    parent = [-1] * graphNodes
    discovery = [-1] * graphNodes
    finish = [-1] * graphNodes
    
    time = 0
    for node in graphNodes:
        if color[node] == "W":
            time = dfsVisit(node, time, color, parent, discovery, finish, graph)


def dfsVisit(node: int, time: int, color: List[str], parent: List[int], discovery: List[int], finish: List[int], graph: List[List[int]]) -> int:
    color[node] = 'G'
    time += 1
    discovery[node] = time

    for v in graph[node]:
        if color[v] == 'W':
            parent[v] = node
            dfsVisit(v, time, color, parent, discovery, finish, graph)
    
    color[node] = 'B'
    time += 1
    finish[node] = time
    return time

