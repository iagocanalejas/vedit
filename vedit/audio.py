import matplotlib.pyplot as plt
import numpy as np
from pydub import AudioSegment
from scipy.signal import correlate

from .models import AudioData


def read_audio(file: str) -> tuple[float, np.ndarray]:
    audio = AudioSegment.from_file(file)
    data = np.array(audio.get_array_of_samples())
    if audio.channels == 2:
        data = data.reshape((-1, 2)).mean(axis=1)  # Convert stereo to mono
    return audio.frame_rate, data


def read_and_trim_audio(file: str, duration_ms: int = 30 * 1000) -> tuple[float, np.ndarray]:
    audio = AudioSegment.from_file(file)
    trimmed_audio = audio[:duration_ms]  # Trim to the specified duration
    data = np.array(trimmed_audio.get_array_of_samples())
    if trimmed_audio.channels == 2:
        data = data.reshape((-1, 2)).mean(axis=1)  # Convert stereo to mono
    return audio.frame_rate, data

# TODO: audio delay prediction
def predict_start_delay(audio1: AudioData, audio2: AudioData) -> float:
    correlation = correlate(audio1.sample, audio2.sample, mode="full")
    lag = np.argmax(correlation) - (len(audio2.sample) - 1)
    return float(lag / audio1.frame_rate)


def _plot_waves(audio1: AudioData, audio2: AudioData):
    sample_rate1, data1 = audio1.frame_rate, audio1.sample
    sample_rate2, data2 = audio2.frame_rate, audio2.sample

    # Check if the audio files are stereo and convert to mono if necessary
    if len(data1.shape) == 2:
        data1 = data1.mean(axis=1)
    if len(data2.shape) == 2:
        data2 = data2.mean(axis=1)

    # Generate time axes for both audio files
    time1 = np.linspace(0.0, len(data1) / sample_rate1, num=len(data1))
    time2 = np.linspace(0.0, len(data2) / sample_rate2, num=len(data2))

    # Plot the audio waves
    plt.figure(figsize=(15, 6))

    plt.subplot(2, 1, 1)
    plt.plot(time1, data1, label="Audio Wave 1")
    plt.xlabel("Time [s]")
    plt.ylabel("Amplitude")
    plt.title("Audio Wave 1")
    plt.legend()

    plt.subplot(2, 1, 2)
    plt.plot(time2, data2, label="Audio Wave 2")
    plt.xlabel("Time [s]")
    plt.ylabel("Amplitude")
    plt.title("Audio Wave 2")
    plt.legend()

    plt.tight_layout()
    plt.show()
