import os
import numpy as np
from astropy.io import fits
from astropy.io import fits
from scipy.optimize import curve_fit
from utils.raw_filenames import filename_d



def create_synthetic_flat(flat_files, exposure_times, master_bias_file, target_exposure_time, output_file=None):
    """
    Create a synthetic flat field for a given target exposure time by fitting a model 
    to flat fields taken with varying exposure times.
    
    Parameters:
    -----------
    flat_files : list of str
        List of file paths to the flat field FITS files.
    
    exposure_times : list of float
        List of exposure times corresponding to each flat file.
        
    master_bias_file : str
        File path to the master bias FITS file.
    
    target_exposure_time : float
        The exposure time for which the synthetic flat is needed.
    
    output_file : str or None
        File path to save the synthetic flat field FITS file. If None, no file is saved.
    
    Returns:
    --------
    synthetic_flat : np.ndarray
        The synthetic flat field corresponding to the target exposure time.
    """
    
    # Load the master bias file
    master_bias = fits.getdata(master_bias_file)
    # master_bias_ccd = CCDData(master_bias, unit='adu')

    # Initialize a list to store bias-subtracted, normalized flat fields
    normalized_flats = []

    # Loop over flat files and subtract bias and normalize each flat
    for flat_file in flat_files:
        # Load the flat field
        flat_data = fits.getdata(flat_file)
        # flat_ccd = CCDData(flat_data, unit='adu')
        
        # Subtract the master bias
        flat_bias_subtracted = flat_data - master_bias
        
        # Normalize the flat by its median
        flat_normalized = flat_bias_subtracted / np.median(flat_bias_subtracted)
        
        # Append the normalized flat to the list
        normalized_flats.append(flat_normalized)
    
    # Stack normalized flats into a 3D array (num_flats, height, width)
    flats_stack = np.stack(normalized_flats, axis=0)
    
    # Prepare an array to store the synthetic flat for the target exposure time
    synthetic_flat = np.zeros_like(normalized_flats[0])
    
    # Define a linear model for fitting (can be replaced with more complex models if needed)
    def linear_model(exposure, a, b):
        return a * exposure + b

    # Fit the model for each pixel and generate the synthetic flat
    for i in range(synthetic_flat.shape[0]):
        for j in range(synthetic_flat.shape[1]):
            # Get the pixel values across the normalized flats
            pixel_values = flats_stack[:, i, j]
            
            # Fit the linear model to the pixel values
            popt, _ = curve_fit(linear_model, exposure_times, pixel_values)
            
            # Use the fitted model to predict the flat field value at the target exposure time
            synthetic_flat[i, j] = linear_model(target_exposure_time, *popt)
    
    # Optionally, save the synthetic flat to a FITS file
    if output_file:
        hdu = fits.PrimaryHDU(synthetic_flat)
        hdu.writeto(output_file, overwrite=True)
    
    return synthetic_flat


def create_synth_flats_for_filters_at_target_exposure_times():
    synth_flat_filenames = []
    # For each filter in the target img list, create a custom synthetic flat file at that exposure time using create_synthetic_flat
    for filter_num in np.arange(0,len(list(filename_d['target'].values())[0])):
        flat_filenames = [exp_t_l[filter_num] for exp_t_l in filename_d['flat'].values()]
        raw_data_dir = 'data/raw'
        processed_data_dir = 'data/processed'

        # Read all flat frames into a list
        flat_frame_filepath_l = [os.path.join(raw_data_dir, filename) for filename in flat_filenames]

        # Get the exposure time for each target image
        target_exposure_time = list(filename_d['target'].values())[0][filter_num]['exposure_time']

        output_filename = os.path.join(processed_data_dir, 'flat/master_flat_filter_'+str(filter_num)+'_'+str(target_exposure_time)+'s'+'.fits')
        synth_flat_filenames.append(output_filename)
        create_synthetic_flat(flat_files=flat_frame_filepath_l,
                            exposure_times=[30, 5, 4, 3.5],
                            master_bias_file=os.path.join(processed_data_dir, 'bias/master_bias.fits'),
                            target_exposure_time=target_exposure_time,
                            output_file=output_filename)
        print('Synthetic flat created for filter ', filter_num, ' at exposure time ', target_exposure_time)

    return synth_flat_filenames