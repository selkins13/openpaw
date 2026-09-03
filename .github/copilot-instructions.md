# OpenPaw Copilot Instructions

These instructions apply throughout the repository. Follow more specific
instructions when a subdirectory defines them. Treat approved specifications,
tests, and existing behavior as authoritative when they conflict with general
guidance here.

## Project context

OpenPaw is an open-source, modular communication platform for companion animals.
It uses a Raspberry Pi 5 hub and interchangeable RP2040-powered hexagonal tiles
with pressure input and RGB feedback.

Before changing product behavior or interfaces, review:

- `docs/product-requirements.md`
- `docs/architecture.md`
- `docs/hardware-spec.md`
- `docs/tile-connector-standard.md`
- `docs/communication-protocol.md`
- `docs/roadmap.md`

Do not invent product requirements, hardware constraints, protocol details, or
toolchain choices that these documents leave undecided.

## Engineering principles

- Keep hardware interfaces, transport, protocol, domain logic, audio, and user
  interfaces separated by explicit boundaries.
- Treat production tiles as interchangeable. Assign role, position, behavior,
  and user-facing identity through discovery and configuration rather than
  bespoke firmware or hardcoded physical IDs.
- Keep core operation local and functional without internet access or a closed
  cloud service.
- Favor common parts, open standards, portable formats, repairability, and
  reproducible builds.
- Prefer explicit, observable, and maintainable solutions over clever or
  implicit ones.
- Design for accessibility. Do not rely on color alone, and keep timing,
  sensitivity, brightness, volume, and feedback configurable where practical.

## Repository boundaries

Preserve the current top-level layout:

- `firmware/` contains tile firmware.
- `hub/` contains hub APIs, audio, and services.
- `dashboard/` contains the independent user interface.
- `hardware/` contains CAD, PCB, printable, and BOM sources.
- `docs/` contains requirements, specifications, and project guidance.
- `labels/` contains label artwork and sources.
- `examples/` contains reference configurations and integrations.
- `tests/` contains cross-component and system tests.

Keep component-specific tests close to their implementation. Use top-level
`tests/` for integration, hardware-in-the-loop, and system behavior. Do not add
new top-level directories or duplicate protocol definitions without an approved
architecture change.

## Reliability and performance

- Detect a physical tile press in less than 50 ms under documented normal
  operating conditions.
- Begin assigned audio playback in less than 100 ms after the physical press.
- Keep latency-critical paths non-blocking and bounded.
- Isolate and report a missing or faulty tile instead of disabling unrelated
  tiles or crashing the hub.
- Define timeouts, retries, queue limits, shutdown behavior, and recovery
  behavior explicitly.
- Use monotonic clocks for durations and latency measurements.

Record test setup, stage boundaries, sample count, and latency distributions
when validating performance targets.

## Protocol and configuration

- Treat the hub-to-tile protocol as a public compatibility boundary.
- Specify message versions, framing, field widths, units, limits, integrity
  checks, compatibility, and error behavior before implementation.
- Reject malformed, oversized, duplicated, stale, or unsupported input safely.
- Keep protocol fixtures shared so hub and firmware implementations cannot
  silently diverge.
- Never hardcode tile roles, layout positions, machine paths, ports, addresses,
  calibration values, or deployment-specific settings.
- Validate configuration with documented types, defaults, ranges, units, and
  migration behavior.

## Quality, safety, and privacy

- Add tests at the lowest useful level for behavior changes and regression
  tests for bug fixes when feasible.
- Keep tests deterministic; avoid arbitrary sleeps and external network
  dependencies.
- Update relevant documentation with behavior, hardware, configuration,
  protocol, setup, or API changes.
- Validate and bound all input from hardware, configuration, APIs, sockets, and
  removable media.
- Never commit credentials, personal data, or real deployment configuration.
- Minimize collected activity data and keep telemetry local and opt-in by
  default.
- Treat electrical, mechanical, animal, and human safety as correctness
  requirements. Fail safely on malformed commands, communication loss,
  brownouts, thermal faults, and stuck inputs.

When requirements remain ambiguous, preserve compatibility, make the smallest
reversible change, document the uncertainty, and ask before establishing a new
product or hardware requirement.
