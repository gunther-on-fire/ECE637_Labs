import numpy as np
import matplotlib.pyplot as plt

"""
EXERCISE 2.1: Generating Gaussian Random Vectors

W: "white" Gaussian random vectors (a Gaussian random matrix, n x p)
X_tilde: scaled random vectors (scaled by the square root of eigenvalues of cov_x matrix)
X: X_tilde rotated by cov_eigenvectors transformation
"""

p = 2  # random vector dimension
n = 1000  # number of samples

# Set the covariance matrix R_x to generate
# the Gaussian random vectors X_i
cov_x = np.array([[2, -1.2],
                  [-1.2, 1]])

# Eigendecomposition of the covariance matrix
cov_eigenvalues, cov_eigenvectors = np.linalg.eig(cov_x)

# Generate the whitened Gaussian random vector N(0, I)
W = np.random.normal(loc=0, scale=1, size=p*n).reshape(p, n)

# Generate the scaled random vectors X_tilde from W
X_tilde = np.dot(np.diag(cov_eigenvalues) ** 0.5, W)

# Generate the samples of the random vectors X from X_tilde
X = np.dot(cov_eigenvectors, X_tilde)

# Display the "whitened" random Gaussian random vectors W
plt.figure(1)
plt.plot(W[0, :], W[1, :], '.')
plt.xlabel(r"$W_{1}$:")
plt.ylabel(r"$W_{2}$")
plt.title(r"The whitened Gaussian random vectors $W_{i}$")
plt.axis('equal')
plt.show()

# Display the scaled W (that is, X_tilde vectors)
plt.figure(2)
plt.plot(X_tilde[0, :], X_tilde[1, :], '.')
plt.xlabel(r"$\tilde{X}_{1}$")
plt.ylabel(r"$\tilde{X}_{2}$")
plt.title(r"The scaled random vectors $\tilde{X}_{i}$")
plt.axis('equal')
plt.show()

# Display the random vectors X with covariance R_x
plt.figure(3)
plt.plot(X[0, :], X[1, :], '.')
plt.xlabel(r"$X_{1}$")
plt.ylabel(r"$X_{2}$")
plt.title(r"Generated random samples $X_i=E\tilde{X}_{i}$")
plt.axis('equal')
plt.show()

"""
EXERCISE 2.2: Covariance Estimation and Whitening
"""

# Estimate the covariance using samples of random Gaussian vectors X_i
mu_x = np.mean(X, axis=1, keepdims=True)  # the sample mean
Z = X - mu_x  # removing the sample mean from the data observed
cov_x_est = np.dot(Z, Z.T) / (n - 1)  # the unbiased covariance estimate R_x
print("R_x = ", np.round(cov_x_est, 2))

# Eigendecomposition of the covariance estimate
cov_est_eigenvalues, cov_est_eigenvectors = np.linalg.eig(cov_x_est)
cov_est_eigenvalues_mx = np.diag(cov_est_eigenvalues)
inv_cov_eigenvalues = (np.linalg.inv(cov_est_eigenvalues_mx)) ** 0.5

# Decorrelate the samples of X_i using the eigendecomposition from above
X_tilde_rev = np.dot(cov_est_eigenvectors.T, X)

# "Whiten" the X_tilde samples
W_rev = np.dot(inv_cov_eigenvalues, X_tilde_rev)

# Compute the covariance estimate of whitened Gaussian vectors
mu_w = np.mean(W_rev, axis=1, keepdims=True)  # the sample mean for W
Z_w = W_rev - mu_w  # subtract the sample mean to get the zero-centered vectors
cov_w_est = np.dot(Z_w, Z_w.T) / (n - 1)  # the estimate R_w
print("R_w = ", np.round(cov_w_est, 2))

# Display the X_tilde_rev vectors
plt.figure(4)
plt.plot(X_tilde_rev[0, :], X_tilde_rev[1, :], '.')
plt.xlabel(r"$\tilde{X}_{1}$")
plt.ylabel(r"$\tilde{X}_{2}$")
plt.title(r"Decorrelated random samples $\tilde{X}_{i}=E^{t}X_{i}$")
plt.axis('equal')
plt.show()

# Display the whitened Gaussian random vectors W_rev
plt.figure(5)
plt.plot(W_rev[0, :], W_rev[1, :], '.')
plt.xlabel(r"$W_{1}$")
plt.ylabel(r"$W_{2}$")
plt.title(r"The whitened Gaussian random vectors $W_{i}$")
plt.axis('equal')
plt.show()
