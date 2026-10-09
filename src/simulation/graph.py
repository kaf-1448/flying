from typing import Dict, List, Tuple, Optional
from .zone import Zone
from parser.map_parser import MapParser


class Graph:
    def __init__(self) -> None:
        self.nodes: Dict[str, Zone] = {}
        self.adj: Dict[str, List[str]] = {}
        self.start_node: Optional[str] = None
        self.end_node: Optional[str] = None
        self.capacities: Dict[Tuple[str, str], int] = {}

    def init_zones(self, parser: MapParser) -> None:
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

    def build_adjacent_list(self, parser: MapParser) -> None:
        for conct in parser.connections:
            u: str = conct['from']
            v: str = conct['to']
            cap: int = conct['meta_data']['max_capacity']

            self.adj[u].append(v)
            self.adj[v].append(u)
            self.capacities[(u, v)] = cap
            self.capacities[(v, u)] = cap
