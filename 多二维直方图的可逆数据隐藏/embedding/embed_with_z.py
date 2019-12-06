from typing import List
from entity.threshold import Threshold
from entity.pixelpair import PixelPair
from numpy import ndarray
from entity.auxiliaryinformation import AuxiliaryInformation
from globaldata import image_data


def embed(img_matrix: ndarray, pp_list: List[PixelPair], ex_ey_list: List[tuple], lc_list: List[int], threshold_list: List[int], z_list: List[int], data:str):
    data_index = 0
    print("times", image_data.times)
    index = 0
    print("len_pp, len_ex_ey, len_lc", len(pp_list), len(ex_ey_list), len(lc_list))
    for pp, (ex, ey), lc in zip(pp_list, ex_ey_list, lc_list):
        index += 1

        # print("len_data, data_index", len(data), data_index)

        if data_index > len(data) -1 :
            break
        threshold_index = 0
        while threshold_index < len(threshold_list) and lc > threshold_list[threshold_index]:
            threshold_index += 1
        z = z_list[threshold_index]
        xi = pp.xi
        xj = pp.xj
        yi = pp.yi
        yj = pp.yj

        if ex - ey == z and ex >= z:
            img_matrix[xi][xj] += int(data[data_index])
            if data_index == len(data) - 1:
                if image_data.times == 1:
                    AuxiliaryInformation.k1 = index
                    image_data.times += 1
                else:
                    AuxiliaryInformation.k2 = index
                    image_data.times += 1
            data_index += 1

        elif ex + ey == z and ex > z:
            img_matrix[xi][xj] += int(data[data_index])
            if data_index == len(data) - 1:
                if image_data.times == 1:
                    AuxiliaryInformation.k1 = index
                    image_data.times += 1
                else:
                    AuxiliaryInformation.k2 = index
                    image_data.times += 1
            data_index += 1

        elif ex - ey == -z - 1 and ey >= z + 1:
            img_matrix[yi][yj] += int(data[data_index])
            if data_index == len(data) - 1:
                if image_data.times == 1:
                    AuxiliaryInformation.k1 = index
                    image_data.times += 1
                else:
                    AuxiliaryInformation.k2 = index
                    image_data.times += 1
            data_index += 1

        elif ex + ey == z + 1 and ey > z + 1:
            img_matrix[yi][yj] += int(data[data_index])
            if data_index == len(data) - 1:
                if image_data.times == 1:
                    AuxiliaryInformation.k1 = index
                    image_data.times += 1
                else:
                    AuxiliaryInformation.k2 = index
                    image_data.times += 1
            data_index += 1

        elif ex + ey == -z and ex <= -z:
            img_matrix[xi][xj] -= int(data[data_index])
            if data_index == len(data) - 1:
                if image_data.times == 1:
                    AuxiliaryInformation.k1 = index
                    image_data.times += 1
                else:
                    AuxiliaryInformation.k2 = index
                    image_data.times += 1
            data_index += 1

        elif ex - ey == -z and ex < -z:
            img_matrix[xi][xj] -= int(data[data_index])
            if data_index == len(data) - 1:
                if image_data.times == 1:
                    AuxiliaryInformation.k1 = index
                    image_data.times += 1
                else:
                    AuxiliaryInformation.k2 = index
                    image_data.times += 1
            data_index += 1

        elif ex - ey == z + 1 and ey <= -z - 1:
            img_matrix[yi][yj] -= int(data[data_index])
            if data_index == len(data) - 1:
                if image_data.times == 1:
                    AuxiliaryInformation.k1 = index
                    image_data.times += 1
                else:
                    AuxiliaryInformation.k2 = index
                    image_data.times += 1
            data_index += 1

        elif ex + ey == -z - 1 and ey < -z - 1:
            img_matrix[yi][yj] -= int(data[data_index])
            if data_index == len(data) - 1:
                if image_data.times == 1:
                    AuxiliaryInformation.k1 = index
                    image_data.times += 1
                else:
                    AuxiliaryInformation.k2 = index
                    image_data.times += 1
            data_index += 1

        elif ex - ey > z and ex + ey > z:
            img_matrix[xi][xj] += 1
        elif ex - ey < -z - 1 and ex + ey > z + 1:
            img_matrix[yi][yj] += 1
        elif ex - ey < -z and ex + ey < -z:
            img_matrix[xi][xj] -= 1
        elif ex - ey > z + 1 and ex + ey < -z - 1:
            img_matrix[yi][yj] -= 1
    print("index, k1", index, AuxiliaryInformation.k1)
    print("index, k2", index, AuxiliaryInformation.k2)