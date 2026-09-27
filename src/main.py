from parser import map_parser
from simulation.graph import Graph
from simulation.pathfinder import PathFinder
from simulation.simulation import Drone, Simulation
from simulation.visualizer import Visualizer
import sys
from rich import print
from collections import deque
import heapq


try:
    parser = map_parser.MapParser()
    parser.read_file(sys.argv[1])
    # parser.check_errors()

    print(parser.nb_drones)

    print(parser.connections)

    graph = Graph()

    graph.init_zones(parser)
    graph.build_adjacent_list(parser)

    path_f = PathFinder()

    p = path_f.dijkstra(graph, graph.start_node, graph.end_node)
    path = path_f.yen_algorithm(graph, 2, p, graph.end_node)

    simu = Simulation(Drone, parser.nb_drones, path)
    history = simu.turns_history

    simu.start_simulation(graph)
    vis = Visualizer(graph, parser, history)
    vis.run()

    print(simu.turns_history)
except Exception as e:
    print(e)
