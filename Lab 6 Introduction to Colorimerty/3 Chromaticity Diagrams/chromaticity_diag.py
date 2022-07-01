import numpy as np
import matplotlib.pyplot as plt
import os

# Load data.npy
PATH = os.path.dirname(os.getcwd())
data = np.load(PATH+"/data.npy", allow_pickle=True)[()]

# Wavelengths with step 10 nm
wavelength = np.arange(400, 710, 10)

# Prepare data
x0 = data['x'].reshape(31)
y0 = data['y'].reshape(31)
z0 = data['z'].reshape(31)

x = x0 / (x0 + y0 + z0)
y = y0 / (x0 + y0 + z0)

# Matrices
RGB_CIE_1931 = np.array([[0.73467, 0.26533, 0.0],
                         [0.27376, 0.71741, 0.00883],
                         [0.16658, 0.00886, 0.82456],
                         [0.73467, 0.26533, 0.0]])

RGB_709 = np.array([[0.640, 0.330, 0.030],
                    [0.300, 0.600, 0.100],
                    [0.150, 0.060, 0.790],
                    [0.640, 0.330, 0.030]])

D_65 = np.array([[0.3127, 0.3290, 0.3583]])

EE = np.array([[0.3333, 0.3333, 0.3333]])

# Display the results
plt.figure()

plt.xlim([0, 0.9])
plt.ylim([0, 0.9])
plt.title("Chromaticity diagram for CIE 1931 and Rec. 709 RGB primaries")
plt.plot(x, y)
plt.plot(RGB_CIE_1931[:, 0], RGB_CIE_1931[:, 1], marker='*')
for i in range(RGB_CIE_1931.shape[0]):
    plt.text(RGB_CIE_1931[i, 0], RGB_CIE_1931[i, 1], r'$RGB_{CIE\_1931}$')
plt.plot(RGB_709[:, 0], RGB_709[:, 1], marker='^')
for i in range(RGB_709.shape[0]):
    plt.text(RGB_709[i, 0], RGB_709[i, 1], r'$RGB_{709}$')
plt.plot(D_65[:, 0], D_65[:, 1], marker='o', color='red')
plt.text(0.9 * D_65[:, 0], 0.85 * D_65[:, 1], r'$D_{65}$')
plt.plot(EE[:, 0], EE[:, 1], marker='.', color='blue')
plt.text(1.02 * EE[:, 0], 1.02 * EE[:, 1], 'EE')

plt.savefig("chromaticity_diagram.png")
