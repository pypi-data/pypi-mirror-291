# fits_image_writer.py

from .fits_image import FITSImage
import astropy.io.fits as pyfits
class FITSImageWriter:
    def write(self, image: FITSImage, filename):
        # Write the FITS file
        hdu0 = pyfits.PrimaryHDU(image.data)
        hdul = pyfits.HDUList([hdu0])
        hdul.writeto(filename, overwrite=True)