import mne
import numpy as np
from charset_normalizer.md import List
from mne.io import RawArray


def resample_data(
    data: np.array, channel_names: List[str], sfreq: int, resampling_freq: int
) -> np.array:
    """
    Resamples the data with the desired frequency

    :param sfreq: original frequency of the data
    :param channel_names: labels of the channels
    :param data: data to be resampled
    :param resampling_freq:
    :return: resampled data
    """
    info = mne.create_info(ch_names=channel_names, sfreq=sfreq)
    resampled_data = RawArray(data, info=info).resample(sfreq=resampling_freq)
    return resampled_data.get_data()