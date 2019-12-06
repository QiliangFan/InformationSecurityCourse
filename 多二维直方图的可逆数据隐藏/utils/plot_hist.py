import matplotlib.pyplot as plt
from PIL import Image
import numpy as np

def plot(path, name):
    img = Image.open(path)
    img = np.array(img)
    plt.figure()
    plt.title(name)
    plt.xlabel("pixel value")
    plt.ylabel("the number of pixels")
    plt.hist(img.flatten(), bins=255)
    plt.show()

plot("../lenna_recovered.bmp", "lenna_recovered")
plot("../lenna_with_data.bmp", "lenna_with_data")
plot("../lenna_without_aux.bmp", "lenna_without_aux")
plot("../img/1.bmp", "lenna")
