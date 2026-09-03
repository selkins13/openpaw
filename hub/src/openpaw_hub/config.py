"""Validated configuration for the experimental OpenPaw hub."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any


class ConfigError(ValueError):
    """Raised when hub configuration is invalid."""


@dataclass(frozen=True, slots=True)
class AudioConfig:
    directory: Path
    required: bool = True


@dataclass(frozen=True, slots=True)
class TileConfig:
    label: str
    audio_file: Path | None
    audio_required: bool
    color: tuple[int, int, int]


@dataclass(frozen=True, slots=True)
class HubConfig:
    audio: AudioConfig
    queue_size: int
    shutdown_timeout_s: float
    mock_interval_s: float | None
    tiles: dict[str, TileConfig]

    def audio_path_for(self, tile_id: str) -> Path | None:
        tile = self.tiles.get(tile_id)
        if tile is None or tile.audio_file is None:
            return None
        root = self.audio.directory.resolve()
        candidate = (root / tile.audio_file).resolve()
        if not candidate.is_relative_to(root):
            raise ConfigError(f"audio file for {tile_id!r} escapes audio.directory")
        return candidate


def _mapping(value: Any, field: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ConfigError(f"{field} must be an object")
    return value


def _integer(value: Any, field: str, minimum: int, maximum: int) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        raise ConfigError(f"{field} must be an integer")
    if not minimum <= value <= maximum:
        raise ConfigError(f"{field} must be between {minimum} and {maximum}")
    return value


def _number(value: Any, field: str, minimum: float, maximum: float) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ConfigError(f"{field} must be a number")
    result = float(value)
    if not minimum <= result <= maximum:
        raise ConfigError(f"{field} must be between {minimum} and {maximum}")
    return result


def _boolean(value: Any, field: str) -> bool:
    if not isinstance(value, bool):
        raise ConfigError(f"{field} must be a boolean")
    return value


def _color(value: Any, field: str) -> tuple[int, int, int]:
    if not isinstance(value, list) or len(value) != 3:
        raise ConfigError(f"{field} must contain three RGB channels")
    return tuple(
        _integer(channel, f"{field}[{index}]", 0, 255)
        for index, channel in enumerate(value)
    )


def load_config(path: Path) -> HubConfig:
    """Load and validate a JSON configuration file."""
    try:
        document = json.loads(path.read_text(encoding="utf-8"))
    except OSError as exc:
        raise ConfigError(f"cannot read configuration {path}: {exc}") from exc
    except json.JSONDecodeError as exc:
        raise ConfigError(f"invalid JSON in {path}: {exc}") from exc

    root = _mapping(document, "configuration")
    allowed_root = {
        "audio",
        "queue_size",
        "shutdown_timeout_s",
        "mock_interval_s",
        "tiles",
    }
    unknown = set(root) - allowed_root
    if unknown:
        raise ConfigError(f"unknown configuration fields: {', '.join(sorted(unknown))}")

    audio_data = _mapping(root.get("audio", {}), "audio")
    audio_unknown = set(audio_data) - {"directory", "required"}
    if audio_unknown:
        raise ConfigError(f"unknown audio fields: {', '.join(sorted(audio_unknown))}")
    directory_value = audio_data.get("directory", "audio")
    if not isinstance(directory_value, str) or not directory_value.strip():
        raise ConfigError("audio.directory must be a non-empty string")
    audio_directory = Path(directory_value)
    if not audio_directory.is_absolute():
        audio_directory = path.parent / audio_directory
    audio = AudioConfig(
        directory=audio_directory,
        required=_boolean(audio_data.get("required", True), "audio.required"),
    )

    interval_value = root.get("mock_interval_s")
    mock_interval = (
        None
        if interval_value is None
        else _number(interval_value, "mock_interval_s", 0.01, 3600)
    )
    tile_data = _mapping(root.get("tiles", {}), "tiles")
    tiles: dict[str, TileConfig] = {}
    for tile_id, raw_tile in tile_data.items():
        if not isinstance(tile_id, str) or not tile_id.strip():
            raise ConfigError("tile identifiers must be non-empty strings")
        data = _mapping(raw_tile, f"tiles.{tile_id}")
        tile_unknown = set(data) - {
            "label",
            "audio_file",
            "audio_required",
            "color",
        }
        if tile_unknown:
            raise ConfigError(
                f"unknown fields for tile {tile_id!r}: "
                f"{', '.join(sorted(tile_unknown))}"
            )
        label = data.get("label", tile_id)
        if not isinstance(label, str) or not label.strip():
            raise ConfigError(f"tiles.{tile_id}.label must be a non-empty string")
        raw_audio_file = data.get("audio_file")
        if raw_audio_file is not None and (
            not isinstance(raw_audio_file, str) or not raw_audio_file.strip()
        ):
            raise ConfigError(
                f"tiles.{tile_id}.audio_file must be null or a non-empty string"
            )
        tiles[tile_id] = TileConfig(
            label=label,
            audio_file=Path(raw_audio_file) if raw_audio_file is not None else None,
            audio_required=_boolean(
                data.get("audio_required", True),
                f"tiles.{tile_id}.audio_required",
            ),
            color=_color(data.get("color", [32, 128, 255]), f"tiles.{tile_id}.color"),
        )

    return HubConfig(
        audio=audio,
        queue_size=_integer(root.get("queue_size", 256), "queue_size", 1, 4096),
        shutdown_timeout_s=_number(
            root.get("shutdown_timeout_s", 5),
            "shutdown_timeout_s",
            0.1,
            60,
        ),
        mock_interval_s=mock_interval,
        tiles=tiles,
    )
