import numpy as np
from matplotlib import pyplot as plt
from scipy.ndimage import rotate
import astropy.io.fits as pyfits
import os
import matplotlib.patches as patches

def create_binary_mask(image):
    return (image != 0).astype(int)


def calculate_bounding_box(binary_mask):
    rows = np.any(binary_mask, axis=1)
    cols = np.any(binary_mask, axis=0)
    rmin, rmax = np.where(rows)[0][[0, -1]]
    cmin, cmax = np.where(cols)[0][[0, -1]]
    return rmin, rmax, cmin, cmax


def is_rectangle_valid(binary_mask, rmin, rmax, cmin, cmax, tolerance=0.001):
    sub_mask = binary_mask[rmin:rmax, cmin:cmax]
    zero_fraction = np.sum(sub_mask == 0) / sub_mask.size
    return zero_fraction <= tolerance


def grow_rectangle(binary_mask, rmin, rmax, cmin, cmax, step=50):
    rows, cols = binary_mask.shape
    while True:
        new_rmin = max(0, rmin - step)
        new_rmax = min(rows, rmax + step)
        new_cmin = max(0, cmin - step)
        new_cmax = min(cols, cmax + step)

        if (new_rmin == rmin and new_rmax == rmax and new_cmin == cmin and new_cmax == cmax) or \
                not is_rectangle_valid(binary_mask, new_rmin, new_rmax, new_cmin, new_cmax):
            break

        rmin, rmax, cmin, cmax = new_rmin, new_rmax, new_cmin, new_cmax

    return rmin+step, rmax-step, cmin+step, cmax-step


def find_largest_rectangle(image, step=50):
    '''
    Find the largest rectangle fitting inside the non-zero region of the image.
    :param image:
    :param step:

    :return:xmin, xmax, ymin, ymax (top left and bottom right corners of the rectangle)
    '''
    binary_mask = create_binary_mask(image)
    rmin, rmax, cmin, cmax = calculate_bounding_box(binary_mask)

    # Start from the center of the bounding box
    center_r = (rmin + rmax) // 2
    center_c = (cmin + cmax) // 2

    initial_rmin = center_r
    initial_rmax = center_r
    initial_cmin = center_c
    initial_cmax = center_c

    # Grow the rectangle from the center
    rmin, rmax, cmin, cmax = grow_rectangle(binary_mask, initial_rmin, initial_rmax, initial_cmin, initial_cmax, step)

    return (rmin, rmax, cmin, cmax)


def plot_rectangle_on_image(image, rect):
    fig, ax = plt.subplots()
    ax.imshow(image, cmap='gray', vmin=np.mean(image) - np.std(image), vmax=np.mean(image) + np.std(image))

    rmin, rmax, cmin, cmax = rect
    width = cmax - cmin
    height = rmax - rmin

    # Create a Rectangle patch
    rect_patch = patches.Rectangle((cmin, rmin), width, height, edgecolor='red', linewidth=2, fill=False)
    ax.add_patch(rect_patch)
    # give name to the plot and axis
    fig.suptitle('Largest Rectangle in Image')
    ax.set_xlabel('X in pixels')
    ax.set_ylabel('Y in pixels')
    plt.show()


if __name__ == '__main__':
    # Example usage:
    cwd = os.getcwd()


    img = pyfits.open(os.path.join(cwd, 'downlaod', 'extra2', 'tile_sup.fits'))[1].data

    #add a border of zeros of size 100 around the image
    img = np.pad(img, 1000, mode='constant', constant_values=0)
    # do a 45-degree rotation and fill the corners with zeros
    img = rotate(img, 50, reshape=False, cval=0)


    # plt.imshow(img, cmap='viridis', vmin=np.mean(img)-np.std(img), vmax=np.mean(img)+np.std(img))
    # plt.colorbar()
    # plt.show()
    best_rect = find_largest_rectangle(img)
    print("Best Rectangle:", best_rect)


    plot_rectangle_on_image(img, best_rect)
