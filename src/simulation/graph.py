class Graph():
    def __init__(self):
        self.nodes = {}
        self.adj = {}
        self.start_node = None
        self.end_node = None
        self.capacities = {}

    def build(self, parser):

        for hub in parser.hubs:

            self.nodes[hub['name']] = hub
            self.adj[hub['name']] = []

            if hub['type'] == 'start_hub':
                self.start_node = hub['name']

            if hub['type'] == 'end_hub':
                self.end_node = hub['name']

        for conn in parser.connections:
            u = conn['from']
            v = conn['to']
            cap = conn['meta_data']['max_capacity']

            self.adj[u].append(v)
            self.adj[v].append(u)
            self.capacities[(u, v)] = cap
            self.capacities[(v, u)] = cap
