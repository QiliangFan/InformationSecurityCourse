import random
import sys

from typing import List
from globaldata import image_data
from globaldata import parameter
from tools.compute_PSNR import get_psnr
from utils import plot_psnr
from utils.image_process import load_image_matrix
from entity.pixelpair import PixelPair
from entity.threshold import Threshold
from entity.locationmap import LocationMap
from entity.auxiliaryinformation import AuxiliaryInformation
from entity.lsbs import LSBs
from search.search_z import recursive_search
from search.search_z import compute_EC_ED
from embedding.embed_with_z import embed
from copy import deepcopy
from PIL import Image
from recovery.recover import Recover
from utils.plot_psnr import plot_psnr_by_databits
import matplotlib.pyplot as plt



def get_ex_ey(pp_list: List[PixelPair], ex_ey_list: List[tuple], image_matrix):
    for item in pp_list:
        xi, xj = item.xi, item.xj
        yi, yj = item.yi, item.yj
        up_pp = PixelPair(xi=xi - 1,
                          xj=xj,
                          yi=yi - 1,
                          yj=yj,
                          x=image_matrix[xi - 1][xj],
                          y=image_matrix[yi - 1][yj])
        down_pp = PixelPair(xi=xi + 1,
                            xj=xj,
                            yi=yi + 1,
                            yj=yj,
                            x=image_matrix[xi + 1][xj],
                            y=image_matrix[yi + 1][yj])
        left_pp = PixelPair(xi=xi,
                            xj=xj - 2,
                            yi=yi,
                            yj=yj - 2,
                            x=image_matrix[xi][xj - 2],
                            y=image_matrix[yi][yj - 2])
        right_pp = PixelPair(xi=xi,
                             xj=xj + 2,
                             yi=yi,
                             yj=yj + 2,
                             x=image_matrix[xi][xj + 2],
                             y=image_matrix[yi][yj + 2])
        ex_ey_list.append(item.compute_ex_ey(up_pp,
                                             down_pp,
                                             left_pp,
                                             right_pp))


def get_lc(item: PixelPair, image_matrix) -> int:
    xi, xj = item.xi, item.xj
    yi, yj = item.yi, item.yj
    up_pp = PixelPair(xi=xi - 1,
                      xj=xj,
                      yi=yi - 1,
                      yj=yj,
                      x=image_matrix[xi - 1][xj],
                      y=image_matrix[yi - 1][yj])
    left_pp = PixelPair(xi=xi,
                        xj=xj - 2,
                        yi=yi,
                        yj=yj - 2,
                        x=image_matrix[xi][xj - 2],
                        y=image_matrix[yi][yj - 2])
    right_pp = PixelPair(xi=xi,
                         xj=xj + 2,
                         yi=yi,
                         yj=yj + 2,
                         x=image_matrix[xi][xj + 2],
                         y=image_matrix[yi][yj + 2])
    ld_pp = PixelPair(xi=xi + 1,
                      xj=xj - 2,
                      yi=yi + 1,
                      yj=yj - 2,
                      x=image_matrix[xi + 1][xj - 2],
                      y=image_matrix[yi + 1][yj - 2])
    down_pp = PixelPair(xi=xi + 1,
                        xj=xj,
                        yi=yi + 1,
                        yj=yj,
                        x=image_matrix[xi + 1][xj],
                        y=image_matrix[yi + 1][yj])
    rd_pp = PixelPair(xi=xi + 1,
                      xj=xj + 2,
                      yi=yi + 1,
                      yj=yj + 2,
                      x=image_matrix[xi + 1][xj + 2],
                      y=image_matrix[yi + 1][yj + 2])
    bottom_pp_1 = PixelPair(xi=xi + 2,
                            xj=xj - 2,
                            yi=yi + 2,
                            yj=yj - 2,
                            x=image_matrix[xi + 2][xj - 2],
                            y=image_matrix[yi + 2][yj - 2])
    bottom_pp_2 = PixelPair(xi=xi + 2,
                            xj=xj,
                            yi=yi + 2,
                            yj=yj,
                            x=image_matrix[xi + 2][xj],
                            y=image_matrix[yi + 2][yj])
    bottom_pp_3 = PixelPair(xi=xi + 2,
                            xj=xj + 2,
                            yi=yi + 2,
                            yj=yj + 2,
                            x=image_matrix[xi + 2][xj + 2],
                            y=image_matrix[yi + 2][yj + 2])
    return item.compute_LC(up_pp,
                           left_pp,
                           right_pp,
                           ld_pp,
                           down_pp,
                           rd_pp,
                           bottom_pp_1,
                           bottom_pp_2,
                           bottom_pp_3)


