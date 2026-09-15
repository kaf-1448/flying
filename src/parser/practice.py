from typing import Any, Dict

s = "hub: junction 1 0 [zone=resricted color=yellow max_drones=2]"
s = "hub: junction 1 0 [zone=resricted color=yellow max_drones=2]"
# s = "hub: junction 1 0 [color=yellow max_drones=2]"
# s = "hub: junction 1 0"


ALLOWED_ZONES = {"normal", "blocked", "restricted", "priority"}


def organize(value: str):

    # data: Dict[str:Any] = {
    #     meta_data: {
    #         'zone': 'normal',
    #         'color': 'none',
    #     }
    # }

    if '[' in s and ']' in s:
        main_part = s.split('[')[0]
        print(main_part)


print(organize(s))
