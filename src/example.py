from asciinema.recorder import record  # type:ignore
from asciinema.notifier import get_notifier  # type:ignore
from asciinema.asciicast.v2 import writer  # type:ignore
from audio import AudioRecorder  # type:ignore
from fs import ArchiveDir  # type:ignore
import os

# TODO: cli with a `record` command and params: filename, sr, ch, cols, rows

filename = "qux"
with ArchiveDir(filename) as path:
    audio = AudioRecorder(wav_file=f"{path}/.tmp.wav")
    with audio.record():
        record(
            f"{path}/cast.cast",
            writer=writer,
            notify=get_notifier(False, None),
            cols_override=80,
            rows_override=30,
        )
    with open(f"{path}/cast.cast") as f:
        *_, last_line = f
        first_word, *_ = last_line.strip("[]\n").split(", ")
        total_time = float(first_word)
    try:
        audio.trim_to(total_time)
    except RuntimeError as err:
        print(err)
    audio.save_as_ogg(f"{path}/audio.ogg")

    print(f"Duration: {int(audio.duration) // 60}m {audio.duration % 60:.3f}s")
