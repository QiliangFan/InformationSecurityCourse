from numpy import ndarray

class LSBs:

    """
    the least significant bits for data hiding
    """
    def __init__(self, data: str, img_matrix: ndarray):
        """
        辅助信息的长度, 假定是约定好相互告知的!
        :param data:
        :param img_matrix:
        """
        times = 1
        for i in range(len(img_matrix)):
            for j in range(len(img_matrix[i])):
                if times <= len(data):
                    if j % 2 == 0:  # even: increase or unchanged
                        img_matrix[i][j] += int(data[times-1])
                    else:           # odd: decrease or unchanged
                        img_matrix[i][j] -= int(data[times-1])
                    times += 1

    def recover(self, modified_img: ndarray, original_img: ndarray, len_aux_info: int) -> str:
        result = []
        times = 1
        for i in range(len(modified_img)):
            if times > len_aux_info:
                break
            for j in range(len(modified_img[i])):
                if times <= len_aux_info:
                    if j % 2 == 0:               # even: decrease or unchanged
                        if modified_img[i][j] != original_img[i][j]:
                            modified_img[i][j] -= 1
                            result.append("1")
                        else:
                            result.append("0")
                    else:                       # odd: increase or unchanged
                        if modified_img[i][j] != original_img[i][j]:
                            modified_img[i][j] += 1
                            result.append("1")
                        else:
                            result.append("0")
                    times += 1

        return "".join(result)