import sys
from .exceptions import DuplicateName
from .exceptions import ConnectNameNotFound
from .exceptions import StartOrEndNotFound, PositiveNumber


ALLOWED_ZONES = {"normal", "blocked", "restricted", "priority"}


class MapParser:
    def __init__(self):
        self.nb_drones = 0
        self.hubs = []
        self.connections = []

    def read_file(self, path: str):
        with open(path, "r") as file:
            for num, line in enumerate(file, start=1):

                cleanedline = line.strip('\n').strip(' ')

                if not cleanedline or cleanedline.startswith('#'):
                    continue

                key, value = cleanedline.split(':')
                key = key.strip(' ')
                value: str = value.strip(' ')

                if key == "nb_drones":
                    self.nb_drones = int(value)

                    if self.nb_drones <= 0:
                        raise PositiveNumber(
                            f"error in line {num} nb_drones must be greath"
                            " than from 0.")

                elif key in ("start_hub", "hub", "end_hub"):

                    if '[' in value and ']' in value:

                        main_part = value.split('[')[0]
                        meta_data_part = value.strip(']').split('[')[1]

                        name, x, y = main_part.strip(' ').split(' ')

                        # # color = meta_data_part.split('=')
                        color = None
                        zone = 'normal'
                        max_drones = 1

                        for item in meta_data_part.split(' '):
                            if 'color' in item:
                                color = item.split('=')[1]

                            if "max_drones" in item:
                                max_drones = item.split('=')[1]

                            if 'zone' in item:
                                is_zone_there = item.split('=')[1]
                                if is_zone_there in ALLOWED_ZONES:
                                    zone = is_zone_there

                            # print(meta_data_part)
                        self.hubs.append(
                            {
                                'type': key,
                                'name': name,
                                'x': x,
                                'y': y,
                                'meta_data': {
                                    'zone': zone,
                                    'color': color,
                                    'max_drones': int(max_drones)
                                }
                            }
                        )
                    else:
                        main_part = value.split('[')[0]
                        name, x, y = main_part.strip(' ').split(' ')

                        color = None
                        zone = 'normal'
                        max_drones = 1

                        self.hubs.append(
                            {
                                'type': key,
                                'name': name,
                                'x': x,
                                'y': y,
                                'meta_data': {
                                    'zone': zone,
                                    'color': color,
                                    'max_drones': int(max_drones)
                                }
                            }
                        )

                elif key == "connection":
                    if '[' in value and ']' in value:

                        main_part = value.split('[')[0]
                        meta_data_part = value.strip(']').split('[')[1]

                        first, second = main_part.strip(' ').split('-')
                        max_capacity = 1

                        if ('max_link_capacity' in meta_data_part
                                or 'max_capacity' in meta_data_part):
                            max_capacity = meta_data_part.split('=')[1]

                        self.connections.append(
                            {
                                'type': key,
                                'from': first,
                                'to': second,
                                'meta_data': {
                                    'max_capacity': int(max_capacity)
                                }
                            }
                        )

                    else:

                        for item in value.split(' '):
                            first = item.split('-')[0]
                            second = item.split('-')[1]

                        self.connections.append(
                            {
                                'type': key,
                                'from': first,
                                'to': second,
                                'meta_data': {
                                    'max_capacity': 1
                                }
                            }
                        )

    def check_errors(self):
        end_hub_is_there = 0
        start_hub_is_there = 0
        is_duplicat = 0
        name_of_hubs = []

        for hubs in self.hubs:

            if hubs['type'] == "end_hub":
                end_hub_is_there += 1

            if hubs['type'] == "start_hub":
                start_hub_is_there += 1

            if hubs['name'] in name_of_hubs:
                is_duplicat = 1

            name_of_hubs.append(hubs['name'])

        if end_hub_is_there != 1:
            raise StartOrEndNotFound("end_hub not found")

        if start_hub_is_there != 1:
            raise StartOrEndNotFound("start_hub not found")

        if is_duplicat:
            raise DuplicateName()

        for x in self.connections:
            if x['from'] not in name_of_hubs:
                raise ConnectNameNotFound()

            if x['to'] not in name_of_hubs:
                raise ConnectNameNotFound()
