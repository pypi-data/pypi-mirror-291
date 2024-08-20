import cv2
import matplotlib.pyplot as plt
import numpy as np
from numba import jit



def calculate_offset(image1, image2,plotbool=False):
    """
    Calculate the offset between an image and a patch.

    Parameters:
    image1 (numpy.ndarray): Image data.
    image2 (numpy.ndarray): Patch data.
    plotbool (bool): Whether to plot the matched region (default: False).

    Returns:
    tuple: Offset values (x, y).
    """



    # Apply median blur for noise reduction
    image1_blurred = cv2.medianBlur(image1.astype(np.uint8), 7)
    image2_blurred = cv2.medianBlur(image2.astype(np.uint8), 7)

    image1_blurred = image1_blurred.astype(np.float32)
    image2_blurred = image2_blurred.astype(np.float32)

    # # Put nan where the image is zero
    # image1_blurred[image1_blurred == 0] = np.nan
    # image2_blurred[image2_blurred == 0] = np.nan

    # Calculate normalized cross-correlation between the images
    corr = cv2.matchTemplate(image1_blurred, image2_blurred, cv2.TM_CCOEFF_NORMED)

    # Find coordinates of the maximum correlation
    y, x = np.unravel_index(np.argmax(corr), corr.shape)

    # Plot if plotbool is True
    if plotbool:
        plt.figure()
        plt.subplot(1, 2, 1)
        plt.imshow(image1, cmap='gray', vmin=np.nanmean(image1) - 2 * np.nanstd(image1), vmax=np.nanmean(image1) + 2 * np.nanstd(image1))
        plt.plot(x, y, 'rx')
        plt.plot(x + image2.shape[1], y + image2.shape[0], 'rx')
        plt.plot(x + image2.shape[1], y, 'rx')
        plt.plot(x, y + image2.shape[0], 'rx')
        plt.subplot(1, 2, 2)
        plt.imshow(image2, cmap='gray', vmin=np.nanmean(image1) - 2 * np.nanstd(image1), vmax=np.nanmean(image1) + 2 * np.nanstd(image1))
        plt.show()

    # print('Offset x:', x)
    # print('Offset y:', y)

    return x, y


def is_included(wcs1, wcs2, data1, data2, precision=10):
    """
    Check if the WCS of two images include each other.

    Parameters:
    wcs1 (astropy.wcs.WCS): WCS information of the first image.
    wcs2 (astropy.wcs.WCS): WCS information of the second image.
    data1 (numpy.ndarray): Data of the first image.
    data2 (numpy.ndarray): Data of the second image.
    precision (int): Precision factor for checking if one image includes the other (default: 10).

    Returns:
    bool: True if the WCS of one image includes the other, False otherwise.
    """
    # Extract celestial coordinates of the corners of both images
    corners1 = np.array([
        wcs1.all_pix2world(0, 0, 0),
        wcs1.all_pix2world(data1.shape[1], 0, 0),
        wcs1.all_pix2world(0, data1.shape[0], 0),
        wcs1.all_pix2world(data1.shape[1], data1.shape[0], 0)
    ])

    corners2 = np.array([
        wcs2.all_pix2world(0, 0, 0),
        wcs2.all_pix2world(data2.shape[1], 0, 0),
        wcs2.all_pix2world(0, data2.shape[0], 0),
        wcs2.all_pix2world(data2.shape[1], data2.shape[0], 0)
    ])


    def is_corners_included(corners, ra1, dec1, ra12, dec12):
        ra_min, ra_max = min(ra1, ra12), max(ra1, ra12)
        dec_min, dec_max = min(dec1, dec12), max(dec1, dec12)
        corner_bool = all(ra_min <= ra <= ra_max and dec_min <= dec <= dec_max for ra, dec in corners)
        return corner_bool

    ra1, dec1, ra12, dec12 = corners1[:, 0].min(), corners1[:, 1].min(), corners1[:, 0].max(), corners1[:, 1].max()
    ra2, dec2, ra22, dec22 = corners2[:, 0].min(), corners2[:, 1].min(), corners2[:, 0].max(), corners2[:, 1].max()

    # if is_corners_included(corners2, ra1, dec1, ra12, dec12):
    #     return True
    #
    # if is_corners_included(corners1, ra2, dec2, ra22, dec22):
    #     return True

    # Generate grid points for data2
    y_indices, x_indices = np.mgrid[0:data2.shape[0]:100, 0:data2.shape[1]:100]

    #keep the indices only if the pixel in data2 is not zero or nan
    y_indices, x_indices = y_indices[data2[y_indices, x_indices] != 0], x_indices[data2[y_indices, x_indices] != 0]



    grid_points = np.vstack([x_indices.ravel(), y_indices.ravel()]).T
    grid_celestial_coords = np.array(wcs2.all_pix2world(grid_points[:, 0], grid_points[:, 1], 0)).T
    count_included = np.sum(
        (ra1 <= grid_celestial_coords[:,0]) & (grid_celestial_coords[:,0] <= ra12) &
        (dec1 <= grid_celestial_coords[:,1]) & (grid_celestial_coords[:,1] <= dec12)
    )
    return count_included > (grid_points.shape[0] * precision / 100)

