# fits_image_plotter.py
import cmastro
import numpy as np
from astropy.wcs import WCS
from matplotlib import pyplot as plt
from matplotlib.patches import Ellipse

from .fits_image_stats import FITSImageStats
from .fits_image import FITSImage
from .fits_image_processor import FITSImageProcessor
from .fits_object_detector import FITSObjectDetector
class FITSImagePlotter:
    def plot_self(self, image: FITSImage):
        # Implementation for plotting the FITS image
        """
                Plot the FITS image with axes in arcminutes.

                Parameters:
                image (FITSImage): An instance of FITSImage containing the image data.
                """
        wcs = WCS(image.header)
        name = image.path.split("\\")[-1]

        fig, ax = plt.subplots(subplot_kw={'projection': wcs})
        im=ax.imshow(image.data_relatif, cmap='viridis', vmin=image.m - 3 * image.s, vmax=image.m + 3 * image.s,
                  origin='lower')

        ax.set_xlabel('Right Ascension (Arcmin)')
        ax.set_ylabel('Declination (Arcmin)')
        ax.set_title('FITS Image: ' + name)

        ax.grid(color='white', ls='dotted', lw=0.5)

        fig.colorbar(im,label='Intensity', ax=ax)

        plt.show(block=False)

    def plot_diff(self, image: FITSImage, other: FITSImage):
        # Implementation for plotting differences between FITS images
        """
                Plot the differences between two FITS images with axes in arcminutes.

                Parameters:
                image (FITSImage): An instance of FITSImage containing the original image data.
                other (FITSImage): An instance of FITSImage containing the image data from another epoch.
                """
        wcs = WCS(image.header)


        image_substration = image.imgsub[other]
        if image_substration is None:
            image_substraction = FITSImageProcessor().subtract(image, other)





        # Compute statistics for the difference image
        m1, s1 = np.nanmean(image_substration), np.nanstd(image_substration)

        # Create subplots
        fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(12, 4), subplot_kw={'projection': wcs}, sharex=True,
                                            sharey=True)

        print("are images the same size?", image.border_image[other].shape == other.aligned_image[image].shape)
        # Plot the original image
        ori = ax1.imshow(image.border_image[other], cmap='viridis', vmin=image.m - image.s, vmax=image.m + image.s,
                         origin='lower')
        ax1.set_xlabel('Right Ascension (Arcmin)')
        ax1.set_ylabel('Declination (Arcmin)')
        ax1.set_title('Original Image')
        fig.colorbar(ori, ax=ax1)

        # Plot the image from another epoch
        line1 = ax2.imshow(other.aligned_image[image], cmap='viridis', vmin=image.m - image.s, vmax=image.m + image.s,
                           origin='lower')
        ax2.set_xlabel('Right Ascension (Arcmin)')
        ax2.set_title('Image from Other Epoch')
        fig.colorbar(line1, ax=ax2)

        # Plot the subtraction of the two images
        im = ax3.imshow(image_substration, cmap='RdBu', vmin=m1 - 2 * s1, vmax=m1 + 2 * s1, origin='lower')
        ax3.set_xlabel('Right Ascension (Arcmin)')
        ax3.set_title('Subtraction of the Two Images')
        cbar2 = fig.colorbar(im, ax=ax3)

        plt.tight_layout()
        plt.show(block=False)

    def plot_stats(self, image: FITSImage):
        """
        Plot the statistics of the FITS image with axes in arcminutes.

        Parameters:
        image (FITSImage): An instance of FITSImage containing the image data.
        """
        wcs = WCS(image.header)

        # Compute statistics of the image
        bg_img, bkg_rms = FITSImageStats.stats(image)

        # Create subplots
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5), subplot_kw={'projection': wcs})

        # Plot the background image
        img1 = ax1.imshow(bg_img, cmap='gray', origin='lower')
        ax1.set_xlabel('Right Ascension (Arcmin)')
        ax1.set_ylabel('Declination (Arcmin)')
        ax1.set_title('Background')
        fig.colorbar(img1, ax=ax1)

        # Plot the background noise image
        img2 = ax2.imshow(bkg_rms, cmap='gray', origin='lower')
        ax2.set_xlabel('Right Ascension (Arcmin)')
        ax2.set_title('Background Noise')
        fig.colorbar(img2, ax=ax2)

        plt.tight_layout()
        plt.show(block=False)

    def plot_objects(self, image: FITSImage,is_sub=True,other:FITSImage=None, isDIP=False):
        # Implementation for plotting detected objects in the FITS image
        """
                Plot the detected objects in the FITS image with axes in arcminutes.

                Parameters:
                image (FITSImage): An instance of FITSImage containing the image data.
                isDIP (bool, optional): Indicates if the image has been preprocessed with Digital Image Processing.
                is_sub (bool, optional): Indicates if the image subtraction is available.
                """
        wcs = WCS(image.header)

        # Detect objects in the image
        if is_sub:
            if other is None:
                raise ValueError("Subtracted and old image are required for object detection of a subtraction.")
            else:
                objects = FITSObjectDetector().detect_objects(image,is_sub=True,other=other, is_dip=isDIP)
                img = image.data_relatif[other]
        else:
            objects = FITSObjectDetector().detect_objects(image,is_sub=False, is_dip=isDIP)
            img = image.data_relatif

        # Create subplots
        if is_sub:
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5), subplot_kw={'projection': wcs}, sharex=True,
                                           sharey=True)
        else:
            fig, ax1 = plt.subplots(subplot_kw={'projection': wcs})

        # Plot the original image or subtraction image
        img_plot = ax1.imshow(img, cmap='gray', vmin=np.nanmean(img)-2*np.nanstd(img),vmax=np.nanmean(img)+2*np.nanstd(img), origin='lower')
        ax1.set_xlabel('Right Ascension (Arcmin)')
        ax1.set_ylabel('Declination (Arcmin)')
        ax1.set_title('Original Image' if not is_sub else 'Image Subtraction')
        fig.colorbar(img_plot, ax=ax1)

        if not is_sub:
            # Plot ellipses on the original or subtraction image
            for obj in objects:
                e = Ellipse(xy=(obj['x'], obj['y']),
                            width=6 * obj['a'],
                            height=6 * obj['b'],
                            angle=obj['theta'] * 180. / np.pi,
                            edgecolor='red',
                            facecolor='none')
                ax1.add_artist(e)

        if is_sub:
            ax2.imshow(image.imgsub[other], cmap='gray', vmin=np.nanmean(img)-2*np.nanstd(img),vmax=np.nanmean(img)+2*np.nanstd(img), origin='lower')
            # Plot ellipses on the subtraction image
            for obj in objects:
                e = Ellipse(xy=(obj['x'], obj['y']),
                            width=6 * obj['a'],
                            height=6 * obj['b'],
                            angle=obj['theta'] * 180. / np.pi,
                            edgecolor='red',
                            facecolor='none')
                ax2.add_artist(e)

            ax2.set_xlabel('Right Ascension (Arcmin)')
            ax2.set_title('Image Subtraction')
            fig.colorbar(img_plot, ax=ax2)

        plt.tight_layout()
        plt.show(block=False)

    def plot_histogram(self, image: FITSImage):
        # Implementation for plotting the histogram of the FITS image
        """
                Plot the histogram of pixel values in the FITS image.

                Parameters:
                image (FITSImage): An instance of FITSImage containing the image data.
                """
        plt.figure()
        plt.hist(image.data.flatten(), bins=1000, range=(-image.s, image.m + 5 * image.s), histtype='step')
        plt.yscale('log')
        plt.xlabel('Pixel Value')
        plt.ylabel('Frequency')
        plt.title('Histogram of Pixel Values (Absolute Image)')
        plt.show(block=False)