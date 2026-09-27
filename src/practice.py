from rich import print
from collections import deque
import heapq

start_node = 'A'
end_node = 'F'
K = 3


adj = {
    'A': ['B', 'C'],
    'B': ['C', 'D'],
    'C': ['D', 'E'],
    'D': ['E', 'F'],
    'E': ['F'],
    'F': []
}


weights = {
    ('A', 'B'): 3,
    ('A', 'C'): 2,
    ('B', 'C'): 1,
    ('B', 'D'): 4,
    ('C', 'D'): 2,
    ('C', 'E'): 3,
    ('D', 'E'): 1,
    ('D', 'F'): 1,
    ('E', 'F'): 2,
}


def dijkstar(adj, weights, start, end):
    pq = []
    distance = {}

    heapq.heappush(pq, (0, start, [start]))
    distance[start] = 0

    while pq:

        cost, node, path = heapq.heappop(pq)

        if end == node:
            return cost, path

        for neighbor in adj[node]:

            new_cost = distance[node] + weights[(node, neighbor)]

            if new_cost < distance.get(neighbor, float('inf')):
                distance[neighbor] = new_cost
                heapq.heappush(pq, (new_cost, neighbor, path + [neighbor]))


path = dijkstar(adj, weights, start_node, end_node)
# print(path)


def cost(path, weights):
    cost = 0

    for i in range(len(path) - 1):
        cost += weights[(path[i], path[i+1])]

    return cost


def yen_algorithm(adj, weights, path, end, k):

    final_paths = []
    condidate_paths = []
    seen = set()
    heapq.heappush(condidate_paths, path)
    seen.add(tuple(path[1]))

    while len(final_paths) < k and condidate_paths:
        i = 0
        c, p = heapq.heappop(condidate_paths)
        final_paths.append(p)

        while i < len(p) - 1:

            spur_node = p[i]
            root_path = p[:i+1]
            for neighbor in adj[spur_node]:
                if neighbor not in root_path and neighbor not in p[:i+2]:
                    res = dijkstar(adj, weights, neighbor, end)

                    if res is not None:

                        n_c, n_p = res
                        total_cost = (cost(root_path, weights) +
                                      weights[(spur_node, neighbor)] + n_c)

                        new_full_path = tuple(root_path + n_p)
                        if new_full_path not in seen:

                            heapq.heappush(
                                condidate_paths, (total_cost, root_path + n_p))
                            seen.add(new_full_path)

            i += 1

    return final_paths


k = yen_algorithm(adj, weights, path, end_node, 5)
print(k)
