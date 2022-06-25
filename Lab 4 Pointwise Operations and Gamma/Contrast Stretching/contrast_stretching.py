import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from PIL import Image


def stretch(input_img, T1, T2):

    output_img = np.zeros(input_img.shape)
    row, col = input_img.shape

    for i in range(row):
        for j in range(col):
            if input_img[i, j] <= T1:
                output_img[i, j] = 0
            elif input_img[i, j] >= T2:
                output_img[i, j] = 255
            else:
                output_img[i, j] = 255 * (input_img[i, j] - T1)/(T2 - T1)

    return output_img.astype(np.uint8)


# Open an image
gray = cm.get_cmap('gray', 256)
im = Image.open('kids.tif')
x = np.array(im)

# Enhance the image by contrast stretching
y = stretch(x, 70, 180)

# Display initial image vs processed image
f, axarr = plt.subplots(2)
plt.suptitle('Contrast stretching for image enhancement')
axarr[0].title.set_text("Initial image")
axarr[0].imshow(x, cmap=gray, vmin=0, vmax=255)
axarr[1].title.set_text("Enhanced image")
axarr[1].imshow(y, cmap=gray, vmin=0, vmax=255)
plt.tight_layout()
plt.savefig('init_vs_enhanced.png')
plt.close()

# Display the histogram of the initial image
plt.figure(2)
plt.title(r"The histogram of the image $\it{kids.tif}$ $\bf{before}$ enhancement")
plt.hist(x.flatten(), bins=np.linspace(0, 255, 256))
plt.savefig('init_hist.png')
plt.close()

# Display the histogram of the enhanced image
plt.figure(3)
plt.title(r"The histogram of the image $\it{kids.tif}$ $\bf{after}$ enhancement")
plt.hist(y.flatten(), bins=np.linspace(0, 255, 256))
plt.savefig('enhanced_hist.png')
plt.close()
