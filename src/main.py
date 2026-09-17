from parser import map_parser
from simulation.graph import Graph
import sys

parser = map_parser.MapParser()

parser.read_file(sys.argv[1])


data_graph = Graph()


data_graph.build(parser)

print(data_graph.start_node)
# print(data_graph.nodes)
print(data_graph.adj)
# print(data_graph.start_node)
# print(data_graph.end_node)
print(data_graph.capacities)
