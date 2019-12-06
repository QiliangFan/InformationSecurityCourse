from numpy import ndarray


class LocationMap:
    """
    9: for row: 标定行坐标
    9: for col: 标定列坐标
    18 bits: sufficient!
    """
    def __init__(self, img_matrix: ndarray):
        self.modified_location = []
        for row in range(len(img_matrix)):
            for col in range(len(img_matrix[row])):
                if img_matrix[row][col] == 255:
                    self.modified_location.append((row, col))
                    img_matrix[row][col] = 254
                elif img_matrix[row][col] == 0:
                    self.modified_location.append((row, col))
                    img_matrix[row][col] = 1
        self.img_martix = img_matrix

    @property
    def location_map(self):
        result = ""
        result_row = 0
        result_col = 0
        for row, col in self.modified_location:
            result_row |= (2**(len(self.img_martix)-1)) >>row
            result_col |= (2**(len(self.img_martix[0])-1)) >>row
        result = "{0:0>9}{1:0>9}".format(result_row, result_col)
        return result