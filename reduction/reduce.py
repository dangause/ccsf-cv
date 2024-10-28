from reduction.bias import create_master_bias_file
from reduction.flat import create_synth_flats_for_filters_at_target_exposure_times
from reduction.target import reduce_target_images

def run_reduction_pipeline():
    create_master_bias_file()
    synth_flat_filename_l = create_synth_flats_for_filters_at_target_exposure_times()
    # synth_flat_filename_l = [
    #     'data/processed/flat/master_flat_filter_0_30s.fits',
    #     'data/processed/flat/master_flat_filter_1_180s.fits',
    #     'data/processed/flat/master_flat_filter_2_120s.fits',
    #     'data/processed/flat/master_flat_filter_3_60s.fits',
    #     'data/processed/flat/master_flat_filter_4_60s.fits',
    # ]
    reduce_target_images(synth_flat_filename_l)