# fits_object_detector.py
import cv2
import numpy as np
import sep

from .fits_image import FITSImage
from .functions.manageSources import cleanCatalogSourcesFast

class FITSObjectDetector:
    def detect_objects(self, image: FITSImage, is_sub=False, other: FITSImage=None, is_dip=False):
        """
        Detect objects in the image using SEP source extraction.

        Parameters:
        image (FITSImage): An instance of FITSImage containing the image data.
        is_sub (bool): Whether the image is subtracted (default: False).
        is_dip (bool): Whether the image is preprocessed (default: False).

        Returns:
        list: A list of objects detected in the image.
        """
        data = image.data_relatif

        # Subtract background and take absolute values
        if is_sub:
            if other is None:
                raise ValueError("Subtracted and old image are required for object detection of a subtraction.")
            else:
                bg = sep.Background(np.abs(image.imgsub[other]))
                data_sub = np.abs(image.imgsub[other]) - bg
        else:
            bg = sep.Background(data)
            data_sub = np.abs(data - bg)

        # Digital Image Processing (DIP) if required
        if is_dip:
            # Threshold and morphological operations
            data_sub = cv2.threshold(data_sub.astype('uint8'), 0.2, 255, cv2.THRESH_BINARY)[1]
            data_sub = cv2.morphologyEx(data_sub, cv2.MORPH_CLOSE, np.ones((5, 5), np.uint8))

        # Extract objects using SEP
        threshold_objects = 5
        objects = sep.extract(data_sub, threshold_objects, err=bg.globalrms)
        if not is_dip:
            objects = cleanCatalogSourcesFast(objects)

        return objects

    def detect_objects_auto(self, image: FITSImage, is_sub=False,other:FITSImage=None, is_dip=False, threshold_objects=10):
        """
        Detect objects in the image using SEP source extraction with adaptive thresholding.

        Parameters:
        image (FITSImage): An instance of FITSImage containing the image data.
        is_sub (bool): Whether the image is subtracted (default: False).
        is_dip (bool): Whether the image is preprocessed (default: False).
        threshold_objects (int): Threshold for object detection (default: 10).

        Returns:
        list: A list of objects detected in the image.
        """
        data = image.data_relatif

        # Subtract background and take absolute values
        if is_sub:
            if other is None:
                raise ValueError("Subtracted and old image are required for object detection of a subtraction.")
            else:
                bg = sep.Background(np.abs(image.imgsub[other]))
                data_sub = np.abs(image.imgsub[other]) - bg
        else:
            bg = sep.Background(data)
            data_sub = np.abs(data - bg)

        # Digital Image Processing (DIP) if required
        if is_dip:
            # Adaptive thresholding
            data_sub = cv2.adaptiveThreshold(data_sub.astype('uint8'), 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                             cv2.THRESH_BINARY, 11, 2)

            # Additional morphological operations
            data_sub = cv2.morphologyEx(data_sub, cv2.MORPH_CLOSE, np.ones((5, 5), np.uint8))

        # Extract objects using SEP
        objects = sep.extract(data_sub, threshold_objects, err=bg.globalrms)

        # Filter contours based on area and circularity
        filtered_objects = []
        for obj in objects:
            contour = np.array(obj['npix'])
            area = cv2.contourArea(contour)
            perimeter = cv2.arcLength(contour, True)
            circularity = 4 * np.pi * area / (perimeter * perimeter)

            # Only include objects with reasonable area and circularity
            if 100 < area < 1000 and circularity > 0.5:
                filtered_objects.append(obj)

        return objects

    def patch_catalog(self, image: FITSImage, objects, patch_size=50, save_png=False, save_path=""):
        """
        Extract patches around detected objects in the image.

        Parameters:
        image (FITSImage): An instance of FITSImage containing the image data.
        objects (list): A list of objects detected in the image. Use detect_objects() to get this list.
        patch_size (int): Size of the patch around each object (default: 50).

        Returns:
        list: A list of patches extracted around the detected objects.
        """
        patches = []

        for obj in objects:
            x, y = obj['x'], obj['y']
            patch = image.data_relatif[y - patch_size:y + patch_size, x - patch_size:x + patch_size]
            patches.append(patch)


        i=0
        for patch in patches:
            i+=1
            if save_png:
                cv2.imwrite(save_path+f'patch{i}.png', patch)

        return patches