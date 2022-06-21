import numpy as np
from PIL import Image              
import matplotlib.pyplot as plt    

PSD_X = 1/12
N = 64

a = b = np.linspace(-np.pi, np.pi, num = N)
X, Y = np.meshgrid(a, b)

psd_y = PSD_X * abs(3/((1-0.99*np.exp(-1j*X)-0.99*np.exp(-1j*Y)+0.9801*np.exp(-1j*X)*np.exp(-1j*Y))))**2

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

surf = ax.plot_surface(X, Y, np.log(psd_y), cmap=plt.cm.coolwarm)

ax.set_xlabel('$\\mu$ axis')
ax.set_ylabel('$\\nu$ axis')
ax.set_zlabel('Z Label')

fig.colorbar(surf, shrink=0.5, aspect=5)

plt.show()