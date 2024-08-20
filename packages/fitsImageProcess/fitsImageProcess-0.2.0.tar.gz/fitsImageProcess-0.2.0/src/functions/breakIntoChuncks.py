import matplotlib.pyplot as plt
import numpy as np
import astropy.io.fits as pyfits


def chunk_image(image, num_chunks):
    """
    Breaks an image into a grid of chunks.

    Parameters:
    image (numpy.ndarray): The image to break into chunks.
    num_chunks (int): The number of chunks to break the image into in each axis.

    Returns:
    list: A list of numpy.ndarrays representing the chunks of the image.
    """
    rows, cols = image.shape
    chunk_size_x = int(np.ceil(cols / num_chunks))
    chunk_size_y = int(np.ceil(rows / num_chunks))

    chunks = []
    for i in range(num_chunks):
        for j in range(num_chunks):
            chunk = image[i * chunk_size_y:(i + 1) * chunk_size_y, j * chunk_size_x:(j + 1) * chunk_size_x]
            chunks.append(chunk)

    return chunks
