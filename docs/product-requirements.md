# Product Requirements

Version: 0.1 draft

## Vision

OpenPaw is an open-source, modular communication platform for companion animals
built around a Raspberry Pi 5 hub and smart RP2040-powered hexagonal tiles.

## Product goals

- Provide modular, snap-together hexagonal tiles.
- Use an RP2040 microcontroller in every tile.
- Use a Raspberry Pi 5 as the local hub.
- Publish open hardware and software.
- Be straightforward to assemble, repair, and extend.
- Provide excellent build, usage, and contributor documentation.

## MVP scope

### Tile

The initial tile:

- Reads a pressure switch.
- Controls RGB LEDs.
- Reports button presses to the hub.
- Exposes a unique tile identifier.

### Hub

The initial hub:

- Discovers connected tiles automatically.
- Plays audio assigned to tile presses.
- Records usage history and analytics.
- Provides an API for the dashboard.
- Supports a Home Assistant integration after the core MVP is stable.

### Dashboard

The dashboard MVP allows a user to:

- Discover connected tiles.
- Rename tiles.
- Upload and assign audio.
- Assign LED colors.
- View usage history.

## Acceptance criteria

The MVP must:

- Detect a tile press in less than 50 ms.
- Begin audio playback in less than 100 ms after a detected press.
- Support connecting and removing tiles while the system is operating.
- Discover connected tiles without manual addressing.

Latency must be measured from the physical input transition. Press detection
ends when tile firmware recognizes the input; audio response ends when the hub
begins playback. Test conditions and results must be recorded with the
implementation.

## Initial backlog

- [ ] Create tile CAD.
- [ ] Build and characterize the pressure-switch prototype.
- [ ] Implement RP2040 tile firmware.
- [ ] Implement Raspberry Pi hub software.
- [ ] Implement the dashboard MVP.
- [ ] Document assembly, setup, operation, and extension workflows.

## Related specifications

- [Architecture](architecture.md)
- [Hardware specification](hardware-spec.md)
- [Prototype bill of materials](../hardware/bom/prototype-bom.md)
- [Tile connector standard](tile-connector-standard.md)
- [Communication protocol](communication-protocol.md)
- [Roadmap](roadmap.md)
