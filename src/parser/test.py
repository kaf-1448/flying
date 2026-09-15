from typing import Dict, Any
import sys
from .exceptions import ThereNotFount


hubs = []
connections = []
nb_drones = 0
data: dict[str: Any] = {}

ALLOWED_ZONES = {"normal", "blocked", "restricted", "priority"}


with open(sys.argv[1], "r") as file:
    for num, line in enumerate(file, start=1):

        cleanedline = line.strip('\n').strip(' ')

        if not cleanedline or cleanedline.startswith('#'):
            continue

        key, value = cleanedline.split(':')
        key = key.strip(' ')
        value: str = value.strip(' ')

        if key == "nb_drones":
            nb_drones = int(value)

            # if nb_drones <= 0:
            #     raise PositiveNumber(
            #         f"error in line {num} nb_drones must be greath than from 0.")

        elif key in ("start_hub", "hub", "end_hub"):

            if '[' in value and ']' in value:

                main_part = value.split('[')[0]
                meta_data_part = value.strip(']').split('[')[1]

                name, x, y = main_part.strip(' ').split(' ')

                # # color = meta_data_part.split('=')
                color = None
                zone = 'normal'
                max_drones = 1

                # print(meta_data_part.split(' '))

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
                hubs.append(
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

                # # color = meta_data_part.split('=')
                color = None
                zone = 'normal'
                max_drones = 1

                hubs.append(
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

                connections.append(
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
                    # print(first)

                connections.append(
                    {
                        'type': key,
                        'from': first,
                        'to': second,
                        'meta_data': {
                            'max_capacity': 1
                        }
                    }
                )


# print(hubs)
# print(data)
# print(hubs)

# print(nb_drones)
# print(connections)

# print(hubs)


def check_errors(zones):
    end_hub_is_there = 0
    start_hub_is_there = 0
    is_duplicat = 0
    name_of_hubs = []

    for hubs in zones:

        if hubs['type'] == "end_hub":
            end_hub_is_there = 1

        if hubs['type'] == "start_hub":
            start_hub_is_there = 1
            print(hubs['type'])

        if hubs['name'] in name_of_hubs:
            is_duplicat = 1

        name_of_hubs.append(hubs['name'])

    # if end_hub_is_there or start_hub_is_there:
    #     if end_hub_is_there:
    #         raise ThereNotFount("end_hub not found")

    #     if start_hub_is_there:
    #         raise ThereNotFount("start_hub not found")

    # print(is_duplicat)

    if is_duplicat:
        raise DuplicateName()

    for x in connections:
        if x['from'] not in name_of_hubs:
            raise NameMapsParsingError()

        if x['to'] not in name_of_hubs:
            raise NameMapsParsingError()


# try:
#     check_errors(hubs)
# except ThereNotFount as e:
#     print(e)

check_errors(hubs)
