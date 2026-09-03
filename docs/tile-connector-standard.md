# Tile Connector Standard

This document will define the mechanical, electrical, and logical interface
between a tile and the OpenPaw hub or backplane.

## Goals

- Prevent incorrect orientation and unsafe insertion.
- Support tool-free replacement.
- Provide power, ground, and bidirectional communication.
- Permit capability discovery and hardware revision identification.
- Reserve room for future expansion without changing existing pin meanings.

## Specification status

Connector family, pinout, voltage, current limit, signaling, keying, retention,
and hot-plug behavior are not yet finalized. Prototype implementations must
document these values locally and must not claim standards compliance.

## Compatibility

The finalized standard will use semantic revisions. Breaking electrical or
mechanical changes require a new major revision; backwards-compatible
clarifications use a minor revision.
