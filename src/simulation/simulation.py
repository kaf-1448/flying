from typing import Type, List, Dict, Any, Tuple, Optional
from .graph import Graph


class Drone:
    def __init__(
        self,
        id: int,
        path: List[str],
        position: int,
        is_finished: bool
    ) -> None:
        self.id: int = id
        self.path: List[str] = path
        self.position: int = 0
        self.is_finished: bool = is_finished
        self.wait: int = 0


class Simulation:
    def __init__(
            self,
            drone: Type[Drone],
            nb_drones: int,
            paths: List[List[str]]) -> None:
        self.drones: List[Drone] = (
            [drone(i + 1, paths[i % len(paths)], 0, False)
             for i in range(nb_drones)])
        self.turns_history: List[List[Dict[str, Any]]] = [[
            {
                'dron_id': d.id,
                'zone': d.path[d.position],
                'if_finished': d.is_finished
            }
            for d in self.drones]]
        self.turn: int = 1

    def start_simulation(self, graph: Graph) -> None:

        while any(not d.is_finished for d in self.drones):

            moves: List[str] = []
            occupied: List[str] = []
            edge_used: List[Tuple[str, str]] = []
            current_state: List[Dict[str, Any]] = []

            for d in self.drones:

                current_hub: str = d.path[d.position]
                next_hub: Optional[str] = (
                    d.path[d.position + 1]
                    if d.position < len(d.path) - 1
                    else None
                )
                edge: Optional[Tuple[str, str]] = (
                    (current_hub, next_hub)
                    if next_hub else None
                )

                if not d.is_finished:

                    if d.wait > 0:
                        d.wait -= 1
                        occupied.append(current_hub)
                        moves.append(
                            f"D{d.id}-{current_hub}"
                        )
                        current_state.append({
                            'dron_id': d.id,
                            'zone': current_hub,
                            'if_finished': d.is_finished
                        })
                        continue

                    if next_hub == graph.end_node:
                        d.position += 1
                        moves.append(
                            f"D{d.id}-{d.path[d.position]}"
                        )

                    elif (
                            next_hub is not None and edge is not None
                            and occupied.count(
                                next_hub) < graph.nodes[next_hub].max_drones
                            and edge_used.count(
                                edge) < graph.capacities.get(edge, 1)
                            and d.wait == 0):

                        if graph.nodes[next_hub].type == 'restricted':
                            d.wait += 1
                            occupied.append(next_hub)
                            edge_used.append(edge)
                            moves.append(f"D{d.id}-{current_hub}-{next_hub}")

                            current_state.append({
                                'dron_id': d.id,
                                'zone': f"{current_hub}-{next_hub}",
                                'if_finished': False
                            })
                            d.position += 1
                            if d.position == len(d.path) - 1:
                                d.is_finished = True
                            continue

                        else:
                            d.position += 1
                            occupied.append(next_hub)
                            edge_used.append(edge)
                            moves.append(
                                f"D{d.id}-{d.path[d.position]}"
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
                print(f"Turn {self.turn}: {' '.join(line for line in moves)}")

            self.turn += 1
