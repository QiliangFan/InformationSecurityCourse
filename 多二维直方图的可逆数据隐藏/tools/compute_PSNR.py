import numpy as np
from numpy import ndarray
from PIL import Image


def psnr(img1: ndarray, img2: ndarray):
    im1 = img1.astype(np.float64) / 255.
    im2 = img2.astype(np.float64) / 255.
    mse = np.mean((img1 - img2) ** 2)
    if mse == 0:
        return 0.0
    return 10 * np.math.log10(255. ** 2/ mse)


def get_psnr():
    img1 = Image.open("img/1.bmp", 'r')
    img2 = Image.open("lenna_with_data.bmp", 'r')
    img3 = Image.open("lenna_without_aux.bmp", 'r')
    img4 = Image.open("lenna_recovered.bmp", 'r')

    img1 = np.array(img1)  # original image
    img2 = np.array(img2)  # with data
    img3 = np.array(img3)  # without auxiliary
    img4 = np.array(img4)  # recovered

    return psnr(img1, img2), psnr(img1,img3), psnr(img1, img4)

