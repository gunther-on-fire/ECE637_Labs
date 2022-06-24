import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from PIL import Image
import sys # added to read the external arguments for the script

for i in range(1, len(sys.argv)):
    # Read the filename
    im_name = str(sys.argv[i])

    # Open an image
    gray = cm.get_cmap('gray', 256)
    im = Image.open(im_name)
    x = np.array(im)

    # Create and display the image histogram
    plt.figure()
    plt.hist(x.flatten(), bins=np.linspace(0,255,256))
    plt.xlabel('Pixel Intensity')
    plt.xlim(0,255)
    plt.ylabel('Number of Pixels')
    plt.title('Histogram of the 8 bit image $\it{}$'.format(im_name))
    plt.show()