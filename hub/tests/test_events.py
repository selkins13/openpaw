from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
from time import monotonic_ns

from openpaw_hub.config import AudioConfig, HubConfig, TileConfig
from openpaw_hub.events import EventRouter, TileEvent


class RecordingAudio:
    def __init__(self) -> None:
        self.calls: list[tuple[Path, bool]] = []

    def play(self, path: Path, required: bool) -> bool:
        self.calls.append((path, required))
        return True


class EventRouterTests(unittest.TestCase):
    def test_deduplicates_sequence_and_routes_assigned_audio(self) -> None:
        audio_dir = Path(self.enterContext(tempfile.TemporaryDirectory()))
        config = HubConfig(
            audio=AudioConfig(audio_dir),
            queue_size=2,
            shutdown_timeout_s=1,
            mock_interval_s=None,
            tiles={
                "tile-a": TileConfig(
                    label="Water",
                    audio_file=Path("water.wav"),
                    audio_required=True,
                    color=(1, 2, 3),
                )
            },
        )
        audio = RecordingAudio()
        router = EventRouter(config, audio)
        event = TileEvent("tile-a", "tile.pressed", 1, 10, monotonic_ns())

        router.handle(event)
        router.handle(event)

        self.assertEqual(
            audio.calls,
            [((audio_dir / "water.wav").resolve(), True)],
        )

    def test_required_tile_without_assignment_fails(self) -> None:
        config = HubConfig(
            audio=AudioConfig(Path("audio")),
            queue_size=2,
            shutdown_timeout_s=1,
            mock_interval_s=None,
            tiles={
                "tile-a": TileConfig(
                    label="Water",
                    audio_file=None,
                    audio_required=True,
                    color=(1, 2, 3),
                )
            },
        )
        router = EventRouter(config, RecordingAudio())

        with self.assertRaisesRegex(RuntimeError, "requires audio"):
            router.handle(
                TileEvent("tile-a", "tile.pressed", 1, 10, monotonic_ns())
            )


if __name__ == "__main__":
    unittest.main()
