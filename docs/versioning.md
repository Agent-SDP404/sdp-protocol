# Versioning and migration

Current specification: [2.0.0](../VERSION). Reference implementation maturity: alpha. Tags use `vMAJOR.MINOR.PATCH`; a specification release does not imply a production-ready runtime.

- Major changes alter normative semantics or established wire formats incompatibly.
- Minor changes add compatible optional capabilities/profiles.
- Patch changes correct wording or defects without changing the declared protocol contract.

## From v1 to v2

The protocol is now named **AGENT-SDP404**. Its scope includes personal, organizational, public, research, device, environmental, agent-generated and composite data. A principal is an accountable authorizing identity, while a data source can have a separate controller.

V1 supplied abstract semantics and an illustrative `sdp/1.0` mandate envelope. V2 adds a concrete `agent-sdp404/2.0` signed local profile with source descriptors, accepted agreements and receipts. These are not compatible signing formats. Do not relabel old signed objects; obtain new authorization against the new semantics.

The [legacy v1 fixtures](../examples/legacy-v1/mandates.json) and [schema](../schemas/legacy-v1/mandate.schema.json) remain explicitly segregated. They are not runtime authorizations. The [v1.0.0 tag and release](https://github.com/Agent-SDP404/sdp-protocol/releases/tag/v1.0.0) remain unchanged, including their original name and scope.

The GitHub repository address remains `Agent-SDP404/sdp-protocol` to preserve published links. The repository is the protocol's primary reference; it does not designate an NFT project's site as a protocol website.

Published tags are not moved. Implementations declare both specification version and wire profile. No automatic compatibility is inferred from a shared brand name or major version.
