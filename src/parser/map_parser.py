from typing import Dict, Any, List, Set, Optional, Tuple
from .exceptions import DuplicateName, NameMapsParsingError
from .exceptions import ConnectNameNotFound, StartByNmDrone
from .exceptions import StartOrEndNotFound, PositiveNumber
from .exceptions import DuplicateConnectionError, MetaDataError
from .exceptions import SyntaxError


ALLOWED_ZONES: Set[str] = {"normal", "blocked", "restricted", "priority"}


class MapParser:
    def __init__(self) -> None:
        self.nb_drones: int = 0
        self.hubs: List[Dict[str, Any]] = []
        self.connections: List[Dict[str, Any]] = []

    def read_file(self, path: str) -> None:

        if path is None:
            raise FileNotFoundError("Error File not found")

        num = 0

        with open(path, "r") as file:
            end_hub_is_there: int = 0
            start_hub_is_there: int = 0
            number_drones: int = 0
            name_hubs: List[str] = []
            seen_connection: Set[Tuple[str, str]] = set()

            for num, line in enumerate(file, start=1):

                if '#' in line:
                    line = line.split('#', 1)[0]

                cleanedline = line.strip('\n').strip(' ')

                if not cleanedline:
                    continue

                if ':' not in cleanedline:
                    raise SyntaxError(
                        f"Error in line {num}: missing ':' separator")

                if cleanedline.count(':') > 1:
                    raise SyntaxError(
                        f"Error in line {num}: extra ':' separator")

                key, value = cleanedline.split(':')
                key = key.strip(' ')
                value = value.strip(' ')

                if key == "nb_drones":

                    try:
                        self.nb_drones = int(value)

                    except ValueError:
                        raise ValueError(
                            f"Error in line {num}: nb_drones must"
                            " be number")

                    if self.nb_drones <= 0:
                        raise PositiveNumber(
                            f"Error in line {num}: nb_drones must be greath"
                            " than from 0.")
                    number_drones += 1

                elif key in ("start_hub", "hub", "end_hub"):

                    if '[' in value and ']' in value:

                        try:

                            main_part = value.split('[')[0]
                            parts = main_part.split()
                            if len(parts) > 3:
                                raise SyntaxError(
                                    f"Error in line {num}: extra data "
                                    "must syntax must "
                                    "coordinates (expected name, x, y)")
                            elif len(parts) != 3:
                                raise SyntaxError(
                                    f"Error in line {num}: missing "
                                    "coordinates (expected name, x, y)")

                            meta_data_part = value.strip(']').split('[')[
                                1]

                            # if (len(meta_data_part.split()) > 1):
                            #     raise SyntaxError(
                            #         f"Error line in {num}"
                            #         f"is extra data must syntax"
                            #         f"as (name x y [meta data])")

                            name, x, y = main_part.strip(' ').split()

                            if '-' in name:
                                raise NameMapsParsingError(
                                    f"Error in line {num}: "
                                    "must not '-' in zone word")

                            color: Optional[str] = None
                            zone: str = 'normal'
                            max_drones: int = 1

                            seen = set()
                            for item in meta_data_part.split():

                                meta_key = item.split('=')[0]

                                if (meta_key in {'color', 'zone', 'max_drones'}
                                        and meta_key not in seen):

                                    if 'color' in item:
                                        seen.add('color')
                                        color = item.split('=')[1]

                                    if "max_drones" in item:

                                        try:
                                            max_drones = int(
                                                item.split('=')[1].strip(' '))
                                        except ValueError:
                                            raise ValueError(
                                                f"Error in line {num}: "
                                                "max_drones "
                                                "must be number")

                                        if max_drones <= 0:
                                            raise PositiveNumber(
                                                f"Error in line {num}:"
                                                "max_drones must "
                                                "be greath than 0.")
                                        seen.add('max_drones')

                                    if 'zone' in item:
                                        is_zone_there = item.split('=')[1]
                                        if is_zone_there in ALLOWED_ZONES:
                                            zone = is_zone_there
                                        else:
                                            raise MetaDataError(
                                                f"Error in line {num}: "
                                                "in meta data"
                                            )
                                        seen.add('zone')
                                elif (meta_key in {'color',
                                                   'zone',
                                                   'max_drones'} and
                                      meta_key in seen):
                                    raise MetaDataError(
                                        f"Error in line {num}: in meta data "
                                        f"'{meta_key}' is there before"
                                    )

                                else:
                                    raise MetaDataError(
                                        f"Error in line {num}: in meta data "
                                        f"{meta_key} is must be not here")

                            if name not in name_hubs:
                                name_hubs.append(name)
                            else:
                                raise DuplicateName(
                                    f"Error in line {num}: {name} must not"
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
                                        'max_drones': max_drones
                                    }
                                }
                            )
                        except ValueError:
                            raise ValueError(
                                f"Error in line {num}: x or y "
                                "must be interger number")

                    elif '[' not in value and ']'not in value:
                        try:
                            main_part = value.split('[')[0]
                            parts = main_part.strip().split()

                            if len(parts) > 3:
                                garbage = " ".join(parts[3:])
                                raise MetaDataError(
                                    f"Error in line {num}: extra data"
                                    f" '{garbage}' is not allowed"
                                )
                            elif len(parts) < 3:
                                raise MetaDataError(
                                    f"Error in line {num}: missing "
                                    f"coordinates (expected name, x, y)"
                                )

                            name, x, y = parts[0], parts[1], parts[2]

                            if '-' in name:
                                raise NameMapsParsingError(
                                    f"Error in line {num}: "
                                    "must not '-' in zone word")

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
                                        'max_drones': max_drones
                                    }
                                }
                            )
                        except ValueError:
                            raise ValueError(
                                f"Error in line {num} x or y "
                                "must be interger number")
                    else:
                        raise MetaDataError(
                            f"Error in line {num} in meta data syntax"
                            f" must be [zone=x ...]"
                        )

                elif key == "connection":

                    if '[' in value and ']' in value:

                        main_part = value.strip(' ').split('[')[0]

                        if (len(main_part.split()) != 1
                                or '-' not in main_part.split()[0]):
                            raise SyntaxError(
                                f"Error in line {num}"
                                "must syntax"
                                "node1-node2 [meta data]"
                            )

                        node = main_part.strip().split('-')

                        if len(node) > 2:
                            raise SyntaxError(
                                f"Error in line {num}"
                                " extra data, must syntax"
                                "node1-node2 [meta data] or"
                                " node1-node2"
                            )
                        elif len(node) < 2:
                            raise SyntaxError(
                                f"Error in line {num}"
                                " missing data, must syntax"
                                "node1-node2 [meta data] or"
                                " node1-node2"
                            )

                        conn_meta = (
                            value.strip(']').split('[')[
                                1].strip(' ').split())

                        if len(conn_meta) == 0:
                            raise MetaDataError(
                                f"Error in line {num} in meta data "
                                "must be not Empty between []")

                        elif len(conn_meta) != 1:
                            raise SyntaxError(
                                f"Error in line {num} extra data "
                                "must syntax must "
                                "coordinates (node1-node2 [meta data])")

                        else:

                            max_capacity: int = 1
                            if (len(conn_meta) > 1):
                                raise MetaDataError(
                                    f"Error in line {num} in meta data "
                                    "must be only max capacity or max link"
                                    " capacity")
                            elif (len(conn_meta) == 1 and (
                                    conn_meta[0].split(
                                        '=')[0] == "max_capacity"
                                    or conn_meta[0].split('=')[0]
                                    == "max_link_capacity")):
                                try:
                                    max_capacity = int(
                                        conn_meta[0].split('=')[1])
                                except ValueError:
                                    raise ValueError(
                                        f"Error in line {num} must be number")

                                if max_capacity <= 0:
                                    raise PositiveNumber(
                                        f"Error in line {num}"
                                        f" max_capacity must be"
                                        " greath than 0.")
                            else:
                                raise MetaDataError(
                                    f"Error in line {num} in meta data "
                                    "must be only max capacity or max link"
                                    " capacity")

                        first, second = main_part.strip(' ').split('-')

                        if first == second:
                            raise MetaDataError(
                                f"Error in line {num}: "
                                " connection cannot link zone to itself")

                        if first not in name_hubs or second not in name_hubs:
                            raise ConnectNameNotFound(
                                f"Error in line {num} this {first} not found"
                                " as zone")

                        sorted_nodes = sorted([first, second])
                        edge: Tuple[str, str] = (
                            sorted_nodes[0], sorted_nodes[1])

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
                                    'max_capacity': max_capacity
                                }
                            }
                        )

                    elif '[' not in value and ']' not in value:

                        parts_conn = value.strip().split()

                        if len(parts_conn) != 1 or '-' not in parts_conn[0]:
                            raise MetaDataError(
                                f"Error in line {num}: invalid"
                                f" connection format")

                        nodes = parts_conn[0].split('-')
                        if len(nodes) != 2:
                            raise MetaDataError(
                                f"Error in line {num}: connection must"
                                f" have exactly two hubs")

                        first, second = nodes

                        if first == second:
                            raise MetaDataError(
                                f"Error in line {num}: "
                                " connection cannot link zone to itself")

                        if first not in name_hubs or second not in name_hubs:
                            raise ConnectNameNotFound(
                                f"Error in line {num} this {first} not found"
                                " as zone")

                        sorted_nodes = sorted([first, second])
                        edge = (sorted_nodes[0], sorted_nodes[1])

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

                    else:
                        raise MetaDataError(
                            f"Error in line {num} in meta data "
                            f" syntax must be [max_capacity=x]"
                        )
                else:
                    raise SyntaxError(
                        f"Error in line {num}: unknown directive '{key}'")

                if self.nb_drones == 0:
                    raise StartByNmDrone(
                        f"Error in line {num} the number of Drones must be"
                        " in the firt file")

                elif number_drones != 1:
                    raise DuplicateName(
                        f"Error in line {num} the number of Drones must be"
                        " not duplicat")

            for hub_dict in self.hubs:
                if hub_dict['type'] == "start_hub":
                    start_hub_is_there += 1
                elif hub_dict['type'] == "end_hub":
                    end_hub_is_there += 1

                if end_hub_is_there > 1:
                    raise DuplicateName(
                        f"Error in line {num} end_hubs must not duplicate")

                if start_hub_is_there > 1:
                    raise DuplicateName(
                        f"Error in line {num} start_hubs must not duplicate")

            if start_hub_is_there == 0:
                raise StartOrEndNotFound(
                    f"Error in line {num} start_hubs not found")

            if end_hub_is_there == 0:
                raise StartOrEndNotFound(
                    f"Error in line {num} end_hubs not found")