def get_lc_list(pp_list: List[PixelPair], lc_list: List[int], image_matrix):
    for item in pp_list:
        lc_list.append(get_lc(item, image_matrix))


def main():
    global data
    data1 = data[0:len(data) // 2]
    data2 = data[len(data) // 2:]
    img_matrix = load_image_matrix("img/1.bmp")
    aux_info = AuxiliaryInformation()

    # init the location map
    L_map = LocationMap(img_matrix)
    compressed_location_map = L_map.location_map

    # init the encoded data length
    compressed_data_len = aux_info.enc_data_len(data)
    print("compressed_data_len:", compressed_data_len)

    if image_data.image_width == -1 or image_data.image_height == -1:
        print("初始化时出现未知错误!")
        sys.exit(0)

    # blank pixel-pair
    blank_pp_list = []
    blank_LC_list = []
    blank_ex_ey_list = []

    # shadow pixel-pair
    shadow_pp_list = []
    shadow_LC_list = []
    shadow_ex_ey_list = []

    # blank pixel-pair RDH
    for row in range(0, len(img_matrix)):
        if row % 2 == 1:
            for col in range(2, len(img_matrix[row]), 4):
                if row <= 0:
                    continue
                if col <= 0:
                    continue
                if row >= image_data.image_height - 2:
                    break
                if col >= image_data.image_width - 2:
                    break
                blank_pp_list.append(PixelPair(xi=row,
                                               xj=col,
                                               yi=row,
                                               yj=col + 1,
                                               x=img_matrix[row][col],
                                               y=img_matrix[row][col + 1]))
        elif row % 2 == 0:
            for col in range(4, len(img_matrix[row]), 4):

                if row <= 0:
                    continue
                if col <= 2:
                    continue
                if row >= image_data.image_height - 2:
                    break
                if col >= image_data.image_width - 2:
                    break
                blank_pp_list.append(PixelPair(xi=row,
                                               xj=col,
                                               yi=row,
                                               yj=col + 1,
                                               x=img_matrix[row][col],
                                               y=img_matrix[row][col + 1]))
    get_ex_ey(blank_pp_list, blank_ex_ey_list, image_matrix=img_matrix)
    get_lc_list(blank_pp_list, blank_LC_list, image_matrix=img_matrix)
    blank_thereshold = Threshold(pp_list=blank_pp_list, lc_list=blank_LC_list, m=parameter.m)
    blank_thereshold_list = blank_thereshold.get_all_thereshold()
    print("blank_threshold:", blank_thereshold_list)

    # encode the threshold value
    aux_info.enc_thresholds(blank_thereshold_list)

    # for img modifying
    copy_img_matrix = deepcopy(img_matrix)

    print(blank_thereshold_list)
    print(blank_LC_list)
    blank_z_list = [0] * parameter.m
    blank_all_possible_z = recursive_search(blank_z_list, 0)
    min_ED_div_EC = 9999999999999999
    temp_z_list = []
    for z_list in blank_all_possible_z:
        EC, ED = compute_EC_ED(blank_ex_ey_list, blank_LC_list, blank_thereshold_list, z_list, len(data1))
        if (EC, ED) != (-1, -1):
            if ED / EC < min_ED_div_EC:
                temp_z_list = deepcopy(z_list)
    blank_z_list = temp_z_list
    print("blank_z_list:", blank_z_list)

    # init the z_list  enc
    aux_info.enc_z_value(blank_z_list)

    embed(copy_img_matrix,
          blank_pp_list,
          blank_ex_ey_list,
          blank_LC_list,
          blank_thereshold_list,
          blank_z_list,
          data1)

    # # shadow pixel-pair RDH
    for row in range(len(copy_img_matrix)):
        if row % 2 == 0:
            for col in range(2, len(copy_img_matrix[row]), 4):
                if row <= 0:
                    continue
                if col <= 0:
                    continue
                if row >= image_data.image_height - 2:
                    break
                if col >= image_data.image_width - 2:
                    break
                shadow_pp_list.append(PixelPair(xi=row,
                                                xj=col,
                                                yi=row,
                                                yj=col + 1,
                                                x=copy_img_matrix[row][col],
                                                y=copy_img_matrix[row][col + 1]))
        elif row % 2 == 1:
            for col in range(4, len(copy_img_matrix[row]), 4):
                if row <= 0:
                    continue
                if col <= 2:
                    continue
                if row >= image_data.image_height - 2:
                    break
                if col >= image_data.image_width - 2:
                    break
                shadow_pp_list.append(PixelPair(xi=row,
                                                xj=col,
                                                yi=row,
                                                yj=col + 1,
                                                x=copy_img_matrix[row][col],
                                                y=copy_img_matrix[row][col + 1]))
    get_ex_ey(shadow_pp_list, shadow_ex_ey_list, image_matrix=copy_img_matrix)
    get_lc_list(shadow_pp_list, shadow_LC_list, image_matrix=copy_img_matrix)

    shadow_threshold = Threshold(pp_list=shadow_pp_list, lc_list=shadow_LC_list, m=parameter.m)
    shadow_threshold_list = shadow_threshold.get_all_thereshold()
    print("shadow_threshold:", shadow_threshold_list)

    # encode the threshold
    aux_info.enc_thresholds(shadow_threshold_list)

    print(shadow_threshold_list)
    print(shadow_LC_list)
    shadow_z_list = [0] * parameter.m
    shadow_all_possible_z = recursive_search(shadow_z_list, 0)
    min_ED_div_EC = 9999999999999999
    temp_z_list = []
    for z_list in shadow_all_possible_z:
        EC, ED = compute_EC_ED(shadow_ex_ey_list, shadow_LC_list, shadow_threshold_list, z_list, len(data2))
        if (EC, ED) != (-1, -1):
            if ED / EC < min_ED_div_EC:
                temp_z_list = deepcopy(z_list)
    shadow_z_list = temp_z_list
    print("shadow_z_list:", shadow_z_list)

    # init the z value enc
    aux_info.enc_z_value(shadow_z_list)

    embed(copy_img_matrix,
          shadow_pp_list,
          shadow_ex_ey_list,
          shadow_LC_list,
          shadow_threshold_list,
          shadow_z_list,
          data2)

    tmp_shadow_ex = [ex for ex,ey in shadow_ex_ey_list]
    tmp_shadow_ey = [ey for ex,ey in shadow_ex_ey_list]

    tmp_blank_ex = [ex for ex,ey in blank_ex_ey_list]
    tmp_blank_ey = [ey for ex,ey in blank_ex_ey_list]

    plt.figure()
    plt.hist([item[0] for item in blank_ex_ey_list if item[1] == 3], bins=400)
    plt.xlim(-20, 20)
    plt.ylabel("the number of pixel pairs")
    plt.xlabel("ex")
    plt.grid(True)
    plt.show()

    # plt.figure()
    # plt.hist2d(tmp_blank_ex, tmp_blank_ey, bins=(400, 400))
    # plt.xlim(-10, 10)
    # plt.ylim(-10, 10)
    # plt.show()
    #
    # plt.figure()
    # plt.hist2d(tmp_shadow_ex, tmp_shadow_ey, bins=(400, 400))
    # plt.xlim(-10, 10)
    # plt.ylim(-10, 10)
    # plt.show()

    print("总共要隐藏的数据无损： ",(data1 + data2) == data)

    Image.fromarray(copy_img_matrix).save("lenna_without_aux.bmp")

    gout = False
    for row in range(len(copy_img_matrix)):
        for col in range(len(copy_img_matrix[row])):
            if img_matrix[row][col] != copy_img_matrix[row][col]:
                print("图像进行了修改!")
                gout = True
                if gout:
                    break
        if gout:
            break

    # all aux_bits
    all_aux_bits = aux_info.get_all_bits(compressed_location_map)
    print(all_aux_bits)

    print("blank_lc_list", blank_LC_list)
    print("len", len(blank_LC_list))
    print("shadow_lc_list", shadow_LC_list)
    print("len", len(shadow_LC_list))

    # LSBs replacements
    lsb = LSBs(all_aux_bits, copy_img_matrix)

    img_with_data = Image.fromarray(copy_img_matrix)
    with open("lenna_with_data.bmp", "wb") as fp:
        img_with_data.save(fp)

    # ====================================================================start to recover the image!
    recover_aux_info_bits = lsb.recover(copy_img_matrix, img_matrix, len(all_aux_bits))
    print(recover_aux_info_bits)
    print(recover_aux_info_bits == all_aux_bits)

    aux_info.recover_aux_data(recover_aux_info_bits)

    # k1\ k2
    k1, k2 = aux_info.recover_k1_k2()
    print("k1, k2: ", k1, k2)

    # data_len
    recover_data_len = aux_info.recover_data_len()
    print("recover_data_len: ", recover_data_len)

    # z_list:
    recover_blank_z_list = aux_info.recover_blank_z_list()
    recover_shadow_z_list = aux_info.recover_shadow_z_list()
    print("recover_blank_z_list:", recover_blank_z_list)
    print("recover_shadow_z_list:", recover_shadow_z_list)

    # threshold_list:
    recover_shadow_threshold_list = aux_info.recover_shadow_threshold_list()
    recover_blank_threshold_list = aux_info.recover_blank_threshold_list()

    print("recover_blank_threshold_list:", recover_blank_threshold_list)
    print("recover_shadow_threshold_list:", recover_shadow_threshold_list)

    recover = Recover()
    result_secret_data = ""

    # lc_list:
    recover_blank_LC_list = []
    recover_shadow_LC_list = []

    # # recover in shadow layer:
    recover_shadow_pp_list = []
    number = 0
    for row in range(len(copy_img_matrix)):
        if number >= k2:
            break
        if row % 2 == 0:
            for col in range(2, len(copy_img_matrix[row]), 4):
                if number >= k2:
                    break
                if row <= 0:
                    continue
                if col <= 0:
                    continue
                if row >= image_data.image_height - 2:
                    break
                if col >= image_data.image_width - 2:
                    break
                recover_shadow_pp_list.append(PixelPair(xi=row,
                                                        xj=col,
                                                        yi=row,
                                                        yj=col + 1,
                                                        x=copy_img_matrix[row][col],
                                                        y=copy_img_matrix[row][col + 1]))
                number += 1

        elif row % 2 == 1:
            for col in range(4, len(copy_img_matrix[row]), 4):
                if number >= k2:
                    break
                if row <= 0:
                    continue
                if col <= 0:
                    continue
                if row >= image_data.image_height - 2:
                    break
                if col >= image_data.image_width - 2:
                    break
                recover_shadow_pp_list.append(PixelPair(xi=row,
                                                        xj=col,
                                                        yi=row,
                                                        yj=col + 1,
                                                        x=copy_img_matrix[row][col],
                                                        y=copy_img_matrix[row][col + 1]))
                number += 1
        print("k2, number", k2, number)

    data_index = 0

    for pp in reversed(recover_shadow_pp_list):
        xi, xj = pp.xi, pp.xj
        yi, yj = pp.yi, pp.yj

        pp.x = copy_img_matrix[xi][xj]
        pp.y = copy_img_matrix[yi][yj]

        up_pp = PixelPair(xi=xi - 1,
                          xj=xj,
                          yi=yi - 1,
                          yj=yj,
                          x=copy_img_matrix[xi - 1][xj],
                          y=copy_img_matrix[yi - 1][yj])
        left_pp = PixelPair(xi=xi,
                            xj=xj - 2,
                            yi=yi,
                            yj=yj - 2,
                            x=copy_img_matrix[xi][xj - 2],
                            y=copy_img_matrix[yi][yj - 2])
        right_pp = PixelPair(xi=xi,
                             xj=xj + 2,
                             yi=yi,
                             yj=yj + 2,
                             x=copy_img_matrix[xi][xj + 2],
                             y=copy_img_matrix[yi][yj + 2])
        ld_pp = PixelPair(xi=xi + 1,
                          xj=xj - 2,
                          yi=yi + 1,
                          yj=yj - 2,
                          x=copy_img_matrix[xi + 1][xj - 2],
                          y=copy_img_matrix[yi + 1][yj - 2])
        down_pp = PixelPair(xi=xi + 1,
                            xj=xj,
                            yi=yi + 1,
                            yj=yj,
                            x=copy_img_matrix[xi + 1][xj],
                            y=copy_img_matrix[yi + 1][yj])
        rd_pp = PixelPair(xi=xi + 1,
                          xj=xj + 2,
                          yi=yi + 1,
                          yj=yj + 2,
                          x=copy_img_matrix[xi + 1][xj + 2],
                          y=copy_img_matrix[yi + 1][yj + 2])
        bottom_pp_1 = PixelPair(xi=xi + 2,
                                xj=xj - 2,
                                yi=yi + 2,
                                yj=yj - 2,
                                x=copy_img_matrix[xi + 2][xj - 2],
                                y=copy_img_matrix[yi + 2][yj - 2])
        bottom_pp_2 = PixelPair(xi=xi + 2,
                                xj=xj,
                                yi=yi + 2,
                                yj=yj,
                                x=copy_img_matrix[xi + 2][xj],
                                y=copy_img_matrix[yi + 2][yj])
        bottom_pp_3 = PixelPair(xi=xi + 2,
                                xj=xj + 2,
                                yi=yi + 2,
                                yj=yj + 2,
                                x=copy_img_matrix[xi + 2][xj + 2],
                                y=copy_img_matrix[yi + 2][yj + 2])
        lc = pp.compute_LC(up_pp,
                           left_pp,
                           right_pp,
                           ld_pp,
                           down_pp,
                           rd_pp,
                           bottom_pp_1,
                           bottom_pp_2,
                           bottom_pp_3)
        recover_shadow_LC_list.append(lc)
        temp_result = recover.recover(pp,
                                      lc,
                                      recover_shadow_threshold_list,
                                      recover_shadow_z_list,
                                      copy_img_matrix)

        if len(temp_result) > 0:
            data_index += 1
            result_secret_data += temp_result
        if data_index >= recover_data_len - recover_data_len // 2:
            break

    # recover in blank layer:
    recover_blank_pp_list = []
    number = 0
    for row in range(len(copy_img_matrix)):
        if number >= k1:
            break
        if row % 2 == 1:
            for col in range(2, len(copy_img_matrix[row]), 4):
                if number >= k1:
                    break
                if row <= 0:
                    continue
                if col <= 1:
                    continue
                if row >= image_data.image_height - 2:
                    break
                if col >= image_data.image_width - 2:
                    break
                recover_blank_pp_list.append(PixelPair(xi=row,
                                                       xj=col,
                                                       yi=row,
                                                       yj=col + 1,
                                                       x=copy_img_matrix[row][col],
                                                       y=copy_img_matrix[row][col + 1]))
                number += 1
        elif row % 2 == 0:
            for col in range(4, len(copy_img_matrix[row]), 4):
                if number >= k1:
                    break
                if row <= 0:
                    continue
                if col <= 1:
                    continue
                if row >= image_data.image_height - 2:
                    break
                if col >= image_data.image_width - 2:
                    break
                recover_blank_pp_list.append(PixelPair(xi=row,
                                                       xj=col,
                                                       yi=row,
                                                       yj=col + 1,
                                                       x=copy_img_matrix[row][col],
                                                       y=copy_img_matrix[row][col + 1]))
                number += 1
        print("k1, number", k1, number)

    data_index = 0

    for pp in reversed(recover_blank_pp_list):
        xi, xj = pp.xi, pp.xj
        yi, yj = pp.yi, pp.yj
        pp.x = copy_img_matrix[xi][xj]
        pp.y = copy_img_matrix[yi][yj]
        up_pp = PixelPair(xi=xi - 1,
                          xj=xj,
                          yi=yi - 1,
                          yj=yj,
                          x=copy_img_matrix[xi - 1][xj],
                          y=copy_img_matrix[yi - 1][yj])
        left_pp = PixelPair(xi=xi,
                            xj=xj - 2,
                            yi=yi,
                            yj=yj - 2,
                            x=copy_img_matrix[xi][xj - 2],
                            y=copy_img_matrix[yi][yj - 2])
        right_pp = PixelPair(xi=xi,
                             xj=xj + 2,
                             yi=yi,
                             yj=yj + 2,
                             x=copy_img_matrix[xi][xj + 2],
                             y=copy_img_matrix[yi][yj + 2])
        ld_pp = PixelPair(xi=xi + 1,
                          xj=xj - 2,
                          yi=yi + 1,
                          yj=yj - 2,
                          x=copy_img_matrix[xi + 1][xj - 2],
                          y=copy_img_matrix[yi + 1][yj - 2])
        down_pp = PixelPair(xi=xi + 1,
                            xj=xj,
                            yi=yi + 1,
                            yj=yj,
                            x=copy_img_matrix[xi + 1][xj],
                            y=copy_img_matrix[yi + 1][yj])
        rd_pp = PixelPair(xi=xi + 1,
                          xj=xj + 2,
                          yi=yi + 1,
                          yj=yj + 2,
                          x=copy_img_matrix[xi + 1][xj + 2],
                          y=copy_img_matrix[yi + 1][yj + 2])
        bottom_pp_1 = PixelPair(xi=xi + 2,
                                xj=xj - 2,
                                yi=yi + 2,
                                yj=yj - 2,
                                x=copy_img_matrix[xi + 2][xj - 2],
                                y=copy_img_matrix[yi + 2][yj - 2])
        bottom_pp_2 = PixelPair(xi=xi + 2,
                                xj=xj,
                                yi=yi + 2,
                                yj=yj,
                                x=copy_img_matrix[xi + 2][xj],
                                y=copy_img_matrix[yi + 2][yj])
        bottom_pp_3 = PixelPair(xi=xi + 2,
                                xj=xj + 2,
                                yi=yi + 2,
                                yj=yj + 2,
                                x=copy_img_matrix[xi + 2][xj + 2],
                                y=copy_img_matrix[yi + 2][yj + 2])
        lc = pp.compute_LC(up_pp,
                           left_pp,
                           right_pp,
                           ld_pp,
                           down_pp,
                           rd_pp,
                           bottom_pp_1,
                           bottom_pp_2,
                           bottom_pp_3)
        recover_blank_LC_list.append(lc)
        temp_result = recover.recover(pp,
                                      lc,
                                      recover_blank_threshold_list,
                                      recover_blank_z_list,
                                      copy_img_matrix)
        if len(temp_result) > 0:
            data_index += 1
            result_secret_data += temp_result
        if data_index >= recover_data_len // 2:
            break

    print("recover_blank_lc_list:", list(reversed(recover_blank_LC_list)))
    print("len", len(recover_blank_LC_list))
    print("recover_shadow_lc_list:", list(reversed(recover_shadow_LC_list)))
    print("len", len(recover_shadow_LC_list))

    recover_secret_data = "".join(list(reversed(result_secret_data)))
    print(len(recover_secret_data))

    print("图像恢复成功：", recover_secret_data == data)

    Image.fromarray(copy_img_matrix).save("lenna_recovered.bmp")
    # for row in range(len(copy_img_matrix)):
    #     for col in range(len(copy_img_matrix)):
    #         if copy_img_matrix[row][col]  != img_matrix[row][col]:
    #             print((row, col))


if __name__ == "__main__":
    # 一些错误会发生, 由于一层隐藏时容量不够
    data = "1011101011"
    tmp_list = []
    for i in range(500):
        item = random.randint(0, 1)
        tmp_list.append(str(item))

    # 初始化相应参数  作为测试. 将数值硬编码于code, 后期通过argv传递
    parameter.m = 3

    data_len_list = []
    psnr_list = []
    for i in range(1000):
        try:
            random.shuffle(tmp_list)
            data = data + "".join(tmp_list)
            parameter.P = len(data)  # 待隐藏的数据位数

            main()
            datalen = len(data)
            data_len_list.append(datalen)
            psnr_list.append(list(get_psnr()))
            print("# ==============================")
            print("data len:", datalen)
            print("# ==============================")
            # 重新初始化：
            AuxiliaryInformation.k1 = -1
            AuxiliaryInformation.k2 = -1
            image_data.times = 1
        except:
            print("max data len:", datalen - 500)
            break
    plot_psnr_by_databits(data_len_list, psnr_list)


