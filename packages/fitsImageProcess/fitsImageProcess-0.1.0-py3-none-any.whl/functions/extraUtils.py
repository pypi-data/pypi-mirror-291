from matplotlib import pyplot as plt
import numpy as np

def plotListImages(imagesList, titlesList=None):
    """
    Plot a list of images
    """
    nImages = len(imagesList)
    # if all images are the same size set sharex and sharey to True
    if all([image.shape == imagesList[0].shape for image in imagesList]):
        fig, axs = plt.subplots(1,nImages, sharex=True, sharey=True)
    else:
        fig, axs = plt.subplots(1,nImages)
    fig.suptitle('List of JWST Images')
    for i in range(nImages):
        axi=axs[i].imshow(imagesList[i], cmap='viridis', origin='lower', vmin = np.mean(imagesList[0]) - np.std(imagesList[0]), vmax = np.mean(imagesList[0]) + np.std(imagesList[0]))
        fig.colorbar(axi, ax=axs[i])
        if titlesList is not None:
            axs[i].set_title(titlesList[i])
        else:
            axs[i].set_title(f'Image {i}')
        axs[i].axis('off')