from collections import deque
from typing import List, Tuple, Optional, Set, Dict
from .graph import Graph
import heapq


class PathFinder:
    """Find optimal paths and drone distributions on the graph."""

    def __init__(self, nb_drones: int):
        """Initialize PathFinder with total drone count."""
        self.nb_drones = nb_drones

    def bfs(self, graph: Graph) -> Optional[List[str]]:
        """Find the shortest unweighted path using breadth-first search."""
        start = graph.start_node
        if not start:
            return None

        visited: Set[str] = set()
        queue: deque[Tuple[str, List[str]]] = deque([(start, [start])])
        visited.add(start)

        while queue:

            node, current_path = queue.popleft()

            if node == graph.end_node:
                return current_path

            for neighbor in graph.adj.get(node, []):

                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, current_path + [neighbor]))

        return None

    def find_k_paths(self, graph: Graph, k: int) -> List[List[str]]:
        """Find up to k unweighted paths using breadth-first search."""
        start = graph.start_node
        end = graph.end_node
        if not start or not end:
            return []

        queue: deque[Tuple[str, List[str]]] = deque([(start, [start])])
        paths: List[List[str]] = []

        while queue:

            node, current_path = queue.popleft()

            if node == end:
                paths.append(current_path)
                if k == len(paths):
                    return paths
                continue

            for neighbor in graph.adj.get(node, []):
                if neighbor not in current_path:
                    queue.append((neighbor, current_path + [neighbor]))

        return paths

    def dijkstra(
        self,
        graph: Graph,
        start: str,
        end: str
    ) -> Optional[Tuple[float, List[str]]]:
        """Find lowest-cost path using zone weights and priority gains."""
        pq: List[Tuple[float, int,  str, List[str]]] = []
        distance: Dict[str, float] = {start: 0.0}
        heapq.heappush(pq, (0.0, 0, start, [start]))

        if (graph.nodes[start].type == "blocked"
                or graph.nodes[end].type == "blocked"):
            return None

        while pq:
            cost, neg_prio, node, path = heapq.heappop(pq)

            if node == end:
                return cost, path

            for neighbor in graph.adj.get(node, []):
                weight: float = 1.0
                pre_gain: int = 0

                if graph.nodes[neighbor].type == "priority":
                    weight = 1
                    pre_gain = 1

                elif graph.nodes[neighbor].type == "restricted":
                    weight = 2.0

                elif graph.nodes[neighbor].type == "blocked":
                    weight = float('inf')

                new_cost = cost + weight
                new_prio = neg_prio - pre_gain

                if neighbor not in path:

                    if new_cost < distance.get(neighbor, float('inf')):
                        distance[neighbor] = new_cost
                        heapq.heappush(
                            pq, (new_cost, new_prio, neighbor, path +
                                 [neighbor]))

        return None

    def cost(self, graph: Graph, path: List[str]) -> float:
        """Calculate total traversal cost of a path based on zone types."""
        cost: float = 0.0
        for i in range(len(path) - 1):
            node = path[i + 1]
            if graph.nodes[node].type == "restricted":
                cost += 2.0
            elif graph.nodes[node].type == "priority":
                cost += 1.0
            elif graph.nodes[node].type == "blocked":
                cost += float('inf')
            else:
                cost += 1.0
        return cost

    def yen_algorithm(
        self,
        graph: Graph,
        k: int,
        path: Tuple[float, List[str]],
        end: str
    ) -> List[List[str]]:
        """Find up to k alternative loopless shortest paths."""
        paths: List[List[str]] = []
        condidate_paths: List[Tuple[float, List[str]]] = []
        seen: Set[Tuple[str, ...]] = set()
        heapq.heappush(condidate_paths, path)
        seen.add(tuple(path[1]))

        while len(paths) < k and condidate_paths:

            i = 0
            c, p = heapq.heappop(condidate_paths)
            paths.append(p)

            while i < len(p):

                spur_node = p[i]
                root_path = p[:i + 1]

                for neighbor in graph.adj.get(spur_node, []):

                    if graph.nodes[neighbor].type == "blocked":
                        continue

                    if neighbor not in root_path and neighbor not in p[:i + 2]:

                        res = self.dijkstra(graph, neighbor, end)

                        if res is not None:
                            n_c, n_p = res
                            cap = graph.capacities.get(
                                (spur_node, neighbor), 1
                            )
                            total_cost = (
                                self.cost(graph, root_path)
                                + n_c
                                + cap
                            )

                            new_path = tuple(root_path + n_p)
                            if len(new_path) == len(set(new_path)):
                                if new_path not in seen:
                                    heapq.heappush(
                                        condidate_paths,
                                        (total_cost, root_path + n_p)
                                    )
                                    seen.add(new_path)
                i += 1

        return paths

    def brute_force(self, graph: Graph) -> Optional[Tuple[int, int]]:
        """Find optimal drone distribution over paths to minimize makespan."""
        if not graph.start_node or not graph.end_node:
            return None

        best_max = float('inf')
        best_distribution: Optional[Tuple[int, int]] = None

        short_path = self.dijkstra(graph,
                                   graph.start_node, graph.end_node)
        if short_path is None:
            return None

        paths = self.yen_algorithm(graph, 2, short_path, graph.end_node)
        if len(paths) <= 1:
            return (self.nb_drones, 0)

        cost0 = int(self.cost(graph, paths[0]))
        cost1 = int(self.cost(graph, paths[1]))

        for n0 in range(self.nb_drones + 1):

            n1 = self.nb_drones - n0

            t0 = cost0 + n0 - 1 if n0 else 0
            t1 = cost1 + n1 - 1 if n1 else 0

            maximum = max(t0, t1)

            if maximum <= best_max:
                best_max = maximum
                best_distribution = (n0, n1)

        return best_distribution
