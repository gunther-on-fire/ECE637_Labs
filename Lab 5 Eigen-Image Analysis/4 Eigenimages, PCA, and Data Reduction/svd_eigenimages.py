import numpy as np
import read_data as rd
import matplotlib.pyplot as plt

"""
STEP 1: Calculations for 4 Eigenimages, PCA, and Data Reduction
"""
# Read the training images to get
# the data matrix p x n
X = rd.read_data()

# p is the number of pixels in an image
# n is the number of training images
p, n = X.shape

# Compute the "mean" image
mu_est = np.mean(X, axis=1, keepdims=True)

# Center the data by subtracting the mean image
# from each column of X
X_centered = X - mu_est

# Compute Z that can be used
# to get the covariance matrix
Z = X_centered / np.sqrt(n-1)

# Singular value decomposition of Z
u, s, vh = np.linalg.svd(Z, full_matrices=False)

# Compute the projection coefficients
Y = np.dot(u.T, X_centered)

"""
STEP 2: Display the results
"""

letters = 'abcd'
# Set the number of projection coefficients
NUM_PROJ_COEFF = 10
# Set the number of images to display
NUM_IMAGES = 4

# Projection coefficients vs eigenvector number
plt.figure(1)

for i in range(NUM_IMAGES):
    plt.plot(np.arange(1, NUM_PROJ_COEFF + 1), Y[:NUM_PROJ_COEFF, i], label=letters[i])

plt.legend(loc=4)
plt.title("Projection coefficients vs. eigenvector numbers", fontsize=14)
plt.xlabel("Eigenvector number")
plt.ylabel("Projection coefficient")
plt.xlim([1, NUM_PROJ_COEFF])
plt.savefig('proj_coeff_vs_eigenvec_num.png')
plt.close()

# Display image 0 reconstructed from m eigenvectors
fig2, axs2 = plt.subplots(3, 2, num=2)
fig2.suptitle("Image resynthesized from first m eigenvectors", fontsize=14)

eigenvectors = [1, 5, 10, 15, 20, 30]

for k in range(len(eigenvectors)):
    img = np.dot(u[:, :eigenvectors[k]], Y[:eigenvectors[k], :])
    img += mu_est
    img = np.reshape(img[:, 0], (64, 64))

    axs2[k//2, k % 2].imshow(img, cmap=plt.cm.gray, interpolation='none')
    axs2[k//2, k % 2].set_title(f"m={eigenvectors[k]}")

plt.tight_layout(rect=[0, 0, 1, 0.95])
plt.savefig("rec_image.png")
plt.close()

# Display first 12 eigenimages
fig3, axs3 = plt.subplots(3, 4, num=3)
fig3.suptitle("The first 12 eigenimages", fontsize=14)

for k in range(12):
    img = np.reshape(u[:, k], (64, 64))

    axs3[k//4, k % 4].imshow(img, cmap=plt.cm.gray, interpolation='none')
    axs3[k//4, k % 4].set_title(f"eigenimage {k+1}")

plt.tight_layout(rect=[0, 0, 1, 0.95])
plt.savefig("eigenimages.png")
plt.close()
