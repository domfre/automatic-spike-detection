import argparse
import os

import numpy as np
import pandas as pd

from spidet.domain.Artifacts import Artifacts
from spidet.preprocess.artifact_detection import ArtifactDetector
from tests.variables import (
    DATASET_PATHS_008,
    LEAD_PREFIXES_008,
    DATASET_PATHS_007,
    LEAD_PREFIXES_007,
    DATASET_PATHS_006,
    LEAD_PREFIXES_006,
)

if __name__ == "__main__":
    # parse cli args
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--file", help="full path to file to be processed", required=True
    )
    parser.add_argument(
        "--annotations", help="path to annotations file", required=False
    )

    file: str = parser.parse_args().file
    annotations: str = parser.parse_args().annotations

    filename, ext = os.path.splitext(file[file.rfind("/") + 1 :])

    # Get trigger annotations if available
    if annotations is not None:
        df_annotations = pd.read_csv(annotations)
        trigger_times = list(
            (
                df_annotations[df_annotations["description"].str.startswith("TRIG")][
                    "onset"
                ]
            ).values
        )

    # Initialize artifact detector
    artifact_detector = ArtifactDetector()

    # Run artifact detection
    artifacts: Artifacts = artifact_detector.run(
        file_path=file,
        bipolar_reference=True,
        leads=LEAD_PREFIXES_008,
        trigger_times=trigger_times,
        channel_paths=DATASET_PATHS_008,
        detect_stimulation_artifacts=True,
    )

    if artifacts.bad_times is not None:
        np.savetxt(f"bad_times_{filename}.csv", artifacts.bad_times, delimiter=",")

    np.savetxt(
        f"bad_channels_{filename}.csv",
        artifacts.bad_channels.astype(int),
        delimiter=",",
    )

    print(f"Bad channels: {artifacts.bad_channels}")
    print(f"Bad times: {artifacts.bad_times}")
