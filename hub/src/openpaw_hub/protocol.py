"""Experimental protocol-v0 JSON Lines decoder."""

from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any

MAX_FRAME_BYTES = 512
SUPPORTED_VERSION = 0
ALLOWED_TILE_TYPES = {"tile.hello", "tile.pressed", "tile.released"}


class ProtocolError(ValueError):
    """Raised when a transport frame violates protocol-v0 bounds."""


@dataclass(frozen=True, slots=True)
class TileMessage:
    version: int
    message_type: str
    tile_id: str
    sequence: int
    uptime_ms: int
    payload: dict[str, Any]


def decode_tile_frame(frame: bytes) -> TileMessage:
    """Validate one complete newline-terminated tile frame."""
    if not frame.endswith(b"\n"):
        raise ProtocolError("frame is not newline terminated")
    if len(frame) > MAX_FRAME_BYTES:
        raise ProtocolError("frame exceeds 512-byte prototype limit")
    try:
        raw = json.loads(frame)
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ProtocolError("frame is not valid UTF-8 JSON") from exc
    if not isinstance(raw, dict):
        raise ProtocolError("frame root must be an object")

    version = raw.get("v")
    if version != SUPPORTED_VERSION:
        raise ProtocolError(f"unsupported protocol version: {version!r}")
    message_type = raw.get("type")
    if message_type not in ALLOWED_TILE_TYPES:
        raise ProtocolError(f"unsupported tile message type: {message_type!r}")
    tile_id = raw.get("tile_id")
    if (
        not isinstance(tile_id, str)
        or not tile_id.strip()
        or len(tile_id.encode("utf-8")) > 64
    ):
        raise ProtocolError("tile_id must be a non-empty string of at most 64 bytes")
    sequence = raw.get("seq")
    uptime_ms = raw.get("uptime_ms")
    if isinstance(sequence, bool) or not isinstance(sequence, int) or sequence < 0:
        raise ProtocolError("seq must be a non-negative integer")
    if isinstance(uptime_ms, bool) or not isinstance(uptime_ms, int) or uptime_ms < 0:
        raise ProtocolError("uptime_ms must be a non-negative integer")

    return TileMessage(
        version=version,
        message_type=message_type,
        tile_id=tile_id,
        sequence=sequence,
        uptime_ms=uptime_ms,
        payload=raw,
    )
