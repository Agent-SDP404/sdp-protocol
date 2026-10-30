# Positioning and adjacent protocols

AGENT-SDP404 focuses on the relationship between source-use conditions, delegated execution, exchange terms, consumable rights and result evidence. Its design contribution is this combined lifecycle, not the invention of agent tools, authorization, messaging, cryptographic signatures or tokens.

## Complementary layers

| Layer | Existing role | AGENT-SDP404 focus |
|---|---|---|
| MCP | Tool/resource access; its HTTP authorization specification defines resource access flows | Carry source/task constraints and bind the permitted invocation to an exchange result |
| A2A | Agent discovery and interactions using tasks, messages and artifacts | Bind exchanged artifacts/actions to accepted terms, beneficiaries and execution rights |
| Token/ledger standards | Asset representation and ledger-specific operations | Describe the authority and conditions for issuance, transfer and outcome allocation |
| Cryptographic signatures | Authenticate bytes under a trusted key binding | Bind source descriptors, grants, agreements and receipts into one checkable record |

MCP already has authorization, and A2A already defines task and artifact behavior. AGENT-SDP404 does not claim those layers lack security or business semantics. The proposed integration boundary is a cross-layer exchange profile, which must be implemented and tested before compatibility is claimed.

## Concrete integration sketch

An MCP-backed source adapter could resolve a permitted dataset. The Agent could negotiate a task through A2A. The application would preserve the AGENT-SDP404 source commitment, mandate and accepted agreement across that task, then bind its artifact to a receipt. This is an architectural mapping, not a shipped integration in this release.

## Sources

- [MCP authorization specification](https://modelcontextprotocol.io/specification/draft/basic/authorization): HTTP transport authorization and resource-owner access.
- [A2A specification](https://a2a-protocol.org/latest/specification/): messages, tasks, artifacts and protocol operations.
- [Ed25519 API reference](https://cryptography.io/en/latest/hazmat/primitives/asymmetric/ed25519/): the library primitives used by this reference implementation.

The external `draft` and `latest` links are living sources, consulted on 2026-10-30. They are context, not normative dependencies pinned by AGENT-SDP404. No global novelty, audit, endorsement or interoperability certification is asserted.
