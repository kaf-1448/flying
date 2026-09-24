from .zone import Zone
# from ..parser.map_parser import MapParser
# from ..parser.map_parser import MapParser


# class Connections:
#     def __init__():
#         from_zone =
#         to_zone =


class Graph():
    def __init__(self):
        self.nodes = {}
        self.adj = {}
        self.start_node = None
        self.end_node = None
        self.capacities = {}
        # self.position_nodes = {}

    def init_zones(self, parser: MapParser):

        for hub in parser.hubs:

            self.adj[hub['name']] = []

            if hub['type'] == 'start_hub':
                self.start_node = hub['name']

            if hub['type'] == 'end_hub':
                self.end_node = hub['name']

            self.nodes[hub['name']] = Zone(
                hub['name'],
                hub['x'],
                hub['y'],
                hub['meta_data']['zone'],
                hub['meta_data']['color'],
                hub['meta_data']['max_drones']
            )

    def build_adjacent_list(self, parser: MapParser):

        for conct in parser.connections:
            u = conct['from']
            v = conct['to']
            cap = conct['meta_data']['max_capacity']

            self.adj[u].append(v)
            self.adj[v].append(u)
            self.capacities[(u, v)] = cap
            self.capacities[(v, u)] = cap
