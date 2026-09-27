# import pygame
# from simulation.graph import Graph
# from simulation.simulation import Simulation, Drone
# from simulation.pathfinder import PathFinder
# from parser.map_parser import MapParser
# import sys
# from rich import print


# class Visualizer:
#     def __init__(self):
#         self.position_nodes = {}
#         self.max_turnes = 0

#     def get_node_color(self, zone, graph):
#         if zone.name == graph.start_node:
#             return (46, 204, 113)
#         if zone.name == graph.end_node:
#             return (231, 76, 60)

#         if zone.color:
#             try:
#                 return pygame.Color(zone.color)
#             except (ValueError, TypeError):
#                 pass

#         if zone.type == 'restricted':
#             return (243, 156, 18)
#         elif zone.type == 'priority':
#             return (241, 196, 15)
#         elif zone.type == 'blocked':
#             return (80, 80, 80)

#         return (52, 152, 219)

#     def convert_to_pixel(
#         self,
#         x: int, y: int,
#         min_x: int, max_x: int,
#         min_y: int, max_y: int,
#         screen_width: int = 1500,
#         screen_height: int = 800,
#         margin: int = 60
#     ) -> tuple[int, int]:

#         ratio_x = (x - min_x) / (max_x - min_x) if max_x != min_x else 0.5
#         ratio_y = (y - min_y) / (max_y - min_y) if max_y != min_y else 0.5

#         pixel_x = int(margin + ratio_x * (screen_width - 2 * margin))
#         pixel_y = int(margin + ratio_y * (screen_height - 2 * margin))

#         return (pixel_x, pixel_y)

#     def init_position_nodes(self, graph: Graph):

#         value_x = [node.x for node in graph.nodes.values()]
#         value_y = [node.y for node in graph.nodes.values()]

#         for zone in graph.nodes.values():

#             ps = self.convert_to_pixel(
#                 zone.x, zone.y, min(value_x), max(
#                     value_x), min(value_y), max(value_y)
#             )
#             color = self.get_node_color(zone, graph)
#             self.position_nodes[zone.name] = {
#                 'ps': ps,
#                 'color': color
#             }


# par = MapParser()
# par.read_file(sys.argv[1])

# graph = Graph()
# graph.init_zones(par)
# graph.build_adjacent_list(par)


# # graph.init_position_nodes()

# def get_node_color(zone, graph):
#     if zone.name == graph.start_node:
#         return (46, 204, 113)
#     if zone.name == graph.end_node:
#         return (231, 76, 60)

#     if zone.color:
#         try:
#             return pygame.Color(zone.color)
#         except (ValueError, TypeError):
#             pass

#     if zone.type == 'restricted':
#         return (243, 156, 18)
#     elif zone.type == 'priority':
#         return (241, 196, 15)
#     elif zone.type == 'blocked':
#         return (80, 80, 80)

#     return (52, 152, 219)


# def convert_to_pixel(
#     x: int, y: int,
#     min_x: int, max_x: int,
#     min_y: int, max_y: int,
#     screen_width: int = 1500,
#     screen_height: int = 800,
#     margin: int = 60
# ) -> tuple[int, int]:

#     ratio_x = (x - min_x) / (max_x - min_x) if max_x != min_x else 0.5
#     ratio_y = (y - min_y) / (max_y - min_y) if max_y != min_y else 0.5

#     pixel_x = int(margin + ratio_x * (screen_width - 2 * margin))
#     pixel_y = int(margin + ratio_y * (screen_height - 2 * margin))

#     return (pixel_x, pixel_y)


# position_nodes = {}


# def init_position_nodes():

#     value_x = [node.x for node in graph.nodes.values()]
#     value_y = [node.y for node in graph.nodes.values()]

#     for zone in graph.nodes.values():

#         ps = convert_to_pixel(
#             zone.x, zone.y, min(value_x), max(
#                 value_x), min(value_y), max(value_y)
#         )
#         color = get_node_color(zone, graph)
#         position_nodes[zone.name] = {
#             'ps': ps,
#             'color': color
#         }


# init_position_nodes()

# path_f = PathFinder()

