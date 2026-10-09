import sys
from parser import map_parser
from simulation.graph import Graph
from simulation.pathfinder import PathFinder
from simulation.simulation import Drone, Simulation
from simulation.visualizer import Visualizer


try:
    if len(sys.argv) < 2:
        print("Usage: python3 src/main.py <map_file>")
        sys.exit(1)

    parser = map_parser.MapParser()
    parser.read_file(sys.argv[1])

    graph = Graph()
    graph.init_zones(parser)
    graph.build_adjacent_list(parser)

    if graph.start_node is None or graph.end_node is None:
        raise ValueError("Start or End hub not found in graph")

    path_f = PathFinder()

    p = path_f.dijkstra(graph, graph.start_node, graph.end_node)
    if p is None:
        raise ValueError("No path found between start and end hubs")

    paths = path_f.yen_algorithm(graph, 2, p, graph.end_node)

    simu = Simulation(Drone, parser.nb_drones, paths)
    history = simu.turns_history

    simu.start_simulation(graph)
    vis = Visualizer(graph, parser, history)
    vis.run()

except Exception as e:
    print(e)
