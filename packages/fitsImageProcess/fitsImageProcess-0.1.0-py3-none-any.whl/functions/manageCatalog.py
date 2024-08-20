from collections import defaultdict

import numpy as np
from matplotlib import pyplot as plt
from scipy.ndimage import rotate

def create_catalog(image, sources, save_path='catalog.csv'):
    """
    Create a catalog of sources with their properties.

    Parameters:
    image (numpy.ndarray): The image to create the catalog from.
    sources (list): A list of sources detected in the image.
    save_path (str): The path to save the catalog to (default: 'catalog.csv'). Set to None to not save.

    Returns:
    list: A list of dictionaries representing the sources in the catalog.
    """
    catalog = []
    for source in sources:
        catalog.append({
            'x': source['x'],
            'y': source['y'],
            'a': source['a'],  # semi-major axis
            'b': source['b'],  # semi-minor axis
            'flux': source['flux'],
            'original_image': image.path.split("\\")[-1],
        })

    if save_path is not None:
        # save as CSV line by line
        save_catalog(catalog, save_path)

    return catalog



def save_catalog(catalog, save_path):
    """
    Save the catalog to a CSV file.

    Parameters:
    catalog (list): A list of dictionaries representing the sources in the catalog.
    save_path (str): The path to save the catalog to.
    """
    with open(save_path, 'w') as f:
        f.write("x,y,a,b,flux,original_image_name\n")
        for source in catalog:
            f.write \
                (f"{source['x']},{source['y']},{source['a']},{source['b']},{source['flux']},{source['original_image']}\n")


def add_to_catalog(catalog, image, sources):
    """
    Add sources to an existing catalog.

    Parameters:
    catalog (list): A list of dictionaries representing the sources in the catalog.
    image (numpy.ndarray): The image to add the sources from.
    sources (list): A list of sources detected in the image.

    Returns:
    list: A list of dictionaries representing the updated catalog.
    """
    for source in sources:
        catalog.append({
            'x': source['x'],
            'y': source['y'],
            'a': source['a'],  # semi-major axis
            'b': source['b'],  # semi-minor axis
            'flux': source['flux'],
            'original_image': image.path.split("\\")[-1],
        })

    return catalog


def open_catalog(path):
    """
    Open an existing catalog.

    Parameters:
    path (str): The path to the catalog file.

    Returns:
    list: A list of dictionaries representing the sources in the catalog.
    """
    catalog = []
    with open(path, 'r') as f:
        f.readline()  # skip the header
        for line in f:
            x, y, a, b, flux, original_image = line.strip().split(',')
            catalog.append({
                'x': float(x),
                'y': float(y),
                'a': float(a),
                'b': float(b),
                'flux': float(flux),
                'original_image': original_image,
            })

    return catalog

def safe_catalog_merge(catalog1, catalog2,threshold_distance=10):
    """
    Merge two catalogs safely which means without duplicates.

    Parameters:
    catalog1 (list): A list of dictionaries representing the sources in the first catalog.
    catalog2 (list): A list of dictionaries representing the sources in the second catalog.
    threshold_distance (float): The maximum distance between two sources to consider them as the same source (default: 10).

    Returns:
    list: A list of dictionaries representing the merged catalog.
    """
    merged_catalog = []

    for source1 in catalog1:
        merged_catalog.append(source1)

    for source2 in catalog2:
        is_duplicate = False
        for source1 in catalog1:
            distance = np.sqrt((source1['x'] - source2['x'])**2 + (source1['y'] - source2['y'])**2)
            if distance < threshold_distance:
                is_duplicate = True
                break                                  
        if not is_duplicate:
            merged_catalog.append(source2)

    return merged_catalog


