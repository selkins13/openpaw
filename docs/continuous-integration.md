# Continuous Integration

OpenPaw enables CI gates only when the repository contains the implementation
and configuration needed for those gates to produce meaningful results. A
planned check must not report success without actually validating its
component.

## Active required check

`Repository checks` runs for every pull request to `main` and currently
validates:

- Required governance, specification, component, and ownership paths.
- UTF-8 Markdown, final newlines, and trailing whitespace.
- Local Markdown link targets.
- MIT, CERN-OHL-P-2.0, and CC-BY-4.0 license declarations.
- Repository-wide ownership by `@selkins13`.

The implementation is in `.github/scripts/check_repository.py`.

## Planned checks

| Check | Enable when | Required validation |
| --- | --- | --- |
| Hub | The hub has a dependency manifest and test configuration | Format, lint, type-check, and unit test |
| Firmware | The firmware build system and board target are committed | Format, warning-free build, and host unit test |
| Dashboard | The dashboard has a package manifest and test configuration | Lint, type-check, unit test, and production build |
| Protocol | Machine-readable schemas and shared fixtures exist | Schema validation and hub/firmware contract tests |
| Security | Supported source languages or dependency manifests exist | Code scanning and dependency review |
| Integration | Simulated hub and tile implementations exist | Discovery, presses, reconnects, malformed input, and audio dispatch |
| Hardware design | CAD or EDA sources and pinned tools exist | Electrical/design rules and reproducible exports |

Each check should have a stable job name, least-privilege permissions, a
timeout, deterministic inputs, and documented local commands. Run it
successfully on `main` before making it a required branch rule.

## Non-blocking and scheduled validation

Hardware-in-the-loop, endurance, manufacturing, and physical latency tests
depend on representative equipment. Keep them manually dispatched or scheduled
until a reliable runner is available. Release candidates should record:

- Press-detection and audio-response latency distributions.
- Tile hot-plug, discovery, fault isolation, and recovery behavior.
- Hardware revision, software versions, setup, and sample count.
