parsing = []
connections = []
hub = []
is_start_there = 0
is_end_there = 0


class MapParser:
    def __init__(self):
        self.nb_drones = 0
        self.hubs = []
        self.connections = []

    def read_file(self, path):
        with open("../../maps/easy/01_linear_path.txt", "r") as file:
            for num, line in enumerate(file, start=1):

                cleanedline = line.strip('\n').strip(' ')

                if not cleanedline or cleanedline.startswith('#'):
                    continue

                key, value = cleanedline.split(':')
                key = key.strip(' ')
                value = value.strip(' ')

                if key == "nb_drones":
                    self.nb_drones = int(value)

                elif key in ("start_hub", "hub", "end_hub"):
                    value = value.split(' ')

                    if len(value) == 4:
                        self.hubs.append(
                            {
                                'type': key,
                                'name': value[0],
                                'x': value[1],
                                'y': value[2],
                                'meta_data': value[3]
                            }
                        )
                    elif len(value) == 3:
                        self.hubs.append(
                            {
                                'type': key,
                                'name': value[0],
                                'x': value[1],
                                'y': value[2],
                            }
                        )

                elif key == "connection":
                    self.connections.append(value)


hubs = []
connections = []
nb_drones = 0


with open("../../maps/easy/01_linear_path.txt", "r") as file:
    for num, line in enumerate(file, start=1):

        cleanedline = line.strip('\n').strip(' ')

        if not cleanedline or cleanedline.startswith('#'):
            continue

        key, value = cleanedline.split(':')
        key = key.strip(' ')
        value = value.strip(' ')

        if key == "nb_drones":
            nb_drones = int(value)

        elif key in ("start_hub", "hub", "end_hub"):
            value = value.split(' ')

            if len(value) == 4:
                hubs.append(
                    {
                        'type': key,
                        'name': value[0],
                        'x': value[1],
                        'y': value[2],
                        'meta_data': value[3]
                    }
                )
            elif len(value) == 3:
                hubs.append(
                    {
                        'type': key,
                        'name': value[0],
                        'x': value[1],
                        'y': value[2],
                    }
                )

        elif key == "connection":
            connections.append(value)

print(nb_drones)
print(connections)
print(hubs)
