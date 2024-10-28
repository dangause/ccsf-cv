import numpy as np
import glob
from astropy.io import fits



# Get a list of all bias FITS files
bias_files = glob.glob('../data/nickel_raw/bias/*.fits')  # Example: 'bias1.fits', 'bias2.fits', etc.

print('Bias file count: ', len(bias_files))

# Read all bias frames into a list
bias_frames = [fits.getdata(file) for file in bias_files]

# Stack the bias frames into a 3D array (shape: num_frames, height, width)
bias_stack = np.stack(bias_frames, axis=0)

# Compute the median across the stack (median-combine)
master_bias = np.median(bias_stack, axis=0)

# Save the master bias frame to a new FITS file
hdu = fits.PrimaryHDU(master_bias)
hdu.writeto('../data/bias/master_bias.fits', overwrite=True)

print("Master bias frame created and saved as 'master_bias.fits'.")
