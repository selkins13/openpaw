# Hardware Specification

This document defines baseline requirements shared by OpenPaw hardware.

## Safety

- Exposed surfaces must not have sharp edges or accessible pinch points.
- Materials reachable by an animal must be non-toxic and easy to clean.
- Cables, batteries, and small removable parts must be inaccessible in normal
  use.
- Designs must document voltage, current, thermal, and environmental limits.

## Tile requirements

Each tile must provide:

- A stable mechanical mounting interface.
- A connector compliant with the
  [tile connector standard](tile-connector-standard.md).
- An RP2040 microcontroller.
- A pressure switch and addressable RGB LED feedback.
- A machine-readable unique identifier and hardware revision.
- Declared capabilities and power requirements.

The Raspberry Pi 5 reference hub provides audio output through a MAX98357A
amplifier and 3 W speaker. See the
[prototype bill of materials](../hardware/bom/prototype-bom.md) for the initial
reference components.

## Performance targets

- Detect a tile press in less than 50 ms.
- Begin the assigned audio response in less than 100 ms after a press.
- Allow tiles to be connected and removed while the system is operating.
- Discover connected tiles automatically without manual addressing.

## Environmental targets

Ingress protection, impact resistance, operating temperature, and cleaning
requirements remain prototype-dependent and must be recorded with each design.

## Source deliverables

Hardware contributions should include editable CAD or EDA sources, fabrication
exports, assembly notes, and an updated bill of materials.
