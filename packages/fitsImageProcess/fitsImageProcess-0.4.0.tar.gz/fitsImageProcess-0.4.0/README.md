

# FITS Image Toolkit (fits_image)

fits_image is a Python package designed for handling, processing, and analyzing FITS (Flexible Image Transport System) astronomical images. It provides various classes and functions for reading, writing, preprocessing, plotting, and analyzing FITS images.




## Deployment

To deploy this project run

```bash
  pip install fitsImageProcess
```

## Structure

Directory Structure

```bash
│
├── __init__.py               # Makes the directory a package
├── fitsImageProcess.py       # Contains the FITSImage class
├── fits_image_reader.py      # Contains the FITSImageReader class
├── fits_image_writer.py      # Contains the FITSImageWriter class
├── fits_image_processor.py   # Contains the FITSImageProcessor class
├── fits_image_plotter.py     # Contains the FITSImagePlotter class
├── fits_image_stats.py       # Contains the FITSImageStats class
├── fits_object_detector.py   # Contains the FITSObjectDetector class
└── fits_downloader.py        # Contains the FITSDownloader class
```

## Classes and Functions
### FITSImage
Description: Represents a FITS image.

Attributes:
- path: Path to the FITS image file.
- imgsub: Subtracted image data (if available).
- s: Standard deviation of pixel values.
- data: Raw image data.
- data_relatif: Relative image data.
- aligned_image: Aligned image data (if available).
- header: Header information of the FITS image.
- m: Mean pixel value.
### FITSImageReader
Description: Reads FITS images.
### FITSImageWriter
Description: Writes FITS images to files.
### FITSImageProcessor
Description: Preprocesses FITS images and finds differences between images.
### FITSImagePlotter
Description: Plots FITS images, differences, statistics, detected objects, and histograms.
### FITSImageStats
Description: Calculates statistics of FITS images.
### FITSObjectDetector
Description: Detects objects in FITS images.
### FITSDownloader
Description: Downloads FITS images from URLs.


## Usage
Here's how you can use fits_image in your Python scripts:


### 1. Importing

To import all the Functions:

```python
from fits_image import (
    FITSImage,
    FITSImageReader,
    FITSImageWriter,
    FITSImageProcessor,
    FITSImagePlotter,
    FITSImageStats,
    FITSObjectDetector,
    FITSDownloader
)
```


### 2. Loading and Plotting Images

To load a FITS image and plot it:

```python
from fits_image import FITSImage, FITSImagePlotter

# Load a FITS image
image = FITSImage('path/to/image.fits')

# Plot the image
plotter = FITSImagePlotter()
plotter.plot_self(image)
```

### 3. Image Subtraction and Object Detection
You can perform image subtraction between two FITS images and detect objects in the resulting image:

```python
# Load two FITS images for subtraction
other_image = FITSImage('path/to/other_image.fits')

# Subtract images (Needed before plotting)
image_diff = FITSImageProcessor.Subtract(image, other_image)

# Plot the difference and detected objects
plotter.plot_diff(image, other_image)
plotter.plot_objects(image)
```
### 4. Statistics Analysis and Histogram Plotting
Analyze the statistics of a FITS image and plot its histogram:

```python

# Plot statistics and histogram
plotter.plot_stats(image)
plotter.plot_histogram(image)

```
### 5. Preprocessing Images
Preprocess FITS images by applying background subtraction and digital image processing techniques:

```python
from fits_image import FITSImageProcessor

# Preprocess the image
processor = FITSImageProcessor()
processor.preprocess(image)
```
### 6. Writing Images to Files
Save a FITS image to a file:

```python
from fits_image import FITSImageWriter

# Write the image to a file
writer = FITSImageWriter()
writer.write(image, 'output.fits')
```
### 7. Downloading Images
Download FITS images from URLs:

```python
from fits_image import FITSDownloader

# Download the image
downloader = FITSDownloader()
downloader.download('http://example.com/image.fits', 'downloaded_images/')

```
## License
This project is licensed under the GNU License, see
[GPLv3](https://choosealicense.com/licenses/gpl-3.0/#).

