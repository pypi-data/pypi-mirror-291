# fits_image_stats.py
import numpy as np
import sep

from .fits_image import FITSImage

class FITSImageStats:
    def stats(self, image: FITSImage):
        # Implementation for calculating statistics of the FITS image
        bg = sep.Background(image.data)
        print("mean of the bg", bg.globalback)
        print("noise mean level", bg.globalrms)

        # Extract background image
        bg_img = np.array(bg)
        bkg_rms = bg.rms()
        return bg_img, bkg_rms