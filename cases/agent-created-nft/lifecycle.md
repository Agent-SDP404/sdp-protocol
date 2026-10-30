> Application profile, preserved from the initial NFT-focused draft. Its seats, one-output rules, retirement semantics and mint entitlements apply to this case only. They are not requirements of the general SDP core. See [the general protocol](../../README.md).

# NFT-CASE-01: Application lifecycle

| Field | Value |
|---|---|
| Status | Draft |
| Specification | `0.1.0-draft.1` |
| Owner of this specification | Silicon Dreamers Protocol |
| Date | 2026-10-30 |
| Scope | Chain-independent AI creation and seat succession |

## 1. Abstract

This application profile defines a lifecycle for participant-authorized, agent-created artifacts. A persistent seat identifies a position in an application. A scoped entitlement authorizes one participant's agent to create a work and that participant to mint the committed result. Succession assigns the next lifecycle to another participant while preserving predecessor content and seat identity.

The design separates creative autonomy, economic entitlement, token ownership and active inclusion. A work can remain owned after it has permanently retired from the application's active set. A new work can inherit the seat without inheriting the predecessor's private context, artifact or token identity.

## 2. Requirement language and conformance

Uppercase MUST, MUST NOT, SHOULD, SHOULD NOT and MAY express normative requirements as defined by [RFC 2119](https://www.rfc-editor.org/rfc/rfc2119) and [RFC 8174](https://www.rfc-editor.org/rfc/rfc8174). Lowercase words are ordinary prose.

A conforming implementation identifies its exact application-profile version, authority profile, ledger adapter and application policy. It MUST implement the mandatory lifecycle and [authority requirements](authority-and-ai.md). It MAY omit credential succession; if supported, it MUST declare and implement [NFT-CASE-03](credential-succession.md). A marketplace is a separate optional adapter, not a prerequisite for this application profile.

Conformance means satisfying stated rules with specified enforcement. Publication of a document, schema validation or a passing example trace does not establish deployment conformance.

## 3. Actors

| Actor | Responsibility |
|---|---|
| Participant | Authorizes a bounded lifecycle and controls the beneficiary account |
| Agent | Interprets authorized context, makes creative decisions and executes the permitted workflow |
| Developer | Authors application policy and implementation; receives no participant authority merely by doing so |
| Operator | Runs services; may also be the developer, but its powers remain separately classified |
| Policy verifier | Checks eligibility, commitments and permitted state transitions |
| Storage provider | Stores original bytes and returns retrieval evidence |
| Ledger adapter | Records minting, settlement and seat continuity with a declared finality rule |
| Indexer | Projects authoritative evidence into user-facing state |

One organization can operate several components. This does not collapse their authorization boundaries or establish independent verification.

## 4. Namespaces and data model

Identifiers are namespaced by an `instanceId` and are never interpreted as globally unique bare numbers. Profiles MUST define identifier encoding, collision handling, account representation and ledger namespace. Core examples use readable strings; they are not production addresses or secrets.

### 4.1 Seat

A seat contains:

- `seatId`: stable identity within an instance;
- `headWorkId`: the most recently activated work, or null before first activation;
- `activeWorkId`: the currently included work, or null;
- `pendingOrderId`: the one reserved genesis or succession order, or null;
- `revision`: a monotonically increasing concurrency guard;
- `phase`: EMPTY, RESERVED, ACTIVE, INACTIVE or SUCCESSION_PENDING.

`headWorkId` preserves lineage even when its work is retired and the successor is unfinished. It is an abstract projection, not a requirement that a particular contract use that storage layout.

### 4.2 Entitlement and order

An entitlement contains `entitlementId`, `seatId`, `recipient`, `orderId`, `kind`, `policyHash`, `predecessorWorkId`, `status` and settlement evidence when applicable. `kind` is GENESIS or SUCCESSION. A genesis entitlement has no predecessor.

The order is the durable execution record of that entitlement. It pins the creation policy, agent delegation, output specification, reference digests when used, generation attempt identity and content commitment. Ordinary restarts do not create a new entitlement or order.

Entitlement status is RESERVED, FUNDED or FULFILLED. FUNDED means the ledger adapter has accepted the required payment or an explicit zero-fee entitlement authorization. Zero price MUST NOT mean absent authorization.

The rights encoded are creation execution and mint eligibility for this lifecycle. They do not imply copyright, ownership of an AI model, access to another person's memories, a financial return or unconditional permanent inclusion.

### 4.3 Work

A work contains:

- `workId`, `seatId`, `orderId` and `entitlementId`;
- `generation`: zero for genesis, predecessor generation plus one for succession;
- `predecessorWorkId`: null for genesis;
- `participant`: the beneficiary of the creation;
- an artifact commitment and public metadata commitment;
- the pinned policy digest;
- a ledger token reference and finalized mint evidence;
- inclusion status: MINTED_PENDING, INCLUDED, EXCLUDED or RETIRED.

The work's identity, artifact bytes, metadata bytes, participant attribution and lineage MUST NOT be rewritten after commitment. Ownership and inclusion observations are mutable records kept outside that content commitment. EXCLUDED means administratively inactive under published policy; RETIRED means permanently superseded through settlement and MUST NOT be reversed by ordinary inclusion administration.

### 4.4 Content commitments

A profile MUST specify the digest algorithm and byte encoding for every commitment. A commitment to an image is over the original image bytes, not a thumbnail, decoded pixel buffer or gateway URL. A metadata commitment covers the exact published metadata bytes; a mutable HTTP URL alone is insufficient.

If signatures cover structured objects, the profile MUST define a deterministic encoding or established typed-data scheme. Implementations MUST NOT assume that arbitrary JSON serialization is canonical. The optional JSON manifest design uses [RFC 8785](https://www.rfc-editor.org/rfc/rfc8785); an EVM adapter can use [EIP-712](https://eips.ethereum.org/EIPS/eip-712).

Private source context is not part of public metadata. The protocol does not require a public digest of private conversations. Even a hash of low-entropy personal information can leak facts through guessing.

## 5. Mandatory invariants

| ID | Requirement |
|---|---|
| NFT-CORE-01 | A seat MUST have at most one INCLUDED work. |
| NFT-CORE-02 | At most one accepted pending order may reserve a seat's next generation. |
| NFT-CORE-03 | An accepted entitlement MUST bind one recipient, one seat and one order. |
| NFT-CORE-04 | Each entitlement MUST produce at most one fulfilled work and mint. |
| NFT-CORE-05 | A successor MUST use a new work identity and new mint identity, retain the seat, and reference the immediate predecessor. |
| NFT-CORE-06 | Succession MUST NOT edit or burn the predecessor as its means of replacing active participation. Its content and token remain. |
| NFT-CORE-07 | A RETIRED work MUST NOT become INCLUDED again. |
| NFT-CORE-08 | The recipient's agent MUST create the successor from the recipient's authorized context; a profile MUST prohibit reusing the predecessor as the successor output. |
| NFT-CORE-09 | Content, policy and recipient commitments MUST survive retries unchanged. |
| NFT-CORE-10 | UNKNOWN observations MUST NOT authorize another payment, creation attempt or mint. |
| NFT-CORE-11 | Settlement MUST establish retirement and successor entitlement atomically in its authoritative domain. |
| NFT-CORE-12 | Inclusion MUST require a finalized mint and verified public retrieval of the committed files. |
| NFT-CORE-13 | Administrator status MUST NOT bypass participant authorization or reassign a bound entitlement. |
| NFT-CORE-14 | No participant-private context or bearer capability may be included in public artifacts or logs. |

NFT-CORE-08 is a creation-policy requirement. A byte hash does not prove semantic originality, context fidelity or AI authorship. Implementations MUST state how much of that requirement is agent-attested versus independently checked.

## 6. Initial creation

1. **Preflight.** Resolve a valid instance manifest. Verify identity requirements, output capability, policy, ledger, signer and public storage availability. Do not create a paid draft during preflight.
2. **Authorize and reserve.** Obtain the participant's bounded authorization. Atomically reserve an available seat and create one durable order. The profile specifies whether an unfunded genesis reservation expires; funded rights cannot silently expire with the quote.
3. **Fund.** Verify payment or explicit free participation evidence against the same recipient and order. Mark the entitlement FUNDED. A quote refresh changes only an unaccepted quote, not confirmed funding.
4. **Commit direction.** The agent forms an original direction from permitted context and pins it to the order. Only the public-safe direction enters the service.
5. **Execute.** Run one permitted creation attempt. Save the actual tool invocation and its outcome. Record original output, metadata and commitments.
6. **Freeze.** Store original artifact and metadata bytes. Fully retrieve and verify them through the declared public-readback policy before freezing.
7. **Authorize mint.** Verify a mint permit bound to the recipient, order, policy and frozen content. Satisfy the participant's valid authorization; repeat wallet confirmation only when required by that authorization or the wallet.
8. **Mint and include.** Verify finality, identity and commitments; activate the work in the seat only after inclusion and retrieval checks succeed. Mark the entitlement FULFILLED exactly once.

Public content delivery concludes this lifecycle. It does not implicitly authorize credential retrieval, another payment or a marketplace action.

## 7. Succession

This application profile exposes an adapter operation that settles a successor entitlement for a specific predecessor. The credential route is defined in NFT-CASE-03. A future marketplace route must satisfy the same invariants and explicitly define consent, settlement and fees.

At settlement, the authoritative system MUST recheck that the predecessor remains eligible, belongs to the expected participant, matches the claimed seat and revision, and has no competing settled successor. Successful settlement permanently retires it, clears active inclusion and reserves the recipient's funded successor order in one atomic transition.

There is intentionally an interval between retirement and the successor's creation. During that interval, the seat has zero active works and one pending order. The already-settled entitlement persists through storage, model, service or ledger interruptions.

After the successor's own mint is finalized and verified, activation atomically sets `headWorkId` and `activeWorkId` to that new work, clears the pending order and fulfills the entitlement. The predecessor remains RETIRED and its ownership is not changed by this operation.

## 8. State and recovery

### Seat states

| Transition | Required evidence |
|---|---|
| EMPTY → RESERVED | Accepted genesis authorization and unique reservation |
| RESERVED → ACTIVE | Genesis mint finality, verified content and inclusion |
| ACTIVE → INACTIVE | Authorized exclusion under the pinned/disclosed inclusion policy |
| INACTIVE → ACTIVE | Authorized reinstatement of the same non-retired work |
| ACTIVE → SUCCESSION_PENDING | Atomic verified succession settlement |
| SUCCESSION_PENDING → ACTIVE | Successor finality, content verification and activation |

An unfunded genesis reservation MAY be released under its published expiry policy. This does not apply to an accepted succession claim in NFT-CASE-03 or any funded entitlement.

### Order checkpoints

```text
RESERVED → FUNDED → DIRECTION_COMMITTED → CREATING
  → OUTPUT_COMMITTED → ASSET_FROZEN → MINT_FINALIZED → INCLUDED
```

These are logical checkpoints, not a mandated single database enum. Implementations may store funding, generation, storage and mint statuses separately. FAILED and UNKNOWN are observations about an operation; they do not erase the durable checkpoint.

After an output exists, a conforming one-output profile MUST recover and reuse its bytes. An additional attempt is permitted only when the profile defines no-output recovery, evidence establishes terminal failure without output or established non-invocation, and the coordinator authorizes a fresh attempt ID on the same order. Missing logs alone do not establish non-invocation. Subjective dissatisfaction does not qualify.

An RPC timeout or absent transaction hash MUST trigger reconciliation of the original operation. Retries MUST reuse idempotency keys. The same key with a different payload MUST be rejected. There is no claim of exactly-once network delivery; the requirement is at-most-one economic fulfillment with idempotent recovery.

Profiles MUST define ledger finality and reorganization handling. Provisional events MUST NOT retire, activate or fulfill an entitlement in the final user-facing projection. An exceptional reorganization beyond the declared finality assumption requires incident reconciliation; an operator must not secretly remint or reassign a seat to hide it.

## 9. Abstract operations

| Operation | Minimum guard and result |
|---|---|
| `resolveInstance` | Signed/authenticated policy, version, expiry and enforcement map |
| `reserveGenesis` | Eligible authorized recipient; unique seat/order reservation |
| `confirmFunding` | Matching finalized funding proof or zero-fee authorization |
| `commitDirection` | FUNDED order; public-safe direction; immutable commitment |
| `startCreation` | Direction pinned; unique authorized attempt |
| `commitOutput` | Same attempt; original digests and metadata; no replacement |
| `freezeAssets` | Full readback matches committed bytes |
| `issueMintPermit` | Frozen content; exact recipient/order; fresh scoped authorization |
| `verifyMint` | Finalized ledger proof; matching content and beneficiary |
| `activateWork` | Finality/readback/inclusion satisfied; atomic seat update |
| `settleSuccession` | Eligible head; accepted recipient binding; atomic retirement and entitlement |
| `inspectOrder` | Authorized read; return durable checkpoint without duplicate effects |

These names define semantics, not deployed HTTP routes or Solidity selectors. Adapter implementations publish their own precise wire interfaces.

## 10. Profile requirements

Each profile MUST publish identity rules, authorization format, price/fee policy, storage and finality assumptions, concurrency authority, signer powers, administrator powers, upgrade behavior and exclusions. Every order MUST pin the applicable policy version. A new release MUST NOT silently change a funded order's recipient, original output, reference set or accepted charges.

A profile's number of seats and fee schedule are application policy. A transferable token standard is a ledger choice. Direct token movement MUST NOT bypass this profile's succession to change the active participant. Profiles must restrict such movement or invalidate active inclusion and expose the resulting discrepancy; they must not silently relabel an unchanged work as a newly created successor.

Read [security](../../docs/security.md), [AI authority](authority-and-ai.md) and the [EVM binding](evm-binding.md) before designing a conforming adapter.
