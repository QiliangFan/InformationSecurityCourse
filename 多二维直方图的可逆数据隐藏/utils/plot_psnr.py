import matplotlib.pyplot as plt
import numpy as np


def plot_psnr_by_databits(data_bits_list, psnrs_list):
    """
    image with data
    image without auxiliary
    image reocvered
    :param data_bits_list:
    :param psnrs_list:
    :return:
    """
    plt.figure()
    print(data_bits_list)
    print(psnrs_list)
    psnrs_list = np.array(psnrs_list)
    plt.plot(data_bits_list, psnrs_list[:,0], label="image_with_data")
    plt.plot(data_bits_list, psnrs_list[:,1], label="image_without_auxiliary")
    plt.plot(data_bits_list, psnrs_list[:,2], label="image_recovered")
    plt.legend()
    plt.xlabel('data')
    plt.ylabel('PSNR')
    plt.show()

