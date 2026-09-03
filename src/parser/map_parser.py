# class parser:
#     def __init__(self, nb_drones):

connections = []
hub = []

with open("../../maps/easy/01_linear_path.txt", "r") as file:
    for line in file:
        if line.startswith("#"):
            continue
        if line.startswith("\n"):
            continue
        if "nb_drones" in line:
            print(line.split(':')[1].strip(' '))
        if "start_hub" in line:
            print(line.split(':')[1].strip(' ').strip('\n').split(' '))
        if "end_hub" in line:
            print(line.split(':')[1].strip(' ').strip('\n').split(' '))
        if "hub" in line:
            hub.append(line.strip('\n').strip('#').split(":")[1])
        if "connection" in line:
            connections.append(line.split(':')[1].strip('\n'))
print(hub)
print(connections)


# ['start_hub', ' start 0 0 [color=green]\n']
# ['hub', ' waypoint1 1 0 [color=blue]\n']
# ['hub', ' waypoint2 2 0 [color=blue]\n']
# ['end_hub', ' goal 3 0 [color=red]\n']
# ['\n']
# ['connection', ' start-waypoint1\n']
# ['connection', ' waypoint1-waypoint2\n']
# ['connection', ' waypoint2-goal\n']
