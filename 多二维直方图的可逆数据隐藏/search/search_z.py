from typing import List
from copy import deepcopy
from globaldata import parameter

def recursive_search(z_list: List[int], index: int):
    all_possibility = []  # for walking through the all possible z-list
    if index == len(z_list):
        all_possibility.append(deepcopy(z_list))
        return all_possibility
    for i in range(0, 7):
        z_list[index] = i
        all_possibility.extend(recursive_search(z_list, index + 1))
    return all_possibility


def compute_EC_ED(ex_ey_list: List[tuple], lc_list: List[int], threshold_list: List[int], z_list: List[int], data_len) -> (
        int, int):
    ED = 0
    EC = 0
    for (ex, ey), lc in zip(ex_ey_list, lc_list):
        index = 0
        while index < len(threshold_list) - 1 and lc > threshold_list[index]:
            index += 1
        z = z_list[index]
        if ex - ey == z and ex >= z:
            EC += 1
        elif ex + ey == z and ex > z:
            EC += 1
        elif ex - ey == z - 1 and ey >= z + 1:
            EC += 1
        elif ex + ey == z + 1 and ey > z + 1:
            EC += 1
        elif ex + ey == -z and ex <= -z:
            EC += 1
        elif ex - ey == -z and ex <= -z:
            EC += 1
        elif ex - ey == z + 1 and ey <= -z - 1:
            EC += 1
        elif ex + ey == -z - 1 and ey < -z - 1:
            EC += 1
        elif ex - ey > z and ex + ey > z:
            ED += 1
        elif ex - ey < -z - z and ex + ey > z + 1:
            ED += 1
        elif ex - ey < -z and ex + ey < -z:
            ED += 1
        elif ex - ey > z + 1 and ex + ey < -z - 1:
            ED += 1
    if EC >= data_len:
        return EC, ED
    else:
        return -1, -1
