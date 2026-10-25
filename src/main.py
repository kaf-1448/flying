from simulation.visualizer import Visualizer
from simulation.simulation import Drone, Simulation
from simulation.pathfinder import PathFinder
from simulation.graph import Graph
from parser import map_parser
import pygame
import sys


def main() -> None:
    """Parse map, solve routing paths, and run drone simulation."""
    try:

        if len(sys.argv) < 2:
            print("Error File not found must be do that")
            print("Usage: python3 src/main.py <map_file>")
            sys.exit(1)

        parser = map_parser.MapParser()
        parser.read_file(sys.argv[1])

        graph = Graph()
        graph.init_zones(parser)
        graph.build_adjacent_list(parser)

        if graph.start_node is None or graph.end_node is None:
            raise ValueError("Start or End hub not found in graph")

        path_f = PathFinder(parser.nb_drones)

        p = path_f.dijkstra(graph, graph.start_node, graph.end_node)
        if p is None:
            raise ValueError("No path found between start and end hubs")

        k = 2

        paths = path_f.yen_algorithm(graph, k, p, graph.end_node)

        distrib = path_f.brute_force(graph)
        n0, n1 = distrib if distrib is not None else (parser.nb_drones, 0)

        if len(paths) == 1:
            assigned_path = [paths[0]] * parser.nb_drones
        else:
            assigned_path = []
            c0, c1 = 0, 0
            while len(assigned_path) < parser.nb_drones:
                if c0 < n0:
                    assigned_path.append(paths[0])
                    c0 += 1
                if c1 < n1:
                    assigned_path.append(paths[1])
                    c1 += 1

        simu = Simulation(assigned_path, Drone, parser.nb_drones, paths)
        history = simu.turns_history
        simu.start_simulation(graph)

        try:
            vis = Visualizer(graph, parser, history)
            vis.run()
        except pygame.error as e:
            print(f"[Notice] Graphical visualizer skipped: {e}")

    except KeyboardInterrupt:
        sys.exit(0)

    except Exception as e:
        print(F"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
