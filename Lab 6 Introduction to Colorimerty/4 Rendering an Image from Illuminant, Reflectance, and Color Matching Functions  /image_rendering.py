import numpy as np
from PIL import Image
import os


def calc_refl_energy(refl_coeff, illum):
    """
    Computes reflected light distribution
    """
    return refl_coeff * illum


def calc_xyz(xyz_cmf, refl_energy):
    """
    Computes XYZ tristimulus values
    :param xyz_cmf: color matching functions
    :param refl_energy: reflected light distribution
    for 31 wavelengths
    :return: numpy array of size (m, n, 3)
    """
    m, n, _ = refl_energy.shape
    XYZ = [[xyz_cmf @ refl_energy[i, j, :] for j in range(n)] for i in range(m)]
    return np.array(XYZ)


def xyz_to_rgb(M_inv, XYZ):
    """
    Transforms XYZ coordinates to RGB coordinates
    :param M_inv: the inverse of M 3x3 matrix
    that transforms RGB to XYZ
    :param XYZ: XYZ tristimulus values
    :return: numpy array of shape (m, n, 3) with RGB values
    """
    m, n, _ = XYZ.shape
    rgb = [[M_inv @ XYZ[i, j, :].T for j in range(n)] for i in range(m)]
    return np.array(rgb)


def gamma_corr(rgb):
    """
    Gamma correction of an image
    assuming gamma = 2.2
    """
    return 255 * (rgb ** (1/2.2))


def clip_rgb_comps(rgb):
    """
    Clips RGB values that fall
    outside the range [0, 1]
    """
    # Set the thresholds
    upper_lim = rgb > 1
    lower_lim = rgb < 0

    # Apply thresholding
    rgb[upper_lim] = 1
    rgb[lower_lim] = 0
    return rgb


"""
STEP 1: Prepare the data
"""
# Load data.npy
PATH = os.path.dirname(os.getcwd())
data = np.load(PATH+"/data.npy", allow_pickle=True)[()]
reflect = np.load(PATH+'/reflect.npy', allow_pickle=True)[()]

# Wavelengths with step 10 nm
wavelength = np.arange(400, 710, 10)

# Prepare xyz color matching functions
x = data['x'].reshape(31)
y = data['y'].reshape(31)
z = data['z'].reshape(31)

xyz = np.array([x, y, z])

# Prepare illuminant data
illum1 = data['illum1']  # D65 light source
illum2 = data['illum2']  # fluorescent source

# Prepare reflection coefficient table
R = reflect['R']

"""
STEP 2: Compute the reflected light energy at each wavelength
"""
I_D65 = calc_refl_energy(R, illum1)

"""
STEP 3: Compute the XYZ tristimulus values for each pixel
by applying the color matching functions to the spectral energy
"""
XYZ_D65 = calc_xyz(xyz, I_D65)

"""
STEP 4: Compute the transformation matrix from XYZ to RGB
"""
x_wp = 0.3127
y_wp = 0.3290
z_wp = 0.3583

RGB_709 = np.array([[0.64, 0.3, 0.15],
                    [0.33, 0.6, 0.06],
                    [0.03, 0.1, 0.79]])

D65_wp = np.array([[x_wp/y_wp, 1, z_wp/y_wp]])
k_rgb = np.linalg.inv(RGB_709) @ D65_wp.T
M = RGB_709 @ np.diag(k_rgb.reshape(3))

"""
STEP 5: Transform each pixel in XYZ array into RGB coordinates
"""
rgb_D65 = xyz_to_rgb(np.linalg.inv(M), XYZ_D65)

"""
STEP 6: Clip RGB component values 
that fall outside the range [0, 1]
"""
rgb_D65_clipped = clip_rgb_comps(rgb_D65)

"""
STEP 7: Gamma correction of the image
"""
rgb_D65_corr = gamma_corr(rgb_D65_clipped)

"""
STEP 8: Save the resulting image
"""
im_D65 = Image.fromarray(rgb_D65_corr.astype('uint8'), 'RGB')
im_D65.save("img_D65.tif")

"""
STEP 9: Same procedure for the fluorescent illuminant
"""
I_fluor = calc_refl_energy(R, illum2)
XYZ_fluor = calc_xyz(xyz, I_fluor)
rgb_fluor = xyz_to_rgb(np.linalg.inv(M), XYZ_fluor)
rgb_fluor_clipped = clip_rgb_comps(rgb_fluor)
gamma_corr_rgb_fluor = gamma_corr(rgb_fluor_clipped)

im_fluor = Image.fromarray(gamma_corr_rgb_fluor.astype('uint8'), 'RGB')
im_fluor.save("img_fluor.tif")
