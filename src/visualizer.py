import pygame
from simulation.graph import Graph
from simulation.simulation import Simulation, Drone
from simulation.pathfinder import PathFinder
from parser.map_parser import MapParser
import sys
from rich import print


par = MapParser()
par.read_file(sys.argv[1])

graph = Graph()
graph.init_zones(par)
graph.build_adjacent_list(par)


# graph.init_position_nodes()

def get_node_color(zone, graph):
    if zone.name == graph.start_node:
        return (46, 204, 113)
    if zone.name == graph.end_node:
        return (231, 76, 60)

    if zone.color:
        try:
            return pygame.Color(zone.color)
        except (ValueError, TypeError):
            pass

    if zone.type == 'restricted':
        return (243, 156, 18)
    elif zone.type == 'priority':
        return (241, 196, 15)
    elif zone.type == 'blocked':
        return (80, 80, 80)

    return (52, 152, 219)


def convert_to_pixel(
    x: int, y: int,
    min_x: int, max_x: int,
    min_y: int, max_y: int,
    screen_width: int = 1500,
    screen_height: int = 800,
    margin: int = 60
) -> tuple[int, int]:

    ratio_x = (x - min_x) / (max_x - min_x) if max_x != min_x else 0.5
    ratio_y = (y - min_y) / (max_y - min_y) if max_y != min_y else 0.5

    pixel_x = int(margin + ratio_x * (screen_width - 2 * margin))
    pixel_y = int(margin + ratio_y * (screen_height - 2 * margin))

    return (pixel_x, pixel_y)


position_nodes = {}


def init_position_nodes():

    value_x = [node.x for node in graph.nodes.values()]
    value_y = [node.y for node in graph.nodes.values()]

    for zone in graph.nodes.values():

        ps = convert_to_pixel(
            zone.x, zone.y, min(value_x), max(
                value_x), min(value_y), max(value_y)
        )
        color = get_node_color(zone, graph)
        position_nodes[zone.name] = {
            'ps': ps,
            'color': color
        }


init_position_nodes()

path_f = PathFinder()


path = path_f.dijkstra(graph, 6)

simu = Simulation(Drone, par.nb_drones, path)
history = simu.turns_history

simu.start_simulation(graph)

current_turn = 0
max_turns = len(history) - 1
print(max_turns)
for d in history[max_turns]:
    print(d['zone'])


pygame.init()

screen = pygame.display.set_mode((1900, 800))
pygame.display.set_caption("fly-in")

running = True
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 14, bold=True)


while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_SPACE:
                if current_turn < max_turns:
                    current_turn += 1

            elif event.key == pygame.K_LEFT:
                if current_turn > 0:
                    current_turn -= 1

            elif event.key == pygame.K_r:
                current_turn = 0

    screen.fill((45, 30, 30))

    for cont in par.connections:
        ps1 = position_nodes[cont['from']]['ps']
        ps2 = position_nodes[cont['to']]['ps']

        pygame.draw.line(screen, (255, 0, 0), ps1, ps2)

    for zone in position_nodes:
        pygame.draw.circle(
            screen, position_nodes[zone]['color'], position_nodes[zone]['ps'], 25)
        text_surface = font.render(zone, True, (255, 255, 255))
        screen.blit(text_surface, (position_nodes[zone]['ps'][0] - text_surface.get_width(
        ) // 2, position_nodes[zone]['ps'][1] + 35))

    for drone in history[current_turn]:
        pygame.draw.circle(
            screen, (255, 255, 255), position_nodes[drone['zone']]['ps'], 12
        )

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
