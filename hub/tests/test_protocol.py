from __future__ import annotations

import unittest

from openpaw_hub.protocol import MAX_FRAME_BYTES, ProtocolError, decode_tile_frame


class ProtocolTests(unittest.TestCase):
    def test_decodes_valid_press(self) -> None:
        message = decode_tile_frame(
            b'{"v":0,"type":"tile.pressed","tile_id":"pico-a","seq":7,'
            b'"uptime_ms":42}\n'
        )

        self.assertEqual(message.tile_id, "pico-a")
        self.assertEqual(message.sequence, 7)

    def test_rejects_unsupported_version(self) -> None:
        with self.assertRaisesRegex(ProtocolError, "unsupported protocol version"):
            decode_tile_frame(
                b'{"v":1,"type":"tile.pressed","tile_id":"pico-a",'
                b'"seq":7,"uptime_ms":42}\n'
            )

    def test_rejects_oversized_frame(self) -> None:
        with self.assertRaisesRegex(ProtocolError, "exceeds"):
            decode_tile_frame(b"{" + b" " * MAX_FRAME_BYTES + b"}\n")


if __name__ == "__main__":
    unittest.main()
