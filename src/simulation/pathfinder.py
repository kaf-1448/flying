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

    def dijkstra(self, graph: Graph, start: str, end: str) -> list[list]:

        pq = []
        distance = {start: 0}
        heapq.heappush(pq, (0, start, [start]))
        # paths = []

        while pq:
            cost, node, path = heapq.heappop(pq)

            if node == end:
                return cost, path

            for neighbor in graph.adj[node]:
                weight = 1

                if graph.nodes[neighbor].type == "priority":
                    weight = 0.9

                if graph.nodes[neighbor].type == "restricted":
                    weight = 2

                if graph.nodes[neighbor].type == "blocked":
                    continue

                new_cost = cost + weight

                if neighbor not in path:

                    if new_cost < distance.get(neighbor, float('inf')):
                        distance[neighbor] = new_cost
                        heapq.heappush(
                            pq, (new_cost, neighbor, path + [neighbor]))

        return None

    def cost(self, graph: Graph, path: list):
        cost = 0
        for i in range(len(path) - 1):
            node = path[i + 1]
            if graph.nodes[node].type == "restricted":
                cost += 2
            elif graph.nodes[node].type == "priority":
                cost += 0.9
            else:
                cost += 1
        return cost

    def yen_algorithm(self, graph: Graph, k: int, path: list, end: str) -> list[list]:

        paths = []
        condidate_paths = []
        seen = set()
        heapq.heappush(condidate_paths, path)
        seen.add(tuple(path[1]))

        while len(paths) < k and condidate_paths:

            i = 0
            c, p = heapq.heappop(condidate_paths)
            paths.append(p)

            while i < len(p):

                spur_node = p[i]
                root_path = p[:i+1]

                for neighbor in graph.adj[spur_node]:

                    if neighbor not in root_path and neighbor not in p[:i+2]:

                        res = self.dijkstra(graph, neighbor, end)

                        if res is not None:
                            n_c, n_p = res
                            total_cost = (self.cost(graph,
                                                    root_path) +
                                          n_c +
                                          graph.capacities[(spur_node, neighbor)])

                            new_path = tuple(root_path + n_p)
                            if new_path not in seen:
                                heapq.heappush(condidate_paths,
                                               (total_cost, root_path + n_p))
                                seen.add(new_path)
                i += 1

        return paths
