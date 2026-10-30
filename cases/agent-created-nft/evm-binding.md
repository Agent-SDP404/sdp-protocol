# NFT case: EVM binding notes

Proposed adapter requirements, not a deployed ABI or smart-contract implementation.

The adapter maps principal authorization to a wallet signature or explicit bounded delegation; work identity to a unique token reference; original bytes and metadata to immutable commitments; seat succession to authoritative predecessor/successor records; and mint entitlement consumption to a unique fulfilled order.

A mint permit must bind instance/network, verifying contract, order, recipient, content, policy, validity and signer identity/epoch as appropriate to the selected signing design. Service attestation and participant authority remain separate even when both are required for minting. Authorized relayers may submit transactions; possession of an administrator key alone is not principal delegation.

The implementation must define exact encoding, hashing and signed bytes. [EIP-712](https://eips.ethereum.org/EIPS/eip-712) can support typed signing, but applications still need replay protection. [ERC-721](https://eips.ethereum.org/EIPS/eip-721) describes token interfaces; it does not by itself supply private-context handling, personal-agent authority or succession semantics.

The adapter must check authoritative order consumption, recipient binding, content integrity, finality and inclusion. Generic token ownership and case-specific active inclusion are different facts. Restrictions on direct transfer belong to this case, not to general AGENT-SDP404.

Do not infer deployed conformance from these notes. Verifying a real adapter requires its source, deployment identity, runtime code, signed policy, transaction evidence and administrator-power disclosure.
