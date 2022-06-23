import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from PIL import Image

# Open an image
gray = cm.get_cmap('gray', 256)
im = Image.open('kids.tif')
x = np.array(im)

# Create and display the image histogram
plt.hist(x.flatten(), bins=np.linspace(0,255,256))
plt.xlabel('Pixel Intensity')
plt.ylabel('Number of Pixels')
plt.title('Histogram of the 8 bit image $\it{kids.tif}$')
plt.show()

