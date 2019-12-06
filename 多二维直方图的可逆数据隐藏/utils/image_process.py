from PIL import Image
import numpy as np
from globaldata import image_data


def load_image_matrix(img: str) -> np.ndarray:
    img = Image.open(img)
    pixel_matrix = np.asarray(img)
    image_data.image_height = len(pixel_matrix)
    image_data.image_width = len(pixel_matrix[0])
    # print to test the with of image, and the height of image
    # print(image_width, image_height)
    return pixel_matrix


