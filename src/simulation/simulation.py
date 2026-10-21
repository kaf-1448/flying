from typing import Type, List, Dict, Any, Tuple, Optional
from .graph import Graph


class Drone:
    def __init__(
        self,
        id: int,
        path: List[str],
        position: int,
        is_finished: bool,
        edge: Optional[Tuple[str, str]] = None
    ) -> None:
        self.id: int = id
        self.path: List[str] = path
        self.position: int = 0
        self.is_finished: bool = is_finished
        self.wait: int = 0
        self.in_flight_edge: Optional[Tuple[str, str]] = edge


class Simulation:
    def __init__(
            self,
            assigned_path: list[list[str]],
            drone: Type[Drone],
            nb_drones: int,
            paths: List[List[str]]) -> None:
        self.assigned_path: List[List[str]] = assigned_path
        self.drones: List[Drone] = (
            [drone(i + 1, assigned_path[i], 0, False, None)
             for i in range(nb_drones)])
        self.turns_history: List[List[Dict[str, Any]]] = [[
            {
                'dron_id': d.id,
                'zone': d.path[d.position],
                'if_finished': d.is_finished
            }
            for d in self.drones]]
        self.turn: int = 1

    @staticmethod
    def make_edge(u: str, v: str) -> Tuple[str, str]:
        return (u, v) if u < v else (v, u)

    def start_simulation(self, graph: Graph) -> None:

        while any(not d.is_finished for d in self.drones):

            moves: List[str] = []

            occupied: List[str] = [
                d.path[d.position] if d.wait == 0 else d.path[d.position + 1]
                for d in self.drones if (not d.is_finished
                                         and d.path[
                                             d.position] !=
                                         graph.start_node)

            ]

            edge_used: List[Tuple[str, str]] = []
            current_state: List[Dict[str, Any]] = []

            active_drones = [d for d in self.drones if not d.is_finished]
            active_drones.sort(key=lambda d: d.position, reverse=True)

            for d in active_drones:

                current_hub: str = d.path[d.position]
                next_hub: Optional[str] = (
                    d.path[d.position + 1]
                    if d.position < len(d.path) - 1
                    else None
                )

                if next_hub is None:
                    continue

                edge: Tuple[str, str] = self.make_edge(
                    current_hub, next_hub)
                edge_count: int = edge_used.count(edge)
                edge_cap: int = graph.capacities.get(edge, 1)

                if next_hub is not None:
                    edge_count = (
                        edge_used.count((current_hub, next_hub))
                        + edge_used.count((next_hub, current_hub))
                    )

                if not d.is_finished:

                    if d.wait > 0:
                        d.wait -= 1

                        d.position += 1
                        moves.append(
                            f"D{d.id}-{next_hub}"
                        )
                        current_state.append({
                            'dron_id': d.id,
                            'zone': next_hub,
                            'if_finished': d.is_finished
                        })
                        if d.position == len(d.path) - 1:
                            d.is_finished = True
                        continue

                    if next_hub == graph.end_node and edge is not None:
                        if edge_count < edge_cap:
                            d.position += 1
                            if current_hub in occupied:
                                occupied.remove(current_hub)
                            edge_used.append(edge)
                            moves.append(
                                f"D{d.id}-{d.path[d.position]}"
                            )

                    elif (
                            next_hub is not None and edge is not None and
                            graph.nodes[next_hub].type == "restricted"
                            and edge_count < edge_cap
                            and d.wait == 0
                    ):
                        in_flight_to_target = 0
                        for other in self.drones:
                            if (other.wait > 0 and
                                    other.path[other.position + 1]
                                    == next_hub and
                                    other.position + 1 < len(other.path)):
                                in_flight_to_target += 1

                        if (in_flight_to_target <
                                graph.nodes[next_hub].max_drones):
                            d.wait += 1
                            if current_hub in occupied:
                                occupied.remove(current_hub)
                            d.in_flight_edge = edge
                            edge_used.append(edge)
                            occupied.append(next_hub)
                            moves.append(f"D{d.id}-{current_hub}-{next_hub}")

                            current_state.append({
                                'dron_id': d.id,
                                'zone': f"{current_hub}-{next_hub}",
                                'if_finished': False
                            })
                            continue

                    elif (
                            next_hub is not None and edge is not None
                            and occupied.count(
                                next_hub) < graph.nodes[next_hub].max_drones
                            and edge_count < edge_cap
                            and d.wait == 0):

                        d.position += 1
                        occupied.append(next_hub)
                        d.in_flight_edge = edge
                        if current_hub in occupied:
                            occupied.remove(current_hub)
                        edge_used.append(edge)
                        moves.append(
                            f"D{d.id}-{next_hub}"
                        )

                    if d.position == len(d.path) - 1:
                        d.is_finished = True

                    current_state.append({
                        'dron_id': d.id,
                        'zone': d.path[d.position],
                        'if_finished': d.is_finished
                    })

                else:

                    current_state.append({
                        'dron_id': d.id,
                        'zone': d.path[d.position],
                        'if_finished': d.is_finished
                    })
            self.turns_history.append(current_state)

            if moves:
                print(f"{' '.join(line for line in moves)}")

            self.turn += 1
