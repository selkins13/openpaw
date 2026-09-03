# Architecture

OpenPaw consists of four primary layers:

1. **Tiles** provide physical controls, sensors, indicators, and audio input.
2. **Tile firmware** identifies hardware and exchanges events with the hub.
3. **The hub** discovers tiles, processes audio, runs services, and exposes an
   API.
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
