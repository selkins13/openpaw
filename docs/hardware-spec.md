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
- A machine-readable identifier and hardware revision.
- Declared capabilities and power requirements.

## Environmental targets

Ingress protection, impact resistance, operating temperature, and cleaning
requirements remain prototype-dependent and must be recorded with each design.

## Source deliverables

Hardware contributions should include editable CAD or EDA sources, fabrication
exports, assembly notes, and an updated bill of materials.
