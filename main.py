from reduction.bias import create_master_bias_file
from reduction.flat import create_synth_flats_for_filters_at_target_exposure_times
from reduction.target import reduce_target_images
from reduction.reduce import run_reduction_pipeline

def main():
    # # bias_hdu = create_master_bias_file()
    # # create_synth_flats_for_filters_at_target_exposure_times()
    # synth_flat_filename_l = [
    #     'data/processed/flat/master_flat_filter_0_30s.fits',
    #     'data/processed/flat/master_flat_filter_1_180s.fits',
    #     'data/processed/flat/master_flat_filter_2_120s.fits',
    #     'data/processed/flat/master_flat_filter_3_60s.fits',
    #     'data/processed/flat/master_flat_filter_4_60s.fits',
    # ]
    # reduce_target_images(synth_flat_filename_l)
    run_reduction_pipeline()

if __name__ == '__main__':
    main()