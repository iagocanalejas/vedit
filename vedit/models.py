from dataclasses import dataclass

import numpy as np
from vscripts import AudioStream, VideoStream


@dataclass
class VideoData:
    stream: VideoStream


@dataclass
class AudioData:
    stream: AudioStream

    frame_rate: float
    sample: np.ndarray
