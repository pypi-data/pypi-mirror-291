from collections import defaultdict

import cv2
import numpy as np
from astropy.nddata import NDData
from astropy.table import Table
from astropy.io import fits
from astropy.wcs import WCS
import astropy.units as u
from photutils.aperture import CircularAperture
from photutils.detection import DAOStarFinder
from photutils.psf import extract_stars
from skimage.transform import rescale,rotate
from astropy.coordinates import SkyCoord


def addsource(image, x, y, flux,rot_angle = 0, sigma=None, psf=None):
    """
    Add a source to an image.

    Parameters
    ----------
    image : numpy.ndarray
        Image to which the source will be added.
        Make a copy of the image before calling this function if you need to keep the original one.
    x : float
        X coordinate of the source.
    y : float
        Y coordinate of the source.
    flux : float
        Flux of the source. Use MJy/pixel for JWST NIRCam images. You can calculate the flux from the magnitude using the ABmagnitude_to_flux function.
    rot_angle : float
        Rotation angle of the PSF in degrees.
    sigma : float
        Standard deviation of the Gaussian PSF.
    psf : numpy.ndarray
        PSF to be used to add the source (usually a data array). If not provided, a Gaussian PSF will be created.

    Returns
    -------
    numpy.ndarray
        Image with the source added.
    """

    # Create a Gaussian PSF if not provided
    if sigma is not None:
        size = 2 * int(3 * sigma) + 1
        gauss = np.zeros((size, size))
        for i in range(size):
            for j in range(size):
                gauss[i, j] = np.exp(-((i - size // 2) ** 2 + (j - size // 2) ** 2) / (2 * sigma ** 2))

        if psf is None:
            psf = gauss
    else:
        if psf is None:
            raise ValueError("Either sigma or psf must be provided.")

    # Create a Gaussian PSF
    psf = psf / np.abs(np.sum(psf))
    psf = psf * flux
    # Rotate the PSF with skimage
    if rot_angle != 0:
        psf = rotate(psf,rot_angle,resize=True,mode='constant',cval=0,clip=True,preserve_range=True,order=1)


    # Add the source to the image
    image[y - psf.shape[0] // 2:y + psf.shape[0] // 2 , x - psf.shape[1] // 2:x + psf.shape[1] // 2 ] += psf[:psf.shape[0]//2 * 2, :psf.shape[1]//2 * 2]

    return image


# pixel unit : 10 nano Jansky
# 20 ish of magnitude

def mag2fluxWebbNano(mag):
    '''
    Convert magnitude to flux compatible with JWST
    ---------------------PARAMETERS---------------------
    :param mag: Magnitude level of star

    ---------------------RETURN-------------------------
    :return: flux in 10 nano Jansky
    '''
    return 10**(mag/(-2.5)) * 3631*10**8

def mag2fluxWebbStandard(mag):
    '''
    Convert magnitude to flux compatible with JWST
    ---------------------PARAMETERS---------------------
    :param mag: Magnitude level of star

    ---------------------RETURN-------------------------
    :return: flux in Jansky
    '''
    return mag2fluxWebbNano(mag) * 10**(-8)


def ABmagnitude_to_flux(magnitude, pixar_sr=2.29e-14):
    """
    Convert AB magnitude to flux in MJy/pixel for JWST NIRCam images.
    https://jwst-docs.stsci.edu/jwst-near-infrared-camera/nircam-performance/nircam-absolute-flux-calibration-and-zeropoints#gsc.tab=0

    Parameters:
    magnitude (float): The AB magnitude.
    pixar_sr (float): The pixel area in steradians (PIXAR_SR).

    Returns:
    float: The flux in MJy/pixel.
    """
    ZP_AB = -6.10 - 2.5 * np.log10(pixar_sr)
    flux = 10 ** ((ZP_AB - magnitude) / 2.5)
    return flux



def flux2mag(flux):
    '''
    Convert flux to magnitude compatible with JWST
    ---------------------PARAMETERS---------------------
    :param flux: flux in 10 nano Jansky

    ---------------------RETURN-------------------------
    :return: Magnitude level of star
    '''
    return -2.5*np.log10(flux/(3631*10**8))



def samplePixelResolution(header1,header2):
    '''
    Find the sampling transformation between two images
    ---------------------PARAMETERS---------------------
    :param header1: FITS header of the first image
    :param header2: FITS header of the second image (usually JWST PSF reference)

    ---------------------RETURN-------------------------
    :return: scale factor to apply to the second image to match the first image
    '''
    # Find the pixel resolution of the first image
    try:
        try: # Try to find the pixel area in the header of the first image
            pixar1 = header1['PIXAR_A2'] # in arcsec2/pixel
        except KeyError:
            try:
                pixar1 = header1['PIXELSCL'] # in arcsec/pixel
                pixar1 = pixar1**2
            except KeyError:
                pixar1 = header1['PIXAR_SR'] # in steradian/pixel
                pixar1 = pixar1 * 4.25*10**10 # in arcsec2/pixel


        try: # Try to find the pixel area in the header of the second image
            pixar2 = header2['PIXAR_A2']
        except KeyError:
            try:
                pixar2 = header2['PIXAR_SR']
                pixar2 = pixar2 * 4.25*10**10
            except KeyError:
                pixar2 = header2['PIXELSCL'] # in arcsec/pixel
                pixar2 = pixar2**2
    except KeyError:
        print('No pixel area information in the header or need to change the key name')
        return 0


    return np.sqrt(pixar1/pixar2)


def scalePSF(psf,scale):
    '''
    Scale the PSF to match the pixel resolution of the image
    ---------------------PARAMETERS---------------------
    :param psf: PSF to scale
    :param scale: scale factor to apply to the PSF. Scale > 1 means the PSF will be downsampled and Scale < 1 means the PSF will be upsampled
                  - 1/scale,is used in this function to rescale the PSF

    ---------------------RETURN-------------------------
    :return: scaled PSF
    '''

    resampled_psf = rescale(psf,1/scale,anti_aliasing=True)


    return resampled_psf


def cleanCatalogSources(sources):
    '''
    Clean the sources of big stars
    :param sources:
    :return:
    '''
    # If more than 5 sources can be found in the same area (roughly 100 pixels), keep the biggest ellipse and remove others in the area

    sources_to_remove = []
    for i in range(len(sources)):
        nearby_sources = 0
        nearby_sources_indices = []
        for j in range(0, len(sources)):
            if (sources[i]['x'] - sources[j]['x']) ** 2 + (sources[i]['y'] - sources[j]['y']) ** 2 <= 100 ** 2:
                if i != j:
                    nearby_sources += 1
                    nearby_sources_indices.append(j)
        if nearby_sources > 5:
            nearby_sources_indices.append(i)
            areas = [sources[k]['a'] * sources[k]['b'] for k in nearby_sources_indices]
            max_area_index = nearby_sources_indices[np.argmax(areas)]
            sources_to_remove.extend([k for k in nearby_sources_indices if k != max_area_index])


    sources = [source for i, source in enumerate(sources) if i not in sources_to_remove]

    return sources


def cleanCatalogSourcesFast(sources):
    """
    Clean the sources of big stars by keeping only the largest ellipse if more than 5 sources are found
    within the same area (roughly 100 pixels).

    :param sources: List of source dictionaries with 'x', 'y', 'a', and 'b' keys.
    :return: Filtered list of sources.
    """

    grid_size = 100
    grids = defaultdict(list)

    # Assign each source to a grid cell
    for index, source in enumerate(sources):
        grid_x = source['x'] // grid_size
        grid_y = source['y'] // grid_size
        grids[(grid_x, grid_y)].append((index, source))

    sources_to_remove = set()

    for cell, cell_sources in grids.items():
        # Check neighboring cells within 1 cell distance
        for dx in range(-1, 2):
            for dy in range(-1, 2):
                neighbor_cell = (cell[0] + dx, cell[1] + dy)
                if neighbor_cell in grids:
                    combined_sources = cell_sources + grids[neighbor_cell]

                    # Check for sources within 100 pixels distance in the combined sources
                    for i in range(len(combined_sources)):
                        idx_i, source_i = combined_sources[i]
                        nearby_sources = []
                        for j in range(i + 1, len(combined_sources)):
                            idx_j, source_j = combined_sources[j]
                            if (source_i['x'] - source_j['x']) ** 2 + (source_i['y'] - source_j['y']) ** 2 <= 100 ** 2:
                                nearby_sources.append((idx_j, source_j))

                        if len(nearby_sources) >= 5:
                            nearby_sources.append((idx_i, source_i))
                            areas = [s['a'] * s['b'] for _, s in nearby_sources]
                            max_area_index = nearby_sources[np.argmax(areas)][0]
                            sources_to_remove.update(idx for idx, _ in nearby_sources if idx != max_area_index)

    sources = [source for i, source in enumerate(sources) if i not in sources_to_remove]

    return sources

def offsetCatalogSources(sources, offset_x, offset_y):
    """
    Offset the positions of sources in a catalog by a given amount.

    :param sources: List of source dictionaries with 'x' and 'y' keys.
    :param offset_x: Offset in the x-direction.
    :param offset_y: Offset in the y-direction.
    :return: Offset list of sources.
    """

    for source in sources:
        source['x'] += offset_x
        source['y'] += offset_y

    return sources

def get_rotation_angle(header):
    try:
        pc11 = header['PC1_1']
        pc12 = header['PC1_2']
    except KeyError:
        try:
            pc11 = header['PC2_1']
            pc12 = header['PC2_2']
        except KeyError:
            print("The necessary keywords are not present in the FITS header.")
            return None

    # Calculate the rotation angle
    rotation_angle = np.arctan2(pc12, pc11)

    # Convert to degrees
    rotation_angle = np.degrees(rotation_angle)

    return rotation_angle

def estimate_rotation(psf):
    # Calculate the second moment matrix (inertia tensor)
    moments = np.array([[np.sum(psf * np.arange(psf.shape[1])[:, np.newaxis] ** 2),
                         np.sum(psf * np.arange(psf.shape[1])[:, np.newaxis] * np.arange(psf.shape[1])[np.newaxis, :])],
                        [np.sum(psf * np.arange(psf.shape[0])[np.newaxis, :] ** 2),
                         np.sum(psf * np.outer(np.arange(psf.shape[0]), np.arange(psf.shape[1])))]])

    # Use eigenvectors of the moment matrix to find rotation angle
    _, eigenvectors = np.linalg.eigh(moments)
    rotation_angle = np.degrees(np.arctan2(eigenvectors[1, 0], eigenvectors[0, 0]))

    return rotation_angle


def get_rotation_angle_visually(image):
    """
    Get the rotation angle by aligning PSF with the star in the image and photutils.
    :param image: hdu.data of the image
    :return: rotation angle
    """

    # Detect stars in the image
    mean, median, std = np.mean(image), np.median(image), np.std(image)
    daofind = DAOStarFinder(fwhm=3.0, threshold=50. * std)
    sources = daofind(image - median)

    # Extract star positions
    positions = np.transpose((sources['xcentroid'], sources['ycentroid']))
    apertures = CircularAperture(positions, r=4.)

    table_sources = Table(positions, names=['x', 'y'])

    # Extract PSF of detected stars
    stars = extract_stars(NDData(image), table_sources, size=25)

    rotation_angles = []
    for i, star in enumerate(stars):
        rotation_angle = estimate_rotation(star.data)
        rotation_angles.append(rotation_angle)

    final_angle = np.median(rotation_angles)

    return final_angle



def addRandomSources(images : list, num_sources, flux_range, header=None, psf=None, sigma=None,rot_angle=0,save_list = False):
    """
    Add random sources to an image. With Psf and proper rotation if paramaters are provided, else Gaussian PSF is used.

    :param images: Image to which the sources will be added. It's a list of images of the same size.
    :param num_sources: Number of sources to add.
    :param flux_range: Tuple (min_flux, max_flux) for the flux range of the sources.
    :param header: FITS header containing the rotation angle information.
    :param psf: PSF to be used to add the sources.
    :param sigma: Standard deviation of the Gaussian PSF.
    :return: Image with the sources added.
    """
    # take copy of the images
    images = [image.copy() for image in images]

    if header is not None:
        rot_angle = get_rotation_angle(header)
        if rot_angle is None:
            rot_angle = 0

    # Verify that the images are of the same size
    for i in range(1, len(images)):
        if images[i].shape != images[i - 1].shape:
            raise ValueError("All images must be of the same size.")

    if psf is not None:
        xpsf = psf.shape[0]//2
        ypsf = psf.shape[1]//2
    else:
        xpsf = (2 * int(3 * sigma) + 1) // 2
        ypsf = (2 * int(3 * sigma) + 1) // 2

    save_positions = []
    for _ in range(num_sources):

        x = np.random.randint(xpsf, images[0].shape[1]-xpsf)
        y = np.random.randint(ypsf, images[0].shape[0]-ypsf)

        while any([image[y,x] == 0 for image in images]):
            x = np.random.randint(xpsf, images[0].shape[1]-xpsf)
            y = np.random.randint(ypsf, images[0].shape[0]-ypsf)

        flux = np.random.uniform(*flux_range)
        flux = ABmagnitude_to_flux(flux)
        for i,image in enumerate(images):
            save_positions.append((x,y))
            if np.random.rand() < 0.4:
                rot_angle = np.random.randint(-45,45)
            image = addsource(image, x, y, flux,rot_angle=rot_angle, sigma=sigma, psf=psf)
            images[i] = image

    if save_list:
        return images,save_positions
    return images,[]



def locate_galaxy(fits_file_data,fits_file_header, ra, dec, radius=100):

    """
    Locate a galaxy in a FITS image given its RA and Dec coordinates.

    Parameters:
    - fits_file: str, path to the FITS file.
    - ra: float, Right Ascension of the galaxy in degrees.
    - dec: float, Declination of the galaxy in degrees.
    - radius: int, radius of the region around the galaxy to extract in pixels (default is 10).

    Returns:
    - cutout_data: numpy array, cutout image data around the galaxy.
    - x: float, x coordinate of the galaxy in the image.
    - y: float, y coordinate of the galaxy in the image.
    """
    # Open the FITS file and extract WCS information

    wcs = WCS(fits_file_header)
    data = fits_file_data

    if wcs.footprint_contains(SkyCoord(ra,dec,unit='deg')):


        # Create a SkyCoord object for the galaxy's position
        galaxy_coord = SkyCoord(ra=ra * u.deg, dec=dec * u.deg, frame='icrs')

        # Convert the RA, Dec coordinates to pixel coordinates
        x, y = wcs.world_to_pixel(galaxy_coord)

        # Define the region to extract
        x = int(x)
        y = int(y)
        x_min = max(x - radius, 0)
        x_max = min(x + radius, data.shape[1] - 1)
        y_min = max(y - radius, 0)
        y_max = min(y + radius, data.shape[0] - 1)

        # Extract the cutout region
        cutout_data = data[y_min:y_max, x_min:x_max]
        # get the amount of exact zeros or nan in the cutout
        zeros = np.sum(cutout_data == 0)
        nans = np.sum(np.isnan(cutout_data))
        if zeros + nans > 0.5 * cutout_data.size:
            print("The cutout contains too many zeros or NaNs.")
            cutout_data = None
            x = None
            y = None
    else:
        print("The galaxy is outside the image.")
        cutout_data = None
        x = None
        y = None
    return cutout_data, x, y