# Communication Protocol

The OpenPaw communication protocol carries discovery, events, commands, state,
and diagnostics between tiles and the hub.

## Message envelope

Every message is expected to include:

- Protocol version.
- Message type.
- Source and destination identifiers.
- Monotonic sequence number.
- Payload length and integrity information.

## Message classes

- **Discovery** announces identity, revision, and capabilities.
- **Event** reports user interaction or sensor input.
- **Command** requests a supported tile action.
- **State** reports current configuration or operating state.
- **Diagnostic** reports health, faults, and firmware information.

## Reliability and safety

Receivers must reject unsupported versions, malformed payloads, duplicate
commands, and commands outside declared capabilities. Timeouts, retries,
acknowledgements, transport framing, and wire encoding remain to be specified.

Protocol changes must include compatibility notes and representative test
vectors.
