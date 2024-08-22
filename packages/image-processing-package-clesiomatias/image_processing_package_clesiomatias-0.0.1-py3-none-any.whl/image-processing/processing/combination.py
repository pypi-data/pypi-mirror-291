import numpy as np
from skimage.color import rgb2gray
from skimage.exposure import match_histograms
from skimage.metrics import structural_similarity


def find_differences(image1, image2):
    """
    Find the differences between two images using structural similarity.

    Args:
        image1 (numpy.ndarray): The first image.
        image2 (numpy.ndarray): The second image.

    Returns:
        numpy.ndarray: A binary mask indicating the differences between the two images.
    """
    assert image1.shape == image2.shape, "Specify 2 images with the same shapes."
    
    gray1 = rgb2gray(image1)
    gray2 = rgb2gray(image2)
    (score, difference_image) = structural_similarity(gray1, gray2, full=True)
    print("Similarity of images: ", score)
    normalized_difference_image = (difference_image.np.min(difference_image))/(np.max(difference_image)-np.min(difference_image))
  
    return normalized_difference_image

def transfer_histogram(image1, image2):
    """
    Transfer the histogram of the first image to the second image.

    Args:
        image1 (numpy.ndarray): The first image.
        image2 (numpy.ndarray): The second image.

    Returns:
        numpy.ndarray: The second image with the histogram of the first image.
    """
   

    matched_image = match_histograms(image1, image2, multichannel=True)

    return matched_image