# Enforcement and conformance matrix

Specification version: 2.0.0. Local wire profile: `agent-sdp404/local-1`. Reference maturity: alpha.

| Claim | Status in this release | Evidence and limit |
|---|---|---|
| Multiple kinds of data sources | Implemented descriptor vocabulary | Source schema; source kind does not prove legality, truth or freshness |
| Source conditions separate from task authority | Implemented local checks | Controller-signed descriptors and principal-signed mandates |
| Principal, agent and recipient acceptance | Implemented Ed25519 verification | Trusted local key registry; not decentralized identity discovery |
| Concrete signed message encoding | Implemented | SDP404-JSON-1, domain separation, full envelope schema |
| Stable terms and input/output commitments | Implemented local checks | Hash and signature binding; deterministic fixtures |
| At-most-once local exchange effect | Implemented and tested | SQLite transaction, persisted response, unique exchange ID and nonce |
| Concurrent duplicate handling | Tested with two connections | Shared local database only; not distributed consensus |
| Assignment of unused creation rights | Implemented local handoff | Principal + former + new Agent signatures; no allowance copy |
| Revocation | Implemented local serialization | Stops new executions; exact readback of delivered results remains possible |
| General multi-hop delegation | Specification and legacy structural examples | Not implemented by local-1 runtime |
| Recipient acknowledgement | Signed and checked in demo bundle | Not a network delivery protocol; runtime returns before the caller creates acknowledgement |
| Receipt chaining | Implemented | Tamper detection relative to trusted prior records; no external transparency log |
| Agent-created token | Local simulation | Accepted plan, allocation check and administration record; no real token deployed |
| NFT succession | Local simulation | Prior-owner consent, new identity, retained predecessor; no paid credential lifecycle |
| Model/agent intelligence | Deterministic fixture processing | No real model call or AI-authorship proof |
| Payments, fees and financial settlement | Not implemented | local-1 explicitly requires zero charges |
| MCP / A2A network integration | Design mapping | No compatibility claim or network transport implementation |
| Arbitrary memory/device feedback | Specification only | No implicit state writes in the alpha |

Passing the included tests demonstrates the listed local behaviors. It does not certify a deployment against every requirement of the general core. A deployment must publish its profile, source controllers, identity trust, operational overrides, retention and adapter evidence.
