from numpy import ndarray
from entity.pixelpair import PixelPair
from typing import List


class Recover:

    def recover(self, pp: PixelPair, lc: int, threshold_list: List[int], z_list: List[int], img_matrix: ndarray):
        xi, xj = pp.xi, pp.xj
        yi, yj = pp.yi, pp.yj

        up_pp = PixelPair(xi=xi - 1,
                          xj=xj,
                          yi=yi - 1,
                          yj=yj,
                          x=img_matrix[xi - 1][xj],
                          y=img_matrix[yi - 1][yj])
        down_pp = PixelPair(xi=xi + 1,
                            xj=xj,
                            yi=yi + 1,
                            yj=yj,
                            x=img_matrix[xi + 1][xj],
                            y=img_matrix[yi + 1][yj])
        left_pp = PixelPair(xi=xi,
                            xj=xj - 2,
                            yi=yi,
                            yj=yj - 2,
                            x=img_matrix[xi][xj - 2],
                            y=img_matrix[yi][yj - 2])
        right_pp = PixelPair(xi=xi,
                             xj=xj + 2,
                             yi=yi,
                             yj=yj + 2,
                             x=img_matrix[xi][xj + 2],
                             y=img_matrix[yi][yj + 2])

        ex, ey = pp.compute_ex_ey(up_pp,
                                 down_pp,
                                 left_pp,
                                 right_pp)

        threshold_index = 0
        while threshold_index < len(threshold_list) and lc > threshold_list[threshold_index]:
            threshold_index += 1
        z = z_list[threshold_index]

        if ex - ey == z and ex >= z:
            return "0"
        elif ex - ey == z + 1 and ex >= z + 1:
            img_matrix[xi][xj] -= 1
            return "1"

        elif ex + ey == z and ex > z:
            return "0"
        elif ex + ey == z+1 and ex > z+1:
            img_matrix[xi][xj] -= 1
            return "1"

        elif ex - ey == -z - 1 and ey >= z + 1:
            return "0"
        elif ex - ey == -z - 2 and ey >= z + 2:
            img_matrix[yi][yj] -= 1
            return "1"

        elif ex + ey == z + 1 and ey > z + 1:
            return "0"
        elif ex + ey == z + 2 and ey > z + 2:
            img_matrix[yi][yj] -= 1
            return "1"

        elif ex + ey == -z and ex <= -z:
            return "0"
        elif ex + ey == -z-1 and ex <= -z -1:
            img_matrix[xi][xj] += 1
            return "1"

        elif ex - ey == -z and ex <= -z:
            return "0"
        elif ex - ey == -z -1 and ex <= -z -1:
            img_matrix[xi][xj] += 1
            return "1"

        elif ex - ey == z + 1 and ey <= -z - 1:
            return "0"
        elif ex - ey == z + 2 and ey <= -z - 2:
            img_matrix[yi][yj] += 1
            return "1"

        elif ex + ey == -z - 1 and ey < -z - 1:
            return "0"
        elif ex + ey == -z - 2 and ey < -z -2:
            img_matrix[yi][yj] += 1
            return "1"

        elif ex - ey > z + 1 and ex + ey > z + 1:
            img_matrix[xi][xj] -= 1
        elif ex - ey < -z - 2 and ex + ey > z + 2:
            img_matrix[yi][yj] -= 1
        elif ex - ey < -z -1 and ex + ey < -z - 1:
            img_matrix[xi][xj] += 1
        elif ex - ey > z + 2 and ex + ey < -z - 2:
            img_matrix[yi][yj] += 1
        return ""
