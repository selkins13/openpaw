# Architecture

OpenPaw uses a Raspberry Pi 5 as its local hub and RP2040-based hexagonal tiles
as its modular interaction surface. It consists of four primary layers:

1. **Tiles** provide a pressure switch and RGB LED feedback in each physical
   module.
2. **Tile firmware** reads the pressure switch, controls LEDs, identifies the
   tile, and reports button presses.
3. **The hub** discovers tiles, plays audio, records usage analytics, runs
   services and integrations, and exposes an API.
4. **The dashboard** configures the system and visualizes activity.

## Design principles

- Tiles should be replaceable without reconfiguring the entire system.
- Core interaction should continue when internet access is unavailable.
- Protocols and connectors should be documented and implementation-neutral.
- Hardware should favor safe, repairable, and commonly available components.
- Collected animal and household data should remain private by default.

## Data flow

A tile emits a typed event. The hub validates and timestamps the event, routes
it to local services, and publishes relevant state to API clients. Commands
flow in the reverse direction and must include a target tile and supported
capability.

Component boundaries and deployment diagrams will be refined as prototypes
are validated.
