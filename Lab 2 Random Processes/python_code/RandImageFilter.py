import numpy as np                 
from PIL import Image            
import matplotlib.pyplot as plt    

# Set the size of an image
size = (512, 512)

# Create a new grayscale image with the given size.
rand_img = Image.new('L', size)

# Generate a random image in accordance with the uniform distribution on [-0.5, 0.5]
x = np.random.uniform(-0.5, 0.5, size)

# Scale the image
x_scaled = 255 * (x + 0.5)

# Display x_scaled by matplotlib.
plt.imshow(x_scaled.astype('uint8'), cmap=plt.cm.gray)
plt.title('A randomly generated image')
plt.show()

# Save the image x_scaled
rand_img = Image.fromarray(x_scaled.astype('uint8'))
rand_img.save('rand_img.tif')


# Filter the image
y = np.zeros((size[0]+1, size[1]+1))

for m in range(size[0]):
	for n in range(size[1]):
		y[m+1][n+1] = 3*x[m][n]+0.99*y[m][n+1]+0.99*y[m+1][n]-0.9801*y[m][n]

y = y[1:,1:]
y += 127
y = np.clip(y, 0, 255)

# Display the filtered image by matplotlib.
plt.imshow(y.astype('uint8'), cmap=plt.cm.gray)
plt.title('The filtered image')
plt.show()

# Save the filtered image
rand_img_filtered = Image.fromarray(y.astype('uint8'))
rand_img_filtered.save('rand_img_filtered.tif')