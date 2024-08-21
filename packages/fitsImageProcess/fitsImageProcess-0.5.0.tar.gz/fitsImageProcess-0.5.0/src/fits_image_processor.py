# fits_image_processor.py
import cv2
import numpy as np
import sep
from astropy.wcs import WCS
from reproject import reproject_interp
from scipy.ndimage import shift

from .fits_image import FITSImage
from .functions.functionsForAlignment import calculate_offset, is_included
from .functions.find_rectangle import find_largest_rectangle, plot_rectangle_on_image

class FITSImageProcessor:
    def preprocess(self, image: FITSImage):
        # Implementation for preprocessing FITS image
        """
                Preprocess the FITS image data by applying Gaussian blur, thresholding,
                and morphological operations to enhance features.

                Parameters:
                image (FITSImageReader): An instance of FITSImageReader containing the image data.
                """

        # Extract data for preprocessing
        datatopreprocess = image.data_relatif

        # Apply Gaussian blur to the data
        datafiltered = cv2.GaussianBlur(datatopreprocess, (5, 5), 0)

        # Calculate the threshold value using mean and background RMS
        background = sep.Background(datafiltered)
        threshold = np.mean(datafiltered) + 3 * background.globalrms
        print("Threshold value:", threshold)

        # Apply binary thresholding
        _, datathresholded = cv2.threshold(datafiltered.astype('uint8'), threshold, 255, cv2.THRESH_BINARY)

        # Apply morphological closing to fill small holes
        kernel_close = np.ones((3, 3), np.uint8)
        dataclosed = cv2.morphologyEx(datathresholded, cv2.MORPH_CLOSE, kernel_close)

        # Define vertical and horizontal erosion kernels
        kernel_vert = np.array([[0, 1, 0], [0, 1, 0], [0, 1, 0]], np.uint8)
        kernel_horiz = np.array([[0, 0, 0], [1, 1, 1], [0, 0, 0]], np.uint8)

        # Apply vertical and horizontal erosion
        data_erode_vert = cv2.erode(dataclosed, kernel_vert)
        data_erode_horiz = cv2.erode(dataclosed, kernel_horiz)

        # Combine eroded images using bitwise OR
        data_erode = cv2.bitwise_or(data_erode_vert, data_erode_horiz)

        return data_erode

    def subtract(self, image: FITSImage, other: FITSImage, border_size=200, offset_locate_data=0):
        # Implementation for finding differences between FITS images
        """
                Subtract another FITS image from this one after alignment.

                Parameters:
                other (FITSImageReader): Another instance of FITSImageReader to subtract from this one.
                border_size (int): Size of the border to add around the images for alignment.
                offset_locate_data (int): Offset for locating data in the images.

                Returns:
                numpy.ndarray: The subtracted image if successful, otherwise None.
                """

        # Check if the images have a matching area for subtraction
        if is_included(WCS(image.header), WCS(other.header), image.data_relatif, other.data_relatif):
            print("The two images have a matching area for subtraction.")
        else:
            print("The two images are not in the same spot; subtraction cannot be done.")
            return None

        # Prepare data for alignment
        data1 = image.data_relatif.astype(np.float32)
        data2 = other.data_relatif.astype(np.float32)

        # Calculate ideal border size based on the image size
        # print("abs diff x and y are:", abs(data1.shape[0] - data2.shape[0]), abs(data1.shape[1] - data2.shape[1]))

        # Reproject the other image onto the WCS of this image
        array_aligned, _ = reproject_interp((other.data_relatif, other.header), image.header, order='bicubic',
                                            parallel=False,
                                            roundtrip_coords=True)

        # Replace NaN values with 0
        array_aligned[np.isnan(array_aligned)] = 0

        # Integrate pictures with borders for alignment
        array_aligned_offset = np.zeros(
            (array_aligned.shape[0] + 2 * border_size, array_aligned.shape[1] + 2 * border_size))
        array_aligned_offset[border_size:-border_size, border_size:-border_size] = array_aligned
        img1_offset = np.zeros((data1.shape[0] + 2 * border_size, data1.shape[1] + 2 * border_size))
        img1_offset[border_size:-border_size, border_size:-border_size] = data1

        image.border_image[other] = img1_offset

        # Find a small part of the image where there is data to calculate the offset
        # indexes = np.where(array_aligned != 0)
        # minx1, miny1 = np.min(indexes[0]), np.min(indexes[1])
        # minx, miny = find_best_common_pixel(WCS(image.header), WCS(other.header), data1, data2)
        # print('min x and y are:', minx, miny, 'but minx1 and miny1 are:', minx1, miny1)
        # patch1 = array_aligned[minx + offset_locate_data:minx + min(2000, data2.shape[1]),
        #          miny + offset_locate_data:miny + min(2000, data2.shape[0])]


        patch1 = np.where(img1_offset==0, 0, array_aligned_offset)
        patch1 = np.where(np.isnan(img1_offset), 0, patch1)
        # Trouver les coordonnées du rectangle englobant
        x_min, x_max, y_min, y_max = find_largest_rectangle(patch1, step=50)
        plot_rectangle_on_image(patch1, (x_min, x_max, y_min, y_max))


        patch1 = patch1[y_min:y_max, x_min:x_max]

        # plt.figure()
        # plt.subplot(1, 3, 1)
        # plt.imshow(img1_offset, cmap='gray', vmin=np.nanmean(img1_offset) - 2 * np.nanstd(img1_offset),vmax=np.nanmean(img1_offset) + 2 * np.nanstd(img1_offset))
        # plt.title('img1_offset')
        # plt.subplot(1, 3, 2)
        # plt.imshow(array_aligned, cmap='gray', vmin=np.nanmean(array_aligned) - 2 * np.nanstd(array_aligned),
        #            vmax=np.nanmean(array_aligned) + 2 * np.nanstd(array_aligned))
        # plt.title('array_aligned')
        # plt.subplot(1, 2, 2)
        # plt.imshow(patch1, cmap='gray', vmin=np.nanmean(array_aligned) - 2 * np.nanstd(array_aligned),
        #            vmax=np.nanmean(array_aligned) + 2 * np.nanstd(array_aligned))
        # plt.title('patch1')
        # plt.show(block=True)

        # Calculate the offset between the images
        offset_x1, offset_y1 = calculate_offset(img1_offset, patch1, plotbool=False)

        print("delta offset x and y are:", offset_x1 - x_min, offset_y1-y_min)
        # Align images
        # aligned_image1 = shift(array_aligned_offset, (offset_y1 - (minx + 200 + 100), offset_x1 - (miny + 200 + 100)),
        #                        mode='constant', cval=np.nan, order=5, prefilter=False)
        aligned_image1 = shift(array_aligned_offset, (offset_y1-y_min, offset_x1-x_min),
                               mode='constant', cval=np.nan, order=5, prefilter=False)
        # aligned_image1 = shift(array_aligned_offset, (0,0),
        #                        mode='constant', cval=np.nan, order=5, prefilter=False)

        # Subtract images if aligned successfully
        if aligned_image1.shape == img1_offset.shape:
            imgsub = aligned_image1 - img1_offset
            other.aligned_image[image] = aligned_image1
            imgsub = np.where(np.abs(other.aligned_image[image]) <= 10**(-20), np.nan, imgsub)
            img1_offset[np.isnan(img1_offset)] = 0
            imgsub = np.where(np.abs(img1_offset) <= 10**(-20), np.nan, imgsub)
            image.border_image[other] = img1_offset
            image.imgsub[other] = imgsub
            return imgsub
        else:
            print("The images are not the same size; subtraction cannot be done.")
            return None