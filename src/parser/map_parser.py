from .exceptions import DuplicateName, NameMapsParsingError
from .exceptions import ConnectNameNotFound, StartByNmDrone
from .exceptions import StartOrEndNotFound, PositiveNumber
from .exceptions import DuplicateConnectionError


ALLOWED_ZONES = {"normal", "blocked", "restricted", "priority"}


class MapParser:
    def __init__(self):
        self.nb_drones = 0
        self.hubs = []
        self.connections = []

    def read_file(self, path: str):
        with open(path, "r") as file:
            end_hub_is_there = 0
            start_hub_is_there = 0
            number_drones = 0
            name_hubs = []
            seen_connection = set()

            for num, line in enumerate(file, start=1):

                cleanedline = line.strip('\n').strip(' ')

                if not cleanedline or cleanedline.startswith('#'):
                    continue

                key, value = cleanedline.split(':')
                key = key.strip(' ')
                value: str = value.strip(' ')

                if key == "nb_drones":

                    try:
                        self.nb_drones = int(value)

                    except ValueError:
                        raise ValueError(
                            f"Error in line {num} nb_drones must"
                            " be number")

                    if self.nb_drones <= 0:
                        raise PositiveNumber(
                            f"Error in line {num} nb_drones must be greath"
                            " than from 0.")
                    number_drones += 1

                elif key in ("start_hub", "hub", "end_hub"):

                    if '[' in value and ']' in value:

                        main_part = value.split('[')[0]
                        meta_data_part = value.strip(']').split('[')[1]

                        name, x, y = main_part.strip(' ').split(' ')

                        if '-' in name:
                            raise NameMapsParsingError(
                                f"Error in line {num} must not '-' in zone"
                                " word")

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

                        if name not in name_hubs:
                            name_hubs.append(name)
                        else:
                            raise DuplicateName(
                                f"Error in line {num} {name} must not"
                                " duplicate")

                        self.hubs.append(
                            {
                                'type': key,
                                'name': name,
                                'x': int(x),
                                'y': int(y),
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

                        if '-' in name:
                            raise NameMapsParsingError(
                                f"Error in line {num} must not '-' in zone"
                                " word")

                        color = None
                        zone = 'normal'
                        max_drones = 1

                        if name not in name_hubs:
                            name_hubs.append(name)
                        else:
                            raise DuplicateName(
                                f"Error in line {num} {name} must not"
                                " duplicate")

                        self.hubs.append(
                            {
                                'type': key,
                                'name': name,
                                'x': int(x),
                                'y': int(y),
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

                        if first not in name_hubs or second not in name_hubs:
                            raise ConnectNameNotFound(
                                f"Error in line {num} this {first} not found"
                                " as zone")

                        edge = tuple(sorted([first, second]))

                        if edge in seen_connection:
                            raise DuplicateConnectionError(
                                f"Error in line {num} connection is there"
                                " before")

                        seen_connection.add(edge)

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

                        if first not in name_hubs or second not in name_hubs:
                            raise ConnectNameNotFound(
                                f"Error in line {num} this {first} not found"
                                " as zone")

                        edge = tuple(sorted([first, second]))

                        if edge in seen_connection:
                            raise DuplicateConnectionError(
                                f"Error in line {num} connection is there "
                                "before")

                        seen_connection.add(edge)

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

                if self.nb_drones == 0:
                    raise StartByNmDrone(
                        f"Error in line {num} the number of Drones must be"
                        " in the firt file")

                elif number_drones != 1:
                    raise DuplicateName(
                        f"Error in line {num} the number of Drones must be"
                        " not duplicat")

            for key in self.hubs:
                if key['type'] == "start_hub":
                    start_hub_is_there += 1
                elif key['type'] == "end_hub":
                    end_hub_is_there += 1

                if end_hub_is_there > 1:
                    raise DuplicateName(
                        f"Error in line {num} end_hubs must not duplicate")

                if start_hub_is_there > 1:
                    raise DuplicateName(
                        f"Error in line {num} start_hubs must not duplicate")

            if end_hub_is_there == 0:
                raise StartOrEndNotFound(
                    f"Error in line {num} end_hubs not found")

            if start_hub_is_there == 0:
                raise StartOrEndNotFound(
                    f"Error in line {num} start_hubs not found")
