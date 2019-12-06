import matplotlib.pyplot as plt
from PIL import Image
import numpy as np


def plot_figure_hist(path, name):
    img = Image.open(path)
    img = np.array(img)
    plt.figure()
    plt.hist(img.flatten(), 255)
    plt.title(name)
    plt.xlabel("pixel value")
    plt.ylabel('the number of pixels')
    plt.show()

plot_figure_hist("../first/lenna_recover.bmp", "lenna_recovered")
plot_figure_hist("../first/lenna_with_data.bmp", "lenna_with_data")
