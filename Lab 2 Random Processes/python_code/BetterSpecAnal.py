import numpy as np               
from PIL import Image             
import matplotlib.pyplot as plt   

def BetterSpecAnal(x):
	# The number of pixels in a chunk (one direction)
	N = 64

	# The number of windows in horiztontal and vertical directions
	NUM_WIN = 5 

	# Create the 2-D Hamming window
	W = np.outer(np.hamming(N), np.hamming(N))

	# Set the coordinates of the initial position to iterate over NUM_WINxNUM_WIN windows
	h_start, v_start = np.subtract(im.size,(NUM_WIN*N, NUM_WIN*N)) // 2

	# Initialize the values of the FT with zeros
	Z = np.zeros((N,N))

	# Iterate over NUM_WINxNUM_WIN windows
	for v_chunk in range(NUM_WIN):
		for h_chunk in range(NUM_WIN):

			z = x[v_start+v_chunk*N:v_start+(v_chunk+1)*N, h_start+h_chunk*N:h_start+(h_chunk+1)*N]
			Z += (1/N)**2*np.abs(np.fft.fft2(z*W))**2

	# Normalize the result by the number of windows 
	Z /= NUM_WIN * NUM_WIN

	# Use fftshift to move the zero frequencies to the center of the plot.
	Z = np.fft.fftshift(Z)

	# Compute the logarithm of the Power Spectrum.
	Zabs = np.log(Z)

	return Zabs


# Read in a gray scale TIFF image.
im = Image.open('img04g.tif')
print('Read img04.tif.')
print('Image size: ', im.size)

# Display image object by PIL.
im.show(title='image')

# Import Image Data into Numpy array.
# The matrix x contains a 2-D array of 8-bit gray scale values. 
x = np.array(im)
print('Data type: ', x.dtype)

# Display numpy array by matplotlib.
plt.imshow(x, cmap=plt.cm.gray)
plt.title('Image')

# Set colorbar location. [left, bottom, width, height].
cax = plt.axes([0.9, 0.15, 0.04, 0.7]) 
plt.colorbar(cax=cax)
plt.show()

x = np.double(x)/255.0

N = 64

Zabs = BetterSpecAnal(x)

# Plot the result using a 3-D mesh plot and label the x and y axises properly. 
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
a = b = np.linspace(-np.pi, np.pi, num = N)
X, Y = np.meshgrid(a, b)

surf = ax.plot_surface(X, Y, Zabs, cmap=plt.cm.coolwarm)

ax.set_xlabel('$\\mu$ axis')
ax.set_ylabel('$\\nu$ axis')
ax.set_zlabel('Z Label')

fig.colorbar(surf, shrink=0.5, aspect=5)

plt.show()