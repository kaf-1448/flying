seen = set()


s = "connection: start-waypoint1  [max_capacity=1]"

key, value = s.split(':')


data, meta_data = value.strip(']').split('[')

print(meta_data.split(' '))


# for item in meta_data.split(' '):

#     key = item.split('=')[0]
#     if key in {'color', 'max_drones', 'zone'} and key not in seen:
#         seen.add(key)
#         print(key)
#     else:
#         print(f'Error {key}')
