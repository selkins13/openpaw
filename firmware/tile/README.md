# Experimental RP2040 tile firmware

This PlatformIO/Arduino prototype exercises one Velostat-and-copper-tape
pressure input and one WS2812B ring. It is not a finalized firmware toolchain,
pinout, electrical design, calibration, or communication standard.

The analog thresholds in `platformio.ini` are safe placeholders only. Measure
idle and pressed ADC distributions for the assembled tile, then set separate
press and release thresholds to retain hysteresis. The configured WS2812B data
pin also requires electrical validation, including logic-level compatibility,
power injection, current limiting, and a shared ground.

The development build derives a stable hardware identifier from the RP2040
chip ID. This identifier is not a user-facing role or label. Production
provisioning, replacement, privacy, and collision behavior remain unresolved;
deployment-specific tile roles must not be compiled into firmware.

Build with:

```shell
pio run --project-dir firmware/tile
```
