import numpy as np
import matplotlib.pyplot as plt
import os

# Load data.npy
PATH = os.path.dirname(os.getcwd())
data = np.load(PATH+"/data.npy", allow_pickle=True)[()]
# List keys of dataset
data.keys()

# Wavelengths with step 10 nm
wavelength = np.arange(400, 710, 10)

# Prepare data
x = data['x'].reshape(31)
y = data['y'].reshape(31)
z = data['z'].reshape(31)

# Collect x, y, and z
xyz = np.array([x, y, z])

illum1 = data['illum1'].reshape(31)
illum2 = data['illum2'].reshape(31)

# Collect illuminant's data
illum = np.array([illum1, illum2])

"""
STEP 1: XYZ Color Matching Functions
"""
# Plot x, y, and z color matching
plt.figure(1)
for i in range(len(xyz)):
    plt.plot(wavelength, xyz[i], label=str(chr(ord('x')+i))+r'$_{0}(\lambda)$')
plt.xlim([400, 700])
plt.ylim([0, 1.1*np.max(xyz)])
plt.xlabel("Wavelength, nm")
plt.ylabel("Color matching function")
plt.title(r"$x_0(\lambda)$, $y_0(\lambda)$ and $z_0(\lambda)$ color matching functions")
plt.legend()
plt.savefig("xyz_color_matching.png")

"""
STEP 2: LMS Color Matching Functions
"""
# The inverse of the transformation matrix between XYZ and LMS color spaces
A_inv = np.array([[0.2430, 0.8560, -0.0440],
                  [-0.3910, 1.1650, 0.0870],
                  [0.0100, -0.0080, 0.5630]])

# Transform XYZ to LMS color coordinate system
lms = A_inv @ xyz

plt.figure(2)
lms_legend = ['l', 'm', 's']
for i in range(len(lms)):
    plt.plot(wavelength, lms[i], label=lms_legend[i]+r"$_{0}(\lambda)$")
plt.xlim([400, 700])
plt.ylim([0, 1.1 * np.max(lms)])
plt.xlabel("Wavelength, nm")
plt.ylabel("Color matching function")
plt.title(r"$l_0(\lambda)$, $m_0(\lambda)$ and $s_0(\lambda)$ color matching functions")
plt.legend()
plt.savefig("lms_color_matching.png")

"""
STEP 3: Illuminants
"""

# D65 vs Fluorescent Light
illum_legend = [r"$D_{65}$", "Fluorescent Light"]

plt.figure(3)
for i in range(len(illum)):
    plt.plot(wavelength, illum[i], label=illum_legend[i])
plt.xlim([400, 700])
plt.xlabel("Wavelength, nm")
plt.title(r"$D_{65}$ and fluorescent illuminants")
plt.legend()
plt.savefig("d65_vs_fluorescent.png")
