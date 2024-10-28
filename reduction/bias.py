import numpy as np
import os
from astropy.io import fits
from utils.raw_filenames import filename_d

def create_master_bias_file():
    bias_filenames = filename_d['bias']
    raw_data_dir = 'data/raw'

    print('Bias file count: ', len(bias_filenames))

    # Read all bias frames into a list
    bias_frames = [fits.getdata(os.path.join(raw_data_dir, file)) for file in bias_filenames]

    # Stack the bias frames into a 3D array (shape: num_frames, height, width)
    bias_stack = np.stack(bias_frames, axis=0)

    # Compute the median across the stack (median-combine)
    master_bias = np.median(bias_stack, axis=0)

    # Save the master bias frame to a new FITS file
    hdu = fits.PrimaryHDU(master_bias)
    master_bias_output_filename = 'data/processed/bias/master_bias.fits'
    hdu.writeto(master_bias_output_filename, overwrite=True)

    print(f"Master bias frame created and saved as {master_bias_output_filename}")
    return hdu