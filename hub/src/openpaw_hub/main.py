"""OpenPaw Raspberry Pi hub prototype entry point."""

from __future__ import annotations

import argparse
import asyncio
import logging
import signal
from contextlib import suppress
from pathlib import Path

from .audio import AudioService
from .config import HubConfig, load_config
from .events import EventRouter, TileEvent, consume_events, mock_tile_source

LOGGER = logging.getLogger("openpaw.hub")


async def run(config: HubConfig, stop_event: asyncio.Event | None = None) -> None:
    """Run until stopped, then cancel and join all tasks within a fixed bound."""
    stop = stop_event or asyncio.Event()
    loop = asyncio.get_running_loop()
    if stop_event is None:
        for signal_number in (signal.SIGINT, signal.SIGTERM):
            with suppress(NotImplementedError):
                loop.add_signal_handler(signal_number, stop.set)

    queue: asyncio.Queue[TileEvent] = asyncio.Queue(maxsize=config.queue_size)
    audio = AudioService()
    audio.start(required=config.audio.required)
    try:
        for tile_id, tile in config.tiles.items():
            path = config.audio_path_for(tile_id)
            if path is not None:
                audio.preload(path, required=tile.audio_required)

        tasks = [
            asyncio.create_task(
                consume_events(queue, EventRouter(config, audio)),
                name="event-consumer",
            )
        ]
        if config.mock_interval_s is not None:
            if not config.tiles:
                raise ValueError("mock_interval_s requires at least one configured tile")
            tile_id = next(iter(config.tiles))
            tasks.append(
                asyncio.create_task(
                    mock_tile_source(queue, tile_id, config.mock_interval_s),
                    name="mock-tile",
                )
            )
        stop_task = asyncio.create_task(stop.wait(), name="shutdown-signal")
        done, _ = await asyncio.wait(
            [stop_task, *tasks],
            return_when=asyncio.FIRST_COMPLETED,
        )
        failed = [
            task
            for task in done
            if task is not stop_task
            and not task.cancelled()
            and task.exception() is not None
        ]
        if failed:
            raise RuntimeError(
                f"hub task {failed[0].get_name()!r} failed"
            ) from failed[0].exception()
    finally:
        active_tasks = [*locals().get("tasks", [])]
        if "stop_task" in locals():
            active_tasks.append(stop_task)
        for task in active_tasks:
            task.cancel()
        if active_tasks:
            try:
                async with asyncio.timeout(config.shutdown_timeout_s):
                    await asyncio.gather(*active_tasks, return_exceptions=True)
            except TimeoutError:
                pending = [task.get_name() for task in active_tasks if not task.done()]
                raise RuntimeError(
                    f"hub shutdown exceeded {config.shutdown_timeout_s}s: {pending}"
                )
        audio.close()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--config",
        required=True,
        type=Path,
        help="validated JSON configuration file",
    )
    parser.add_argument("--log-level", default="INFO")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    logging.basicConfig(
        level=getattr(logging, args.log_level.upper(), logging.INFO),
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )
    asyncio.run(run(load_config(args.config)))


if __name__ == "__main__":
    main()
