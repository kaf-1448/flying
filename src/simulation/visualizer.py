import pygame
from typing import Tuple, List, Dict, Any
from .graph import Graph
from parser.map_parser import MapParser


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

    def _draw_zones(self,
                    screen: pygame.Surface,
                    font: pygame.font.Font) -> None:

        for zone_name, data in self.position_nodes.items():
            ps = data['ps']
            pygame.draw.circle(screen, data['color'], ps, 25)
            text_surf = font.render(zone_name, True, (255, 255, 255))
            screen.blit(
                text_surf, (ps[0] - text_surf.get_width() // 2, ps[1] + 35))

    def _draw_drones(self,
                     screen: pygame.Surface,
                     font: pygame.font.Font) -> None:
        for drone in self.history[self.current_turn]:
            zone_str = drone['zone']

            if '-' in zone_str or ' ' in zone_str:
                delimiter = '-' if '-' in zone_str else ' '
                hub1, hub2 = zone_str.split(delimiter)

                p1 = self.position_nodes[hub1]['ps']
                p2 = self.position_nodes[hub2]['ps']

                ps = (
                    (p1[0] + p2[0]) // 2,
                    (p1[1] + p2[1]) // 2
                )

            else:
                ps = self.position_nodes[zone_str]['ps']

            pygame.draw.circle(screen, (255, 255, 255), ps, 12)

            drone_text = font.render(f"D{drone['dron_id']}", True, (255, 0, 0))
            screen.blit(
                drone_text,
                (
                    ps[0] - drone_text.get_width() // 2,
                    ps[1] - drone_text.get_height() // 2
                )
            )

    def _draw_hud(self,
                  screen: pygame.Surface,
                  font: pygame.font.Font) -> None:
        hud_text = font.render(
            f"Turn: {self.current_turn} / {self.max_turns}\
                  |  [SPACE]: Next  |  [LEFT]: Prev  |  [R]: Reset",
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
