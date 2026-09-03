from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from openpaw_hub.config import ConfigError, load_config


class ConfigTests(unittest.TestCase):
    def write_config(self, document: object) -> Path:
        directory = Path(self.enterContext(tempfile.TemporaryDirectory()))
        path = directory / "config.json"
        path.write_text(json.dumps(document), encoding="utf-8")
        return path

    def test_loads_relative_audio_directory_and_tile(self) -> None:
        path = self.write_config(
            {
                "audio": {"directory": "sounds", "required": False},
                "tiles": {
                    "tile-a": {
                        "label": "Water",
                        "audio_file": "water.wav",
                        "color": [1, 2, 3],
                    }
                },
            }
        )

        config = load_config(path)

        self.assertEqual(config.audio.directory, path.parent / "sounds")
        self.assertEqual(
            config.audio_path_for("tile-a"),
            (path.parent / "sounds" / "water.wav").resolve(),
        )

    def test_rejects_unknown_fields(self) -> None:
        path = self.write_config({"serial_port": "/dev/ttyACM0"})

        with self.assertRaisesRegex(ConfigError, "unknown configuration fields"):
            load_config(path)

    def test_rejects_audio_path_escape(self) -> None:
        path = self.write_config(
            {"tiles": {"tile-a": {"audio_file": "../outside.wav"}}}
        )

        with self.assertRaisesRegex(ConfigError, "escapes audio.directory"):
            load_config(path).audio_path_for("tile-a")


if __name__ == "__main__":
    unittest.main()
