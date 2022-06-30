import numpy as np
import read_data as rd
from PIL import Image
import sys

DATACHAR = 'abcdefghijklmnopqrstuvwxyz'  # image labels as a string
DATADIR_TEST = './test_data/veranda'  # directory where the data files reside

EIGEN_NUM = 10  # the dimension of original image reduced representation
NUM_CLASSES = len(DATACHAR)  # the number of image classes
true_labels = list(DATACHAR)  # real labels of images from the test set


def read_data(datadir):
    """
        Read in all test images into columns of a single matrix X.
        Returns:
            X: Image column matrix.

    """
    for ch in DATACHAR:
        num_img = ord(ch)-ord("a")

        fname = '/'.join([datadir, ch])+'.tif'

        im = Image.open(fname)
        rows, cols = im.size
        img = np.array(im)
        X[:, num_img] = np.reshape(img, (1, rows*cols))
    return X


def class_mean(images):
    """
    Returns mean estimate of images in a class
    """
    avg_img = np.mean(images, axis=1, keepdims=True)
    return avg_img.ravel()


def class_covariance(num_images, class_images, mean_k):
    """
    Reads the number of images in a class, images of the class,
    the mean estimate of the class, and the dimension of
    Returns:
         covariance matrix cov_mx of a class
    """
    dim_mx = class_images.shape[0]
    cov_mx = np.zeros((dim_mx, dim_mx))
    for img in range(num_images):
        cov_mx += np.outer(class_images[:, img]-mean_k, class_images[:, img]-mean_k)
    cov_mx /= (num_images - 1)
    return cov_mx


def classify(img, mean_val, cov_mx):
    return (np.dot((img-mean_val), np.dot(np.linalg.inv(cov_mx), (img-mean_val))) +
            np.log(np.abs(np.linalg.det(cov_mx))))


def specify_classifier(option):

    """
    Classifies the test data
    :param option: specifies the type of classifier
    :return: Maximum likelihood result for Gaussian distributed images
    """

    if option == "0":
        for k in range(NUM_CLASSES):
            mu_k = params[k]['mean']
            cov_k = params[k]['cov']
            class_scores[k] = classify(test_img, mu_k, cov_k)

    elif option == "1":
        for k in range(NUM_CLASSES):
            mu_k = params[k]['mean']
            cov_k_diag = np.diag(np.diag(params[k]['cov']))
            class_scores[k] = classify(test_img, mu_k, cov_k_diag)

    elif option == "2":
        R_wc = np.zeros((EIGEN_NUM, EIGEN_NUM))
        for k in range(NUM_CLASSES):
            R_wc += params[k]['cov']
        R_wc /= NUM_CLASSES
        for k in range(NUM_CLASSES):
            mu_k = params[k]['mean']
            class_scores[k] = classify(test_img, mu_k, R_wc)

    elif option == "3":
        R_wc = np.zeros((EIGEN_NUM, EIGEN_NUM))
        for k in range(NUM_CLASSES):
            R_wc += params[k]['cov']
        R_wc /= NUM_CLASSES
        Lambda = np.diag(np.diag(R_wc))
        for k in range(NUM_CLASSES):
            mu_k = params[k]['mean']
            class_scores[k] = classify(test_img, mu_k, Lambda)

    else:
        Identity = np.eye(EIGEN_NUM)
        for k in range(NUM_CLASSES):
            mu_k = params[k]['mean']
            class_scores[k] = classify(test_img, mu_k, Identity)

    return class_scores


def label_mismatch(true_lbl, pred_lbl):
    labels = []
    for lbl in range(len(true_lbl)):
        if true_lbl[lbl] != pred_lbl[lbl]:
            dic_labels = {'True': true_lbl[lbl], 'Predicted': pred_lbl[lbl]}
            labels.append(dic_labels)
    return labels


np.set_printoptions(threshold=sys.maxsize)

"""
STEP 1: Reduce the dimension of the training data
"""
# Reading the training set images, each column is one image
X = rd.read_data()

# p is the number of pixels in an image
# n is the number of images
p, n = X.shape

# Compute and subtract the mean image
mu_est = np.mean(X, axis=1, keepdims=True)
X_centered = X - mu_est
Z = X_centered / np.sqrt(n-1)

# SVD decomposition of Z (the covariance is then R = Z*Z.T)
u, s, vh = np.linalg.svd(Z, full_matrices=False)

# The transmission matrix A that consists of EIGEN_NUM left singular vectors
# u are the eigenvectors of the covariance, we pick EIGEN_NUM of the largest
A = u[:, :EIGEN_NUM]

# The lower dimensional representation of training images X_centered
Y = np.dot(A.T, X_centered)

"""
STEP 2: Compute the class means and covariances for each class of training data
and store them in a dictionary
"""
# The list to store the mean value estimate and the covariance matrix for each class
params = []

for k in range(NUM_CLASSES):
    # Get all training images of the class k
    class_samples = Y[:, k::NUM_CLASSES]

    # Get the number of images in the class k
    num_samples = class_samples.shape[1]

    # Calculate parameters
    mu_k = class_mean(class_samples)
    cov_k = class_covariance(num_samples, class_samples, mu_k)

    # Append result of iteration to the list
    dic = {'mean': mu_k, 'cov': cov_k}
    params.append(dic)

"""
STEP 3: Test the classifier
"""

X_test = read_data(DATADIR_TEST)
X_test_centered = X_test - mu_est
Y_test = np.dot(A.T, X_test_centered)

# Classifying the images from the test set
class_scores = np.zeros(NUM_CLASSES)
predicted_labels = []

for i in range(NUM_CLASSES):
    test_img = Y_test[:, i]

    class_scores = specify_classifier("2")
    label = np.argmin(class_scores)
    char = chr(ord('a') + label)
    predicted_labels.append(char)

# Display the classification results
print(label_mismatch(true_labels, predicted_labels))
