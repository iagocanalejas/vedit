#!/usr/bin/env python3
import argparse
import logging
import os
import sys
from dataclasses import dataclass
from pathlib import Path

from vedit.audio import predict_start_delay, read_and_trim_audio
from vedit.models import AudioData, VideoData
from vscripts import NTSC_RATE, AudioStream, VideoStream, delay, extract

logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler(sys.stdout))


def main(config: "VEditConfig"):
    input_video = VideoData(stream=VideoStream.from_file(config.input_file))
    target_stream = VideoStream.from_file(config.target_file)

    if target_stream.avg_frame_rate != NTSC_RATE:
        # TODO: atempo-video + change target_video to the new file
        pass

    target_video = VideoData(stream=target_stream)

    input_audios = AudioStream.from_file(config.input_file)
    target_audios = AudioStream.from_file(config.input_file)

    assert len(input_audios) > 0, "no audio streams found in input file."
    assert len(target_audios) > 0, "no audio streams found in target file."

    sample_rate1, data1 = read_and_trim_audio(config.input_file)
    sample_rate2, data2 = read_and_trim_audio(config.target_file)

    sample_input_audio = AudioData(stream=input_audios[0], frame_rate=sample_rate1, sample=data1)
    target_audio = AudioData(stream=target_audios[0], frame_rate=sample_rate2, sample=data2)

    # print(predict_start_delay(sample_input_audio, target_audio))

    # from vedit.audio import _plot_waves
    # _plot_waves(sample_input_audio, target_audio)

    # for i, _ in enumerate(input_audios):
    #     extract(Path(config.input_file).absolute(), track=i)

    # print(input_video)
    # print("\n\n")
    # print(target_video)
    #
    # print(float(target_video.duration) / float(input_video.duration))


@dataclass
class VEditConfig:
    input_file: str
    target_file: str

    target_intro: float

    @classmethod
    def from_args(cls, params: argparse.Namespace) -> "VEditConfig":
        if not os.path.exists(params.input):
            raise FileNotFoundError(f"file not found: {params.input}")
        if not os.path.exists(params.target):
            raise FileNotFoundError(f"file not found: {params.target}")

        return VEditConfig(
            input_file=params.input,
            target_file=params.target,
            target_intro=params.intro,
        )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=str, help="input file to be handled.")
    parser.add_argument("target", type=str, help="target file to merge into.")

    parser.add_argument("-i", "--intro", type=float, default=0.0, help="time spent in the intro of the target stream.")

    config = VEditConfig.from_args(parser.parse_args())

    logger.info(f"{os.path.basename(__file__)}:: args -> {config.__dict__}")
    main(config)
