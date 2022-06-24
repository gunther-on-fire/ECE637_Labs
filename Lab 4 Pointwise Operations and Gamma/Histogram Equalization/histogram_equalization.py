import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from PIL import Image


def equalize(img):
    """
    Equalize the histogram of an image img
    :param img: numpy.array of the image the histogram of which
    is going to be equalized
    :return: equalized histogram of the image img
    """

    # Get the histogram of an image X
    hist, bins = np.histogram(img.flatten(), bins=np.linspace(0, 255, 256))

    # Get the estimate of the cdf of the image X
    cdf_x = np.cumsum(hist)/np.sum(hist)

    plt.figure(1)
    plt.xlabel("i, Pixel Intensity")
    plt.ylabel(r'$\hat{F_{x}}(i)}$')
    plt.xlim([0, 255])
    plt.ylim([-0.05, 1.05])
    plt.title(r'The CDF $\hat{F_{x}}(i)}$ for the 8 bit image $\it{kids.tif}$')
    plt.plot(cdf_x)
    plt.show()

    # Pass the image img through the CDF of X
    y_s = cdf_x[img]

    # Get min and max values of the new image
    y_min = np.min(y_s)
    y_max = np.max(y_s)

    # Get the equalized image
    z_s = np.round(255*(y_s - y_min)/(y_max - y_min))

    return z_s.astype(np.uint8)


# Open an image
gray = cm.get_cmap('gray', 256)
im = Image.open('kids.tif')
x = np.array(im)

# Equalize the histogram
hist_equalized = equalize(x)

# Display the equalized histogram
plt.figure(2)
plt.xlim([0, 255])
plt.xlabel("Pixel Intensity")
plt.ylabel("Number of Pixels")
plt.title(r'The equalized histogram for the 8 bit image $\it{kids.tif}$')
plt.hist(hist_equalized.flatten(), bins=np.linspace(0, 255, 256))
plt.show()

# Display the equalized image
plt.figure(3)
plt.title(r'The image $\it{kids.tif}$ after histogram equalization')
plt.imshow(hist_equalized, cmap=gray, vmin=0, vmax=255)
plt.show()
