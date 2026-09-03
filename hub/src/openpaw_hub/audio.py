"""Low-latency local audio service for OpenPaw."""

from __future__ import annotations

from pathlib import Path
from typing import Any


class AudioError(RuntimeError):
    """Base class for surfaced audio failures."""


class AudioUnavailableError(AudioError):
    """Raised when required audio cannot be initialized."""


class PlaybackError(AudioError):
    """Raised when assigned audio cannot be loaded or started."""


class AudioService:
    """Own the mixer and cache decoded sounds off the press event path."""

    def __init__(self, mixer: Any | None = None) -> None:
        self._mixer = mixer
        self._sounds: dict[Path, Any] = {}

    def start(self, required: bool) -> None:
        if self._mixer is None:
            try:
                from pygame import mixer
            except ImportError as exc:
                if required:
                    raise AudioUnavailableError(
                        "pygame is required for configured audio output"
                    ) from exc
                return
            self._mixer = mixer
        try:
            self._mixer.pre_init(
                frequency=44_100,
                size=-16,
                channels=2,
                buffer=256,
            )
            self._mixer.init()
        except (OSError, RuntimeError) as exc:
            self._mixer = None
            if required:
                raise AudioUnavailableError(
                    f"required audio output failed to initialize: {exc}"
                ) from exc

    def preload(self, path: Path, required: bool) -> None:
        self._load(path, required)

    def play(self, path: Path, required: bool) -> bool:
        sound = self._load(path, required)
        if sound is None:
            return False
        try:
            channel = sound.play()
        except (OSError, RuntimeError) as exc:
            if required:
                raise PlaybackError(f"required audio failed to start: {path}") from exc
            return False
        if channel is None:
            if required:
                raise PlaybackError(f"no mixer channel available for {path}")
            return False
        return True

    def close(self) -> None:
        if self._mixer is not None:
            self._mixer.quit()
        self._mixer = None
        self._sounds.clear()

    def _load(self, path: Path, required: bool) -> Any | None:
        resolved = path.resolve()
        if resolved in self._sounds:
            return self._sounds[resolved]
        if self._mixer is None:
            if required:
                raise AudioUnavailableError("required audio output is unavailable")
            return None
        if not resolved.is_file():
            if required:
                raise PlaybackError(f"required audio file is missing: {resolved}")
            return None
        try:
            sound = self._mixer.Sound(resolved)
        except (OSError, ValueError, RuntimeError) as exc:
            if required:
                raise PlaybackError(
                    f"required audio file cannot be decoded: {resolved}"
                ) from exc
            return None
        self._sounds[resolved] = sound
        return sound
