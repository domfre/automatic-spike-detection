import multiprocessing
from typing import List

import numpy as np
from loguru import logger

from spikepy.domain.Trace import Trace
from spikepy.preprocessing.filtering import filter_signal, notch_filter_signal
from spikepy.preprocessing.line_length import apply_line_length
from spikepy.preprocessing.resampling import resample_data
from spikepy.preprocessing.rescaling import rescale_data


def apply_preprocessing_steps(
    traces: List[Trace],
    notch_freq: int,
    resampling_freq: int,
    bandpass_cutoff_low: int,
    bandpass_cutoff_high: int,
):
    # TODO add documentation, clean up

    # Channel names
    channel_names = [trace.label for trace in traces]

    logger.debug(f"Channels processed by worker: {channel_names}")

    # Frequency of data
    data_freq = traces[0].sfreq

    # Extract data from traces
    traces = np.array([trace.data for trace in traces])

    # 1. Bandpass filter
    logger.debug(
        f"Bandpass filter data between {bandpass_cutoff_low} and {bandpass_cutoff_high} Hz"
    )

    bandpass_filtered = filter_signal(
        sfreq=data_freq,
        cutoff_freq_low=bandpass_cutoff_low,
        cutoff_freq_high=bandpass_cutoff_high,
        data=traces,
    )

    # 2. Notch filter
    logger.debug(f"Apply notch filter at {notch_freq} Hz")
    notch_filtered = notch_filter_signal(
        eeg_data=bandpass_filtered,
        notch_frequency=notch_freq,
        low_pass_freq=bandpass_cutoff_high,
        sfreq=data_freq,
    )

    # 3. Scaling channels
    logger.debug("Rescale filtered data")
    scaled_data = rescale_data(
        data_to_be_scaled=notch_filtered, original_data=traces, sfreq=data_freq
    )

    # 4. Resampling data
    logger.debug(f"Resample data at sampling frequency {resampling_freq} Hz")
    resampled_data = resample_data(
        data=scaled_data,
        channel_names=channel_names,
        sfreq=data_freq,
        resampling_freq=resampling_freq,
    )

    # 5. Compute line length
    logger.debug("Apply line length computations")
    line_length_eeg = apply_line_length(eeg_data=resampled_data, sfreq=data_freq)

    # 6. Downsample to 50 hz
    logger.debug("Resample line length at 50 Hz")
    resampled_data = resample_data(
        data=line_length_eeg,
        channel_names=channel_names,
        sfreq=data_freq,
        resampling_freq=50,
    )

    # Resampling produced some negative values, replace by 0
    resampled_data[resampled_data < 0] = 0

    return resampled_data


def parallel_preprocessing(
    traces: List[Trace],
    notch_freq: int = 50,
    resampling_freq: int = 500,
    bandpass_cutoff_low: int = 0.1,
    bandpass_cutoff_high: int = 200,
    n_processes: int = 8,
):
    # TODO: add documentation
    logger.debug(f"Starting preprocessing pipeline on {n_processes} parallel processes")

    # Using all available cores for process pool
    n_cores = multiprocessing.cpu_count()

    with multiprocessing.Pool(processes=n_cores) as pool:
        preprocessed_data = pool.starmap(
            apply_preprocessing_steps,
            [
                (
                    data,
                    notch_freq,
                    resampling_freq,
                    bandpass_cutoff_low,
                    bandpass_cutoff_high,
                )
                for data in np.array_split(traces, n_processes)
            ],
        )

    data = np.concatenate(preprocessed_data, axis=0)
    logger.debug("Preprocessing pipeline finished successfully, returning data")
    return data