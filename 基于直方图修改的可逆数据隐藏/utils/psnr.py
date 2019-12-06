import numpy as np
from PIL import Image


def compute_psnr(img1, img2):
    img1 = np.array(img1)
    img2 = np.array(img2)
    mse = np.mean((img1 - img2)**2)
    if mse == 0:
        return 0.
    return 10 * np.math.log10(255. ** 2/mse)

def get_psnr():
    lenna = Image.open("../img/lenna.bmp", mode="r")
    lenna_with_data_single = Image.open("../first/lenna_with_data.bmp")
    lenna_recovered_single = Image.open("../first/lenna_recover.bmp")
    lenna_with_data_multiple = Image.open("../second/lenna_with_data.bmp")
    lenna_recovered_multiple = Image.open("../second/lenna_reverse.bmp")
    print(compute_psnr(lenna, lenna_with_data_single))
    print(compute_psnr(lenna, lenna_recovered_single))
    print(compute_psnr(lenna, lenna_with_data_multiple))
    print(compute_psnr(lenna, lenna_recovered_multiple))

get_psnr()