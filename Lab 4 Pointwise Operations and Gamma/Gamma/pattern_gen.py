import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from PIL import Image


def gen_test_img(g):

    arr = np.zeros((256, 256))

    for i in range(0, 16, 2):
        arr[16*i:16*(i+1), :] = np.kron([[255, 0] * 64, [0, 255] * 64] * 4, np.ones((2, 2)))
        arr[16*(i+1):16*(i+2), :] = g

    return Image.fromarray(arr.astype(np.uint8))


gray = cm.get_cmap('gray', 256)

for gray_level in [127, 165, 170]:
    pattern = gen_test_img(gray_level)

    plt.figure()
    plt.title("gray level is {}".format(gray_level))
    plt.imshow(pattern, cmap=gray)
    plt.savefig("pattern_"+str(gray_level)+".png")
    plt.close()