def safe_catalog_merge_fast(catalog1, catalog2, threshold_distance=10):
    """
    Merge two catalogs safely which means without duplicates.

    Parameters:
    catalog1 (list): A list of dictionaries representing the sources in the first catalog.
    catalog2 (list): A list of dictionaries representing the sources in the second catalog.
    threshold_distance (float): The maximum distance between two sources to consider them as the same source (default: 10).

    Returns:
    list: A list of dictionaries representing the merged catalog.
    """
    grid_size = threshold_distance
    grids = defaultdict(list)

    # Function to get grid coordinates
    def get_grid_coords(source):
        return (source['x'] // grid_size, source['y'] // grid_size)

    # Add all sources from catalog1 to the grid
    for source in catalog1:
        grid_coords = get_grid_coords(source)
        grids[grid_coords].append(source)

    merged_catalog = catalog1.copy()  # Start with catalog1 sources

    # Check each source in catalog2 for duplicates in the grid
    for source2 in catalog2:
        grid_coords = get_grid_coords(source2)
        is_duplicate = False

        # Check neighboring cells within threshold distance
        for dx in range(-1, 2):
            for dy in range(-1, 2):
                neighbor_coords = (grid_coords[0] + dx, grid_coords[1] + dy)
                if neighbor_coords in grids:
                    for source1 in grids[neighbor_coords]:
                        distance = np.sqrt((source1['x'] - source2['x']) ** 2 + (source1['y'] - source2['y']) ** 2)
                        if distance < threshold_distance:
                            is_duplicate = True
                            break
                if is_duplicate:
                    break
            if is_duplicate:
                break

        if not is_duplicate:
            merged_catalog.append(source2)
            grids[grid_coords].append(source2)  # Add to grid for future checks

    return merged_catalog


def pngCatalog(catalog, imageold, imagenew,imagediff,save_directory,name_tag='',cutout_size=7):
    """
    Create a PNG image for each source with a cutout from old, new, and diff images next to each other with a size of cutout_size.
    :param catalog:
    :param imageold: np.ndarray
    :param imagenew: np.ndarray
    :param imagediff: np.ndarray
    :param save_directory:
    :param cutout_size:
    :return:
    """

    mean_old, std_old = np.mean(imageold), np.std(imageold)

    for source in catalog:
        x, y = int(source['x']), int(source['y'])
        x,y = x + np.random.randint(-10,10) , y+np.random.randint(-10,10)

        cutout_old = imageold[y - cutout_size:y + cutout_size, x - cutout_size:x + cutout_size]
        cutout_new = imagenew[y - cutout_size:y + cutout_size, x - cutout_size:x + cutout_size]
        cutout_diff = imagediff[y - cutout_size:y + cutout_size, x - cutout_size:x + cutout_size]
        vertical_bar = np.zeros((2*cutout_size,3))

        # print(cutout_old.shape, cutout_new.shape, cutout_diff.shape)
        if cutout_old.shape != (2*cutout_size,2*cutout_size) or cutout_new.shape != (2*cutout_size,2*cutout_size) or cutout_diff.shape != (2*cutout_size,2*cutout_size):
            print('cutout_old.shape', cutout_old.shape)
            print('cutout_new.shape', cutout_new.shape)
            print('cutout_diff.shape', cutout_diff.shape)
            continue

        # Put Nan instead of 0
        vertical_bar[:] = np.nan

        merged_cutout = np.hstack((cutout_old,vertical_bar, cutout_new,vertical_bar, cutout_diff))
        plt.imshow(merged_cutout, cmap='viridis', vmin = mean_old -std_old, vmax = mean_old + std_old)
        plt.axis('off')
        plt.savefig(f"{save_directory}/{name_tag}source_{x}_{y}.png",bbox_inches='tight',pad_inches=0)
        plt.close()


    # Create a tutorial image called 0a.png which shows the template old image | new image | diff image

    tutorial_cutout_old = imageold[:cutout_size * 2, :cutout_size * 2]
    tutorial_cutout_new = imagenew[:cutout_size * 2, :cutout_size * 2]
    tutorial_cutout_diff = imagediff[:cutout_size * 2, :cutout_size * 2]
    vertical_bar = np.zeros((2 * cutout_size, 3))
    vertical_bar[:] = np.nan

    tutorial_merged_cutout = np.hstack(
        (tutorial_cutout_old, vertical_bar, tutorial_cutout_new, vertical_bar, tutorial_cutout_diff))

    plt.imshow(tutorial_merged_cutout, cmap='viridis', vmin=mean_old - 2 * std_old, vmax=mean_old + 2 * std_old)
    plt.text(cutout_size , cutout_size, 'Old', fontsize=12, color='red', ha='center')
    plt.text(2*cutout_size + cutout_size  + 3,  cutout_size, 'New', fontsize=12, color='red', ha='center')
    plt.text(4 * cutout_size + cutout_size  + 6, cutout_size, 'Subtraction', fontsize=12, color='red', ha='center')
    # plt.axvline(x=2*cutout_size, color='black', linewidth=3)
    # plt.axvline(x=4 * cutout_size + 3, color='black', linewidth=3)
    plt.axis('off')
    plt.savefig(f"{save_directory}/0a.png", bbox_inches='tight', pad_inches=0)
    plt.close()


def pngCatalogXY(save_list,imageold, imagenew,imagediff,save_directory,cutout_size=7,create_result_csv=False,save_result_csv_path=None,noisy_images=False):
    """
    Create a PNG image for each (x,y) in save_list with a cutout from old, new, and diff images next to each other with a size of cutout_size.
    :param save_list:
    :param imageold:
    :param imagenew:
    :param imagediff:
    :param save_directory:
    :param cutout_size:
    :param create_result_csv:
    :param save_result_csv_path:
    :param noisy_images:
    :return:
    """
    mean_old, std_old = np.mean(imageold), np.std(imageold)

    for tuple in save_list:
        x, y = tuple[0], tuple[1]
        if noisy_images:
            xn, yn = x + np.random.randint(-10, 10), y + np.random.randint(-10, 10)
            if xn - cutout_size < 0 or xn+cutout_size >= imageold.shape[1] or yn - cutout_size < 0 or yn + cutout_size >= imageold.shape[0]:
                continue
            else:
                x, y = xn, yn
        cutout_old = imageold[y - cutout_size:y + cutout_size, x - cutout_size:x + cutout_size]
        cutout_new = imagenew[y - cutout_size:y + cutout_size, x - cutout_size:x + cutout_size]
        cutout_diff = imagediff[y - cutout_size:y + cutout_size, x - cutout_size:x + cutout_size]
        vertical_bar = np.zeros((2 * cutout_size, 3))

        if noisy_images:
            rotate_angle = np.random.randint(0, 360)
            cutout_old = rotate(cutout_old, rotate_angle, reshape=False, mode='reflect')
            cutout_new = rotate(cutout_new, rotate_angle, reshape=False, mode='reflect')
            cutout_diff = rotate(cutout_diff, rotate_angle, reshape=False, mode='reflect')

        # Put Nan instead of 0
        vertical_bar[:] = np.nan

        merged_cutout = np.hstack((cutout_old, vertical_bar, cutout_new, vertical_bar, cutout_diff))
        plt.imshow(merged_cutout, cmap='viridis', vmin=mean_old - std_old, vmax=mean_old + std_old)
        plt.axis('off')
        plt.savefig(f"{save_directory}/source_{tuple[0]}_{tuple[1]}.png", bbox_inches='tight', pad_inches=0)
        plt.close()

    # Create a tutorial image called 0a.png which shows the template old image | new image | diff image

    tutorial_cutout_old = imageold[:cutout_size * 2, :cutout_size * 2]
    tutorial_cutout_new = imagenew[:cutout_size * 2, :cutout_size * 2]
    tutorial_cutout_diff = imagediff[:cutout_size * 2, :cutout_size * 2]
    vertical_bar = np.zeros((2 * cutout_size, 3))
    vertical_bar[:] = np.nan

    tutorial_merged_cutout = np.hstack(
        (tutorial_cutout_old, vertical_bar, tutorial_cutout_new, vertical_bar, tutorial_cutout_diff))

    plt.imshow(tutorial_merged_cutout, cmap='viridis', vmin=mean_old - 2 * std_old, vmax=mean_old + 2 * std_old)
    plt.text(cutout_size, cutout_size, 'Old', fontsize=12, color='red', ha='center')
    plt.text(2 * cutout_size + cutout_size + 3, cutout_size, 'New', fontsize=12, color='red', ha='center')
    plt.text(4 * cutout_size + cutout_size + 6, cutout_size, 'Subtraction', fontsize=12, color='red', ha='center')
    # plt.axvline(x=2*cutout_size, color='black', linewidth=3)
    # plt.axvline(x=4 * cutout_size + 3, color='black', linewidth=3)
    plt.axis('off')
    plt.savefig(f"{save_directory}/0a.png", bbox_inches='tight', pad_inches=0)
    plt.close()

    if create_result_csv:
        if save_result_csv_path is None:
            raise ValueError("save_result_csv_path must be provided if create_result_csv is True")
        with open(save_result_csv_path, 'w') as f:
            f.write("Image, Classification\n")
            for tuple in save_list:
                f.write(f"source_{tuple[0]}_{tuple[1]}, 1 \n")