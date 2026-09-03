from __future__ import annotations

import asyncio
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from openpaw_hub.audio import AudioService
from openpaw_hub.config import load_config
from openpaw_hub.main import run


class MainTests(unittest.IsolatedAsyncioTestCase):
    async def test_stops_within_configured_bound(self) -> None:
        directory = Path(self.enterContext(tempfile.TemporaryDirectory()))
        path = directory / "config.json"
        path.write_text(
            json.dumps(
                {
                    "audio": {"required": False},
                    "shutdown_timeout_s": 1,
                    "tiles": {},
                }
            ),
            encoding="utf-8",
        )
        stop = asyncio.Event()
        stop.set()

        with patch.object(AudioService, "start"):
            await asyncio.wait_for(run(load_config(path), stop), timeout=0.5)


if __name__ == "__main__":
    unittest.main()
