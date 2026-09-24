from rich import print
import heapq

graph = {
    "A": [("B", 2), ("C", 3)],
    "B": [("D", 4), ("C", 2)],
    "C": [("D", 2)],
    "D": []
}


def k_short_path(graph) -> list:
    pq = []
    heapq.heappush(pq, (0, 'A'))
    distance = {}
    count = {}

    while pq:

        cost, node = heapq.heappop(pq)


k_short_path(graph)
