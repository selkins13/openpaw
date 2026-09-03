"""Bounded event routing for the experimental hub."""

from __future__ import annotations

import asyncio
import logging
from dataclasses import dataclass
from pathlib import Path
from time import monotonic_ns
from typing import Protocol

from .config import HubConfig

LOGGER = logging.getLogger(__name__)


@dataclass(frozen=True, slots=True)
class TileEvent:
    tile_id: str
    event_type: str
    sequence: int
    tile_uptime_ms: int
    received_ns: int


class AudioPlayer(Protocol):
    def play(self, path: Path, required: bool) -> bool: ...


class EventRouter:
    def __init__(self, config: HubConfig, audio: AudioPlayer) -> None:
        self._config = config
        self._audio = audio
        self._last_sequence: dict[str, int] = {}

    def handle(self, event: TileEvent) -> None:
        previous = self._last_sequence.get(event.tile_id)
        if previous is not None and event.sequence <= previous:
            LOGGER.warning(
                "discarding duplicate or stale event tile=%s seq=%d",
                event.tile_id,
                event.sequence,
            )
            return
        self._last_sequence[event.tile_id] = event.sequence
        if event.event_type != "tile.pressed":
            return
        tile = self._config.tiles.get(event.tile_id)
        if tile is None:
            LOGGER.warning("press from unconfigured tile=%s", event.tile_id)
            return
        path = self._config.audio_path_for(event.tile_id)
        if path is None:
            if tile.audio_required:
                raise RuntimeError(
                    f"tile {event.tile_id!r} requires audio but has no assignment"
                )
            return
        self._audio.play(path, required=tile.audio_required)


async def consume_events(
    queue: asyncio.Queue[TileEvent],
    router: EventRouter,
) -> None:
    while True:
        event = await queue.get()
        try:
            router.handle(event)
        finally:
            queue.task_done()


async def mock_tile_source(
    queue: asyncio.Queue[TileEvent],
    tile_id: str,
    interval_s: float,
) -> None:
    sequence = 0
    started = monotonic_ns()
    while True:
        await asyncio.sleep(interval_s)
        sequence += 1
        await queue.put(
            TileEvent(
                tile_id=tile_id,
                event_type="tile.pressed",
                sequence=sequence,
                tile_uptime_ms=(monotonic_ns() - started) // 1_000_000,
                received_ns=monotonic_ns(),
            )
        )
