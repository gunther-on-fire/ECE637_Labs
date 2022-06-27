import numpy as np
from matplotlib import cm
from PIL import Image

gray = cm.get_cmap('gray', 256)
im = Image.open('gamma15.tif')
x = np.array(im)

cor_x = 255 * (np.double(x)/255) ** (1.5/1.84)

cor_x_uint8 = cor_x.astype(np.uint8)
cor_x_im = Image.fromarray(cor_x_uint8)
cor_x_im.save('cor_gamma15_img.png')