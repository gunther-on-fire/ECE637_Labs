import numpy as np
import matplotlib.pyplot as plt
import os

RGB_709 = np.array([[0.64, 0.3, 0.15],
                    [0.33, 0.6, 0.06],
                    [0.03, 0.1, 0.79]])

RGB_709_graph = np.array([[0.640, 0.330, 0.030],
                          [0.300, 0.600, 0.100],
                          [0.150, 0.060, 0.790],
                          [0.640, 0.330, 0.030]])
M_709 = RGB_709 @ np.eye(3)

# Load data.npy
PATH = os.path.dirname(os.getcwd())
data = np.load(PATH+"/data.npy", allow_pickle=True)[()]

# Prepare data
x0 = data['x'].reshape(31)
y0 = data['y'].reshape(31)
z0 = data['z'].reshape(31)

x_d = x0 / (x0 + y0 + z0)
y_d = y0 / (x0 + y0 + z0)

a = b = np.arange(0, 1.005, 0.005)
x, y = np.meshgrid(a, b)

z = 1 - x - y

m = n = x.shape[0]
XYZ = np.zeros((m, n, 3))

XYZ[:, :, 0] = x
XYZ[:, :, 1] = y
XYZ[:, :, 2] = z

rgb = np.zeros((m, n, 3))

for p in range(m):
    for q in range(n):
        rgb[p, q, :] = np.linalg.inv(M_709) @ XYZ[p, q, :].T
        if np.any(rgb[p, q, :] < 0):
            rgb[p, q, :] = np.array([1, 1, 1])

gc_rgb = rgb ** (1/2.2)

plt.figure()
plt.imshow(gc_rgb, extent=[0, 1, 0, 1], origin='lower')
plt.plot(x_d, y_d)
plt.plot(RGB_709_graph[:, 0], RGB_709_graph[:, 1], color='black', marker='^')
for i in range(RGB_709_graph.shape[0]):
    plt.text(1.05*RGB_709_graph[i, 0], 0.97*RGB_709_graph[i, 1], r'$RGB_{709}$')
plt.savefig("color_chromaticity_diagram.png")
