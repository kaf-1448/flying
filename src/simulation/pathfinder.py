from collections import deque
from .graph import Graph
import heapq

from rich import print


class PathFinder:
    def bfs(self, graph: Graph):

        start = graph.start_node

        visited = set()
        queue = deque([(start, [start])])
        visited.add(start)

        while queue:

            node, current_path = queue.popleft()

            if node == graph.end_node:
                return current_path

            for neighbor in graph.adj[node]:

                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, current_path + [neighbor]))

    def find_k_paths(self, graph: Graph, k: int):

        start = graph.start_node
        end = graph.end_node
        queue = deque([(start, [start])])
        paths = []

        while queue:

            node, current_path = queue.popleft()

            if node == end:
                paths.append(current_path)
                if k == len(paths):
                    return paths
                continue

            for neighbor in graph.adj[node]:
                if neighbor not in current_path:
                    queue.append((neighbor,   current_path + [neighbor]))

        return paths

    def dijkstra(self, graph: Graph, k: int) -> list[list]:

        pq = []
        distance = {graph.start_node: 0}
        heapq.heappush(pq, (0, graph.start_node, [graph.start_node]))
        paths = []

        while pq:
            current_cost, node, path = heapq.heappop(pq)

            if node == graph.end_node:
                paths.append(path)
                if k == len(paths):
                    return paths
                continue

            for neighbor in graph.adj[node]:
                weight = 1

                if graph.nodes[neighbor].type == "priority":
                    weight = 1

                if graph.nodes[neighbor].type == "restricted":
                    weight = 2

                if graph.nodes[neighbor].type == "blocked":
                    continue

                new_cost = current_cost + weight

                if neighbor not in path:

                    if new_cost < distance.get(neighbor, float('inf')):
                        # distance[neighbor] = new_cost
                        heapq.heappush(
                            pq, (new_cost, neighbor, path + [neighbor]))

        return paths
