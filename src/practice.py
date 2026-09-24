from rich import print
from collections import deque


graph = {
    'A': ['B', 'C'],
    'B': ['D'],
    'C': ['D'],
    'D': []
}

queue = deque([('A', ['A'])])
visitid = set(['A'])

while queue:

    node, current_path = queue.popleft()

    if node == 'D':
        print(current_path)
        break

    for neighbor in graph[node]:

        if neighbor not in visitid:
            queue.append((neighbor, current_path + [neighbor]))
            visitid.add(neighbor)


# print(path)
