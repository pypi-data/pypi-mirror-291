# fits_image_reader.py


from astropy.io import fits as pyfits
import numpy as np
import time

class FITSImageReader:
    def read(self, image,verbose=False):
        """
                Reads a FITS file, processes the data, and stores various attributes.

                Parameters:
                image (str): Path to the FITS image file.
                verbose (bool): Whether to print verbose output.
                """
        t1 = time.time()
        # Open the FITS file
        img = pyfits.open(image.path)
        t2 = time.time()
        # print("Time to open the file: ", t2 - t1)


        # Determine if the file path contains 'sub'
        boolsub = 'sub' in image.path

        # Initialize variables
        data = None
        header = None
        openbool = False

        # Attempt to read data and header from the first HDU
        try:
            data = img[0].data
            header = img[0].header
            if data is None:
                data = img[1].data
                header = img[1].header
                if verbose:
                    print("Data found in the second HDU")
            else:
                if verbose:
                    print("Data found in the first HDU")
            openbool = True
        except (IndexError, TypeError):
            print("No data in the first HDU")




        # If data wasn't found, attempt to read from the second HDU
        if not openbool:
            try:
                data = img[1].data
                header = img[1].header
                if verbose:
                    print("Data found in the second HDU")
            except IndexError:
                print("No data in the second HDU")

        t3 = time.time()
        # print("Time to read the data header: ", t3 - t2)


        # Process the data if the file path contains 'sub'
        if boolsub:
            try:
                data = data.byteswap().newbyteorder()
                data_relatif = data
                


            except FileNotFoundError:
                print("No mean and std values found")
        else:
            data_relatif = data

        # Ensure byte swapping and new byte order
        try:
            data = data.byteswap().newbyteorder()
            if verbose:
                print("Byte swap and new byte order applied")
        except AttributeError:
            print("No byte swap and new byte order needed")

        try:
            data_relatif = data_relatif.byteswap().newbyteorder()
            if verbose:
                print("Byte swap and new byte order applied for data_relatif")
        except AttributeError:
            print("No byte swap and new byte order needed for data_relatif")


        t4 = time.time()
        # print("Time to process the data: ", t4 - t3)
        # Calculate mean and standard deviation
        m, s = np.mean(data), np.std(data)

        # Store attributes
        image.data = data
        image.data_relatif = data_relatif
        image.m = m
        image.s = s
        image.header = header