def find_best_common_pixel(wcs1, wcs2, data1, data2):
    """
    Find the best common point between two images based on where their WCS overlap.

    Parameters:
    wcs1 (astropy.wcs.WCS): WCS information of the first image.
    wcs2 (astropy.wcs.WCS): WCS information of the second image.
    data1 (numpy.ndarray): Data of the first image.
    data2 (numpy.ndarray): Data of the second image.

    Returns:
    tuple: Coordinates of the best common point.
    """
    # Find the pixel where the WCS of the two images overlap and return the pixel coordinates of the first one that has at least two or three common points in the same line
    # Extract celestial coordinates of the corners of both images
    corners1 = np.array([
        wcs1.all_pix2world(0, 0, 0),
        wcs1.all_pix2world(data1.shape[1], 0, 0),
        wcs1.all_pix2world(0, data1.shape[0], 0),
        wcs1.all_pix2world(data1.shape[1], data1.shape[0], 0)
    ])

    corners2 = np.array([
        wcs2.all_pix2world(0, 0, 0),
        wcs2.all_pix2world(data2.shape[1], 0, 0),
        wcs2.all_pix2world(0, data2.shape[0], 0),
        wcs2.all_pix2world(data2.shape[1], data2.shape[0], 0)
    ])
    ra1, dec1, ra12, dec12 = corners1[:, 0].min(), corners1[:, 1].min(), corners1[:, 0].max(), corners1[:, 1].max()
    ra2, dec2, ra22, dec22 = corners2[:, 0].min(), corners2[:, 1].min(), corners2[:, 0].max(), corners2[:, 1].max()

    # Generate grid points for data2
    y_indices, x_indices = np.mgrid[0:data2.shape[0]:20, 0:data2.shape[1]:20]
    grid_points = np.vstack([x_indices.ravel(), y_indices.ravel()]).T
    grid_celestial_coords = np.array(wcs2.all_pix2world(grid_points[:, 0], grid_points[:, 1], 0)).T

    @jit(nopython=True)
    def overlap_grid_search(ra1, dec1, ra12, dec12, ra2, dec2, ra22, dec22, grid_points, grid_celestial_coords):
        # Find all the points that are in an overlapping region
        common_points = []
        for i in range(grid_points.shape[0]):
            if ra1 <= grid_celestial_coords[i][0] <= ra12 and dec1 <= grid_celestial_coords[i][1] <= dec12:
                common_points.append(grid_points[i])


        # print min of the common points for x and y axes

        minix,miniy = 1000000,1000000
        for i in range (len(common_points)):
            if common_points[i][0]<minix:
                minix = common_points[i][0]
            if common_points[i][1]<miniy:
                miniy = common_points[i][1]
        print("min of the common points for x and y axes are:", minix, miniy)



        # Find the first point as in near to top left corner as possible that has at least 2 or 3 common points in the same line
        for i in range(len(common_points)):
            for j in range(i+1, len(common_points)):
                    if common_points[i][0] == common_points[j][0]:
                        return common_points[i]

        print("No 3 common point found in a line, increase the precision")
        return common_points[0]


    return overlap_grid_search(min(ra1,ra12), min(dec1,dec12), max(ra1,ra12), max(dec1,dec12), ra2, dec2, ra22, dec22, grid_points, grid_celestial_coords)


if __name__ == "__main__":
    pass
    # Example usage of the functions
    # wcs1 = WCS(header1)
    # wcs2 = WCS(header2)
    # data1 = data1
    # data2 = data2
    # print(is_included(wcs1, wcs2, data1, data2))
    # print(find_best_common_pixel(wcs1, wcs2, data1, data2))