# p = path_f.dijkstra(graph, graph.start_node, graph.end_node)
# path = path_f.yen_algorithm(graph, 2, p, graph.end_node)

# simu = Simulation(Drone, par.nb_drones, path)
# history = simu.turns_history

# simu.start_simulation(graph)

# current_turn = 0
# max_turns = len(history) - 1
# print(max_turns)
# for d in history[max_turns]:
#     print(d)


# pygame.init()

# screen = pygame.display.set_mode((1900, 800))
# pygame.display.set_caption("fly-in")

# running = True
# clock = pygame.time.Clock()
# font = pygame.font.SysFont("Arial", 14, bold=True)


# while running:

#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False

#         if event.type == pygame.KEYDOWN:

#             if event.key == pygame.K_SPACE:
#                 if current_turn < max_turns:
#                     current_turn += 1

#             elif event.key == pygame.K_LEFT:
#                 if current_turn > 0:
#                     current_turn -= 1

#             elif event.key == pygame.K_r:
#                 current_turn = 0

#     screen.fill((45, 30, 30))

#     for cont in par.connections:
#         ps1 = position_nodes[cont['from']]['ps']
#         ps2 = position_nodes[cont['to']]['ps']

#         pygame.draw.line(screen, (255, 0, 0), ps1, ps2)

#     for zone in position_nodes:
#         pygame.draw.circle(
#             screen, position_nodes[zone]['color'], position_nodes[zone]['ps'], 25)
#         text_surface = font.render(zone, True, (255, 255, 255))
#         screen.blit(text_surface, (position_nodes[zone]['ps'][0] - text_surface.get_width(
#         ) // 2, position_nodes[zone]['ps'][1] + 35))

#     for drone in history[current_turn]:
#         pygame.draw.circle(
#             screen, (255, 255, 255), position_nodes[drone['zone']]['ps'], 12
#         )
#         text_surface = font.render(f"D{drone['dron_id']}", True, (255, 0, 0))
#         screen.blit(text_surface, (position_nodes[drone['zone']]['ps'][0] -
#                     text_surface.get_width() // 2, position_nodes[drone['zone']]['ps'][1] - text_surface.get_height() // 2))

#     turn_text = font.render(
#         f"Turn: {current_turn} / {max_turns}  |  [SPACE]: Next  |  [LEFT]: Prev  |  [R]: Reset", True, (255, 255, 255))
#     screen.blit(turn_text, (20, 20))

#     pygame.display.flip()
#     clock.tick(60)

# pygame.quit()


import sys
import pygame
from typing import Tuple, List, Dict, Any
from .graph import Graph
# from .import MapParser


class Visualizer:
    def __init__(
        self,
        graph: Graph,
        parser: MapParser,
        history: List[List[Dict[str, Any]]],
        width: int = 1900,
        height: int = 800,
        margin: int = 60
    ) -> None:
        self.graph = graph
        self.parser = parser
        self.history = history
        self.width = width
        self.height = height
        self.margin = margin
        self.current_turn = 0
        self.max_turns = len(history) - 1
        self.position_nodes: Dict[str, Dict[str, Any]] = {}

        self._init_position_nodes()

    def _get_node_color(self, zone: Any) -> Any:
        if zone.name == self.graph.start_node:
            return (46, 204, 113)
        if zone.name == self.graph.end_node:
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

    def _convert_to_pixel(
        self, x: int, y: int,
        min_x: int, max_x: int,
        min_y: int, max_y: int
    ) -> Tuple[int, int]:
        ratio_x = (x - min_x) / (max_x - min_x) if max_x != min_x else 0.5
        ratio_y = (y - min_y) / (max_y - min_y) if max_y != min_y else 0.5

        pixel_x = int(self.margin + ratio_x * (self.width - 2 * self.margin))
        pixel_y = int(self.margin + ratio_y * (self.height - 2 * self.margin))
        return (pixel_x, pixel_y)

    def _init_position_nodes(self) -> None:
        value_x = [node.x for node in self.graph.nodes.values()]
        value_y = [node.y for node in self.graph.nodes.values()]

        min_x, max_x = min(value_x), max(value_x)
        min_y, max_y = min(value_y), max(value_y)

        for zone in self.graph.nodes.values():
            ps = self._convert_to_pixel(
                zone.x, zone.y, min_x, max_x, min_y, max_y)
            color = self._get_node_color(zone)
            self.position_nodes[zone.name] = {
                'ps': ps,
                'color': color
            }

    def _draw_connections(self, screen: pygame.Surface) -> None:
        for cont in self.parser.connections:
            ps1 = self.position_nodes[cont['from']]['ps']
            ps2 = self.position_nodes[cont['to']]['ps']
            pygame.draw.line(screen, (255, 0, 0), ps1, ps2, 3)

    def _draw_zones(self, screen: pygame.Surface, font: pygame.font.Font) -> None:
        for zone_name, data in self.position_nodes.items():
            ps = data['ps']
            pygame.draw.circle(screen, data['color'], ps, 25)
            text_surf = font.render(zone_name, True, (255, 255, 255))
            screen.blit(
                text_surf, (ps[0] - text_surf.get_width() // 2, ps[1] + 35))

    # def _draw_drones(self, screen: pygame.Surface, font: pygame.font.Font) -> None:
    #     # for drone in self.history[self.current_turn]:
    #     #     ps = self.position_nodes[drone['zone']]['ps']
    #     #     pygame.draw.circle(screen, (255, 255, 255), ps, 12)
    #     #     drone_text = font.render(f"D{drone['dron_id']}", True, (255, 0, 0))
    #     #     screen.blit(
    #     #         drone_text,
    #     #         (ps[0] - drone_text.get_width() // 2,
    #     #          ps[1] - drone_text.get_height() // 2)
    #         )

    def _draw_drones(self, screen: pygame.Surface, font: pygame.font.Font) -> None:
        for drone in self.history[self.current_turn]:
            zone_str = drone['zone']

            # 1. إذا كان الدرون فـ الطريق (Transit بين جوج ديال الـ hubs فـ Turn 1)
            if '-' in zone_str or ' ' in zone_str:
                delimiter = '-' if '-' in zone_str else ' '
                hub1, hub2 = zone_str.split(delimiter)

                p1 = self.position_nodes[hub1]['ps']
                p2 = self.position_nodes[hub2]['ps']

                # حساب منتصف الخط (Midpoint):
                ps = (
                    (p1[0] + p2[0]) // 2,
                    (p1[1] + p2[1]) // 2
                )

            # 2. إذا كان الدرون وصل لـ Hub (فـ Turn 2 أو باقي الـ zones العادية)
            else:
                ps = self.position_nodes[zone_str]['ps']

            # رسم دائرة الدرون (بيضاء)
            pygame.draw.circle(screen, (255, 255, 255), ps, 12)

            # كتابة رقم الدرون (D1, D2...) فـ الوسط بالضبط
            drone_text = font.render(f"D{drone['dron_id']}", True, (255, 0, 0))
            screen.blit(
                drone_text,
                (
                    ps[0] - drone_text.get_width() // 2,
                    ps[1] - drone_text.get_height() // 2
                )
            )

    def _draw_hud(self, screen: pygame.Surface, font: pygame.font.Font) -> None:
        hud_text = font.render(
            f"Turn: {self.current_turn} / {self.max_turns}  |  [SPACE]: Next  |  [LEFT]: Prev  |  [R]: Reset",
            True, (255, 255, 255)
        )
        screen.blit(hud_text, (20, 20))

    def run(self) -> None:
        pygame.init()
        screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Fly-in Drone Visualizer")

        clock = pygame.time.Clock()
        font = pygame.font.SysFont("Arial", 14, bold=True)
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        if self.current_turn < self.max_turns:
                            self.current_turn += 1
                    elif event.key == pygame.K_LEFT:
                        if self.current_turn > 0:
                            self.current_turn -= 1
                    elif event.key == pygame.K_r:
                        self.current_turn = 0

            screen.fill((45, 30, 30))

            self._draw_connections(screen)
            self._draw_zones(screen, font)
            self._draw_drones(screen, font)
            self._draw_hud(screen, font)

            pygame.display.flip()
            clock.tick(60)

        pygame.quit()
