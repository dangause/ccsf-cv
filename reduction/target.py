import numpy as np
import os
from astropy.io import fits
from utils.raw_filenames import filename_d

# Define a function to reduce a single target image
def reduce_target_image(image_file, master_bias_file, master_flat_file, output_filename):
    # Load the raw target image
    target_image, target_header = fits.getdata(image_file, header=True)
    
    # Load the master bias
    master_bias = fits.getdata(master_bias_file)
    
    # Load the master flat
    master_flat = fits.getdata(master_flat_file)
    
    # Step 1: Bias Subtraction
    bias_subtracted_image = target_image - master_bias
    
    # Step 2: Flat-Field Correction (divide by the normalized flat field)
    flat_corrected_image = bias_subtracted_image / master_flat
    
    # Save the reduced target image
    fits.writeto(output_filename, flat_corrected_image, target_header, overwrite=True)
    print(f"Reduced image saved as {output_filename}")
    return output_filename


def reduce_target_images(synth_flat_filename_l):
    raw_data_dir = 'data/raw'
    processed_data_dir = 'data/processed'

    target_flat_d_l = []
    for target_num in np.arange(0,len(list(filename_d['target'].values())[0])):
        target_d = list(filename_d['target'].values())[0][target_num]
        target_flat_d_l.append(
            {
                'target_filename': os.path.join(raw_data_dir, target_d['filename']),
                'master_bias_file': os.path.join(processed_data_dir, 'bias/master_bias.fits'),
                'synth_flat_file': synth_flat_filename_l[target_num],
                'output_filename': os.path.join(processed_data_dir, 'target', 'ay_psc', target_d['filename'])
            }
        )

    output_filenames_l = []
    for target_flat_d in target_flat_d_l:
        output_filenames_l.append(
            reduce_target_image(
                image_file=target_flat_d['target_filename'],
                master_bias_file=target_flat_d['master_bias_file'],
                master_flat_file=target_flat_d['synth_flat_file'],
                output_filename=target_flat_d['output_filename']
            )
        )

    return output_filenames_l
