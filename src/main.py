from parser import map_parser
from simulation.graph import Graph
from simulation.pathfinder import PathFinder
from simulation.simulation import Drone, Simulation
import sys
from rich import print
from collections import deque
import heapq


parser = map_parser.MapParser()
parser.read_file(sys.argv[1])

# print(parser.connections)


data_graph = Graph()


data_graph.init_zones(parser)
data_graph.build_adjacent_list(parser)
# print(data_graph.adj)
# print(data_graph.nodes)
# print(data_graph.adj)
# print(data_graph.capacities)


# print(data_graph.adj)

path_f = PathFinder()
# path = path_f.bfs(data_graph)

result = path_f.find_k_paths(
    data_graph, 2)
# print(result)

path = path_f.dijkstra(data_graph, 6)


simu = Simulation(Drone, parser.nb_drones, path)
simu.start_simulation(data_graph)

print(simu.turns_history)
