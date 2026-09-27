from .graph import Graph


class Drone:
    def __init__(self, id,  path, position, is_finished):
        self.id = id
        self.path = path
        self.position = 0
        self.is_finished = is_finished
        self.wait = 0


class Simulation:
    def __init__(
            self,
            drone: Drone,
            nb_drones: int,
            paths: list[str]):
        self.drones = (
            [drone(i+1, paths[i % len(paths)], 0, False) for i in range(nb_drones)])
        self.turns_history = [[
            {
                'dron_id': d.id,
                'zone': d.path[d.position],
                'if_finished': d.is_finished
            }
            for d in self.drones]]
        self.turn = 1

    def start_simulation(self, graph: Graph):

        while any(not d.is_finished for d in self.drones):

            moves = []
            occupied = []
            edge_used = []
            current_state = []

            for d in self.drones:

                if d.position < len(d.path) - 1:
                    next_hub = d.path[d.position + 1]
                    current_hub = d.path[d.position]
                    edge = (current_hub, next_hub)

                if not d.is_finished:

                    if d.wait > 0:
                        d.wait -= 1
                        occupied.append(current_hub)
                        moves.append(
                            f"D{d.id}-{d.path[d.position]}"
                        )
                        current_state.append({
                            'dron_id': d.id,
                            'zone': current_hub,
                            'if_finished': d.is_finished
                        })
                        continue

                    if next_hub == 'goal':
                        d.position += 1
                        moves.append(
                            f"D{d.id}-{d.path[d.position]}"
                        )

                    elif (occupied.count(next_hub) < graph.nodes[next_hub].max_drones
                          and edge_used.count(edge) < graph.capacities.get(edge, 1) and d.wait == 0):

                        if graph.nodes[next_hub].type == 'restricted':
                            d.wait += 1
                            occupied.append(next_hub)
                            edge_used.append(edge)
                            moves.append(
                                f"D{d.id}-{d.path[d.position]}-{d.path[d.position + 1]}"
                            )
                            d.position += 1

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
                print(f"Turn {self.turn}: {" ".join(line for line in moves)}")

            self.turn += 1
