from numpy import ndarray
from typing import List
from typing import Tuple
from globaldata import parameter


class AuxiliaryInformation:
    """
    data encoding and data hiding for all kinds of Aux Info
    """

    k1 = -1  # represents the location of the last pixel-pair used in blank layer
    k2 = -1  # represents the location fo the last pixel-pair used in shadow layer

    def __init__(self):
        self.enc_thresholds_blank_and_shadow = ""
        self.enc_z_blank_and_shadow = ""
        self.enc_data_lens = ""

    def enc_data_len(self, data: str) -> str:
        data_len = len(data)
        encoded_data_len = bin(data_len).replace("0b", "")
        encoded_data_len = "{0:0>18}".format(encoded_data_len)
        self.enc_data_lens = encoded_data_len
        return encoded_data_len

    def enc_thresholds(self, threshold_list: List[int]) -> None:
        """
        12 bit for each threshold value.
        why? IDONKNOW.
        """
        result = []
        for threshold in threshold_list:
            bin_threshold = "{0:0>12}".format(bin(threshold).replace("0b", ""))
            result.append(bin_threshold)
        self.enc_thresholds_blank_and_shadow += "".join(result)

    def enc_z_value(self, z_list: List[int]) -> None:
        result = []
        for z in z_list:
            bin_z = "{0:0>3}".format(bin(z).replace("0b", ""))
            result.append(bin_z)
        self.enc_z_blank_and_shadow += "".join(result)

    def get_all_bits(self, location_map: str) -> str:
        result = []
        print("k1, k2", AuxiliaryInformation.k1, AuxiliaryInformation.k2)
        _k1 = "{0:0>18}".format(bin(AuxiliaryInformation.k1).replace("0b", ""))
        _k2 = "{0:0>18}".format(bin(AuxiliaryInformation.k2).replace("0b", ""))
        result.append(location_map)
        print(len(location_map))
        result.append(self.enc_data_lens)
        print(len(self.enc_data_lens))
        result.append(self.enc_thresholds_blank_and_shadow)
        print(len(self.enc_thresholds_blank_and_shadow))
        result.append(_k1 + _k2)
        print(len(_k1 + _k2))
        result.append(self.enc_z_blank_and_shadow)
        print(len(self.enc_z_blank_and_shadow))
        return "".join(result)

    def recover_aux_data(self, aux_data: str):
        self.location_map = aux_data[0: 18]
        self.enc_data_lens = aux_data[18: 36]
        self.blank_threshold_list = aux_data[36: (parameter.m-1) * 12 +36]
        self.shadow_threshold_list = aux_data[(parameter.m-1) * 12 + 36: 2 * (parameter.m-1) * 12 + 36]
        self.k1 = aux_data[2 * (parameter.m-1) * 12 + 36: 2 * (parameter.m-1) * 12 + 54]
        self.k2 = aux_data[2 * (parameter.m-1) * 12 + 54: 2 * (parameter.m-1) * 12 + 72]
        self.blank_z_list_str = aux_data[2 * (parameter.m-1) * 12 + 72: 2 * (parameter.m-1) * 12 + 72 + parameter.m * 3]
        self.shadow_z_list_str = aux_data[2 * (parameter.m-1) * 12 + 72 + parameter.m * 3: 2 * (parameter.m-1) * 12 + 72 + 2 * parameter.m * 3]

    def recover_location_map(self, img_matrix: ndarray):
        self.__row_location_map = self.location_map[0:9]
        self.__col_location_map = self.location_map[9:18]
        for row in range(len(img_matrix)):
            if self.__row_location_map[row] == "1":
                for col in range(len(img_matrix[row])):
                    if self.__col_location_map[col] =="1":
                        if img_matrix[row][col] == 254:
                            img_matrix[row][col] = 255
                        elif img_matrix[row][col] == 1:
                            img_matrix[row][col] = 0

    def recover_k1_k2(self) -> Tuple[int, int]:
        k1 = self.k1
        k2 = self.k2
        k1 = "0b" + k1
        k2 = "0b" + k2
        k1 = int(k1, 2)
        k2 = int(k2, 2)
        return k1, k2

    def recover_blank_z_list(self) -> List[int]:
        result = []
        for i in range(0, len(self.blank_z_list_str), 3):
            result.append(int("0b"+self.blank_z_list_str[i: i+3], 2))
        return result

    def recover_shadow_z_list(self) -> List[int]:
        result = []
        for i in range(0, len(self.shadow_z_list_str), 3):
            result.append(int("0b"+self.shadow_z_list_str[i: i+3], 2))
        return result

    def recover_data_len(self) -> int:
        data_len = int("0b" + self.enc_data_lens, 2)
        return data_len

    def recover_blank_threshold_list(self) -> List[int]:
        result = []
        for i in range(0, len(self.blank_threshold_list), 12):
            result.append(int("0b"+self.blank_threshold_list[i:i+12], 2))
        return result

    def recover_shadow_threshold_list(self) -> List[int]:
        result = []
        for i in range(0, len(self.shadow_threshold_list), 12):
            result.append(int("0b" + self.shadow_threshold_list[i:i + 12], 2))
        return result
