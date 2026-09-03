from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from openpaw_hub.audio import AudioService, PlaybackError


class FakeSound:
    def __init__(self, channel: object | None = object()) -> None:
        self.channel = channel

    def play(self) -> object | None:
        return self.channel


class FakeMixer:
    def __init__(self, sound: FakeSound | None = None) -> None:
        self.sound = sound or FakeSound()
        self.closed = False

    def pre_init(self, **kwargs: object) -> None:
        pass

    def init(self) -> None:
        pass

    def Sound(self, path: Path) -> FakeSound:
        return self.sound

    def quit(self) -> None:
        self.closed = True


class AudioTests(unittest.TestCase):
    def test_required_missing_file_is_surfaced(self) -> None:
        service = AudioService(FakeMixer())
        service.start(required=True)

        with self.assertRaisesRegex(PlaybackError, "missing"):
            service.play(Path("/does/not/exist.wav"), required=True)

    def test_optional_missing_file_reports_not_played(self) -> None:
        service = AudioService(FakeMixer())
        service.start(required=True)

        self.assertFalse(service.play(Path("/does/not/exist.wav"), required=False))

    def test_no_channel_is_required_playback_failure(self) -> None:
        directory = Path(self.enterContext(tempfile.TemporaryDirectory()))
        path = directory / "sound.wav"
        path.touch()
        service = AudioService(FakeMixer(FakeSound(channel=None)))
        service.start(required=True)

        with self.assertRaisesRegex(PlaybackError, "no mixer channel"):
            service.play(path, required=True)


if __name__ == "__main__":
    unittest.main()
