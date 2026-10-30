# Versioning and compatibility

The current specification release is recorded in [VERSION](../VERSION). Release tags use `vMAJOR.MINOR.PATCH`.

- **Major:** an incompatible change to normative semantics, required authority boundaries or an established versioned data envelope.
- **Minor:** a backward-compatible optional capability or profile addition that does not weaken existing requirements.
- **Patch:** editorial corrections and clarifications that do not change required behavior.

Implementations must declare the exact specification version and application/wire profiles they implement. A shared major version alone does not establish transport compatibility or deployment conformance.

The illustrative mandate envelope uses `sdp/1.0`. The transition from the pre-release `sdp/0.2-draft` label does not add execution authority. Examples in this repository use the released label; the local structural validator does not accept the previous label. Implementations handling old records must explicitly version and validate them rather than silently relabel signed data.

Application cases are included in the specification release but do not impose their domain-specific states on other applications. Example timestamps and synthetic identifiers are test fixtures, not currently valid execution authorizations.

Published release tags must not be moved. Corrections to a published release are made in a new version with a changelog entry. Repository publication, formal specification release, runtime implementation and deployment verification are distinct milestones.
