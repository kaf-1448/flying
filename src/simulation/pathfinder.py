# graph = {
#     'start': ['waypoint1'],
#     'waypoint1': ['start', 'waypoint2'],
#     'waypoint2': ['waypoint1', 'goal'],
#     'goal': ['waypoint2']}


# class PathFinder:
#     def bfs(graph):
#         pass

from collections import deque


# class PathFinder():

graph = {
    0: [1, 2],
    1: [2, 3],
    2: [3],
    3: []
}

start_point = 0


visited = set()
queue = deque([start_point])
visited.add(start_point)
order = []

while queue:
    node = queue.popleft()
    order.append(node)

    for neighbor in graph[node]:

        if neighbor not in visited:
            visited.add(neighbor)
            queue.append(neighbor)

print(order)


# 0 1 2 3
