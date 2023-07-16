from dataclasses import dataclass
from contextlib import contextmanager
from typing import Callable, Generator, Any

from time import sleep

import soundfile as sf  # type:ignore
import sounddevice as sd  # type:ignore
import numpy as np  # type:ignore

import os

sd.default.device = "pipewire"  # edit


@dataclass()
class AudioRecorder:
    channels: int = 1
    sample_rate: int = 44100
    audio: np.ndarray = np.array([])
    wav_file: str = ""

    @contextmanager
    def record(self) -> Generator:
        with sf.SoundFile(self.wav_file, "w", self.sample_rate, self.channels) as file:

            def callback(indata: np.ndarray, frames, time, status):
                if status:
                    print(status)
                file.write(indata.copy())

            stream = sd.InputStream(
                samplerate=self.sample_rate,
                channels=self.channels,
                dtype=np.int16,
                callback=callback,
            )

            with stream:
                yield

        self.audio, _ = sf.read(self.wav_file)

    @property
    def duration(self) -> float:
        return self.audio.shape[0] / self.sample_rate

    def trim_to(self, time: float):
        difference = self.duration - time
        if difference < 0:
            raise RuntimeError(f"negative time difference: {difference}s")
        sec_to_frame = self.sample_rate
        frames_to_cut = int(sec_to_frame * difference)
        self.audio = self.audio[frames_to_cut // 2 : -frames_to_cut // 2]
        sf.write(self.wav_file, self.audio, self.sample_rate)

    def save_as_ogg(self, path: str, bitrate: int = 80) -> None:
        ret_code = os.system(
            f"ffmpeg -v error -i {self.wav_file} "
            f"-acodec libvorbis -b:a {bitrate}k {path}"
        )
        if ret_code != 0:
            raise RuntimeError(f"FFMPEG's return code: {ret_code}")
