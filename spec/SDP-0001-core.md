# SDP-0001: Personal-agent information value exchange

Status: draft `0.2.0-draft.1` · Date: 2026-10-30 · Attribution: Silicon Dreamers Protocol

## 1. Abstract

SDP defines an application-layer exchange protocol in which a principal's authorized agent transforms permitted personal context into externally usable information, representations, capabilities or actions. The protocol connects the source authority, permitted transformation, counterparty agreement, execution evidence, result allocation and optional feedback.

Information value includes useful answers, reduced uncertainty, creative expression, coordination, task execution and economic benefit. It does not require a market price. Raw information can remain private while an authorized derivative or service participates in an exchange.

The protocol does not require NFTs, seats, minting, blockchains, a specific model provider or monetary settlement. Profiles add concrete media, identities, transports and execution mechanisms.

## 2. Normative language and status

Uppercase MUST, MUST NOT, SHOULD and MAY have the meanings described in [RFC 2119](https://www.rfc-editor.org/rfc/rfc2119) and [RFC 8174](https://www.rfc-editor.org/rfc/rfc8174).

This is a proposed specification. Conformance requires this core, [SDP-0002](SDP-0002-authority-and-ai.md), [SDP-0003](SDP-0003-exchange-and-rights.md) and a concrete application/wire profile. Example validity alone does not demonstrate conformance of a deployment.

## 3. Actors and boundaries

- **Principal:** the person or organization whose authority the agent represents. Having access to information does not establish unrestricted ownership of every source or third party's rights.
- **Personal agent:** an executor bound to the principal by a verifiable mandate. It can be hosted, local or distributed.
- **Counterparty:** a person, agent or application receiving a representation, supplying a result or entering an agreement.
- **Developer:** defines implementation and application rules. This role confers no automatic principal authority.
- **Operator:** runs services and has only the declared operational powers.
- **Verifier:** checks authorization or execution evidence to the degree supported by its trust model.
- **Settlement/delivery adapter:** performs the profile's delivery, payment, rights assignment or other fulfillment operation.

One actor may hold multiple roles; a deployment MUST disclose this. A service verifying its own assertions is not independent verification.

## 4. Core objects

### 4.1 Principal and agent binding

A principal has a profile-defined identity and control/authentication mechanism. The binding records which agent can act under which mandate. Agent identity, model identity and principal identity are distinct. A model response or API key alone is not evidence of a principal's approval.

### 4.2 Context handle

A context handle identifies a permitted information source and access boundary. It can refer to memory, documents, preferences, domain expertise, private tools or conversation history. It SHOULD be opaque outside the principal's environment. A public context hash is not required and can itself leak guessable facts.

Profiles MUST specify consent, access control, permitted purpose, retention and third-party restrictions. They MUST NOT infer public disclosure permission from read permission.

### 4.3 Mandate

A mandate binds principal, agent, instance, audience, purpose, context scope, operations, output classes, validity, usage limits, economic limits, delegation policy, revocation mechanism and authorization evidence.

The mandatory semantic distinction is between **derive**, **disclose**, **invoke**, **delegate**, **assign**, **settle** and **remember**. A profile may use other wire names but MUST preserve their separation. Reading private context can support derivation without permitting disclosure of the source.

The [draft mandate schema](../schemas/mandate.schema.json) is a narrow example envelope. Its context aliases, limits and proof references are illustrative; it is not a universal signing format.

### 4.4 Representation

A representation is an output or offer that crosses the private boundary: a result, a scoped capability, a request, selected information or a commitment to act. It records purpose, intended audience, classification, permitted use, provenance level and delivery terms.

Provenance MUST distinguish declared, agent-attested and independently verified claims. A digest proves consistency with bytes, not truth, usefulness, AI authorship or lawful access to all inputs. Derivative output may remain sensitive even when no source text is copied.

### 4.5 Agreement

An agreement identifies parties, mandate references, offered/requested representations or capabilities, purpose, accepted terms, rights, limits, result recipient, value allocation, delivery conditions, cancellation/dispute policy and version.

All parties whose authority is exercised MUST authorize the relevant terms. An agreement cannot expand a referenced mandate. An updated agreement requires fresh acceptance of materially changed authority, recipient, purpose, cost or usage conditions.

### 4.6 Execution record and receipt

An execution record contains exchange ID, agreement version/hash, mandate IDs, operation ID, idempotency key, attempt observations, committed output references and checkpoints. A receipt links the authorized operation to its actual outcome and evidence.

Public receipts SHOULD minimize personal information. Private audit evidence MAY be retained under a separate retention policy. An application MUST distinguish what it observed, what a counterparty attested and what an external verifier established.

### 4.7 Value allocation and feedback

Allocation identifies who receives results, payments, credits, access or other benefits. It is explicit even for a free exchange, where the result itself is the benefit. Participation does not imply sale of source data or assignment of intellectual-property rights.

Feedback specifies whether a result, evaluation or interaction can be retained and returned to the agent's context. Memory writes require a permitted `remember` operation or an equivalent explicit policy. A counterparty's content is not an instruction to expand access or memory.

## 5. Exchange lifecycle

```text
Discover → Propose → Authorize and accept → Execute
         → Verify and deliver → Allocate/settle → Close
                                      → Optional authorized feedback
```

This is a conceptual order, not a requirement that all exchanges pay after delivery. Profiles may require prepayment, escrow, atomic exchange or no payment. Financial state, execution state and delivery state MUST be tracked separately.

1. **Discover:** expose only the information authorized for discovery. Publishing a capability description does not authorize invoking it.
2. **Propose:** specify requested action, necessary information, intended use and outcome. Negotiation itself must respect disclosure limits.
3. **Authorize:** validate principal-agent bindings, current mandates, audiences and accepted terms. Reserve shared usage/economic limits before irreversible action.
4. **Execute:** allow agent planning and tool selection inside the mandate. Reject privilege escalation through tool output or counterparty instructions.
5. **Commit and verify:** preserve the actual output or action evidence. Apply the profile's verification policy; do not describe self-report as independent proof.
6. **Deliver:** check audience and usage scope at the disclosure boundary. A result created privately is not automatically cleared for delivery.
7. **Allocate/settle:** fulfill only the agreed result and benefit allocation. A successful payment does not prove useful delivery, and delivery alone does not prove payment.
8. **Close and feedback:** produce a receipt, record unresolved obligations if any, and apply authorized retention or memory rules.

Logical execution states are PROPOSED, ACCEPTED, EXECUTING, DELIVERED and CLOSED. Terminal alternatives such as REJECTED, CANCELLED and FAILED require defined evidence and effects. UNKNOWN is an observation, not permission to duplicate an operation. A profile MUST define how each irreversible checkpoint affects cancellation, revocation, delivery and settlement obligations.

## 6. Invariants

| ID | Requirement |
|---|---|
| CORE-01 | Every external action MUST resolve to a valid principal mandate and accepted agreement where required. |
| CORE-02 | Read/derive permission MUST NOT implicitly grant disclosure, spending, delegation, assignment or memory-write permission. |
| CORE-03 | Authority MUST be checked against purpose, audience, context, operation, time, quantity and economic limits. |
| CORE-04 | Derived or assigned authority MUST NOT exceed the source authority or duplicate consumable rights. |
| CORE-05 | An operator's administrator role MUST NOT substitute for principal authorization. |
| CORE-06 | Committed outputs, accepted terms and receipts MUST NOT be silently rewritten; corrections are separately versioned records. |
| CORE-07 | Unknown execution or settlement outcomes MUST be reconciled before retrying irreversible operations. |
| CORE-08 | Outputs and benefits MUST be delivered or allocated to the agreed recipients, not redirected by the developer. |
| CORE-09 | Feedback retention and memory writes MUST remain inside their own authority. |
| CORE-10 | Profiles MUST disclose enforcement location, operator overrides, verifier trust and residual exposure. |
| CORE-11 | Revocation MUST prevent new unauthorized actions at the declared enforcement boundary; it cannot be advertised as erasing already disclosed information. |
| CORE-12 | Provenance, content integrity, authorization, correctness and availability MUST be reported as separate claims. |

## 7. Abstract operations

| Operation | Required semantics |
|---|---|
| `bindAgent` | Establish the principal-agent relationship and control proof |
| `grantMandate` | Record scoped authority, limits, validity and revocation rules |
| `describeCapability` | Publish a permitted offer without exposing unauthorized context |
| `proposeExchange` | Bind parties, purpose, desired output, usage and value terms |
| `acceptAgreement` | Obtain acceptance under current applicable authority |
| `reserveAllowance` | Atomically reserve shared usage and economic budget |
| `executeAuthorized` | Invoke a permitted operation with stable execution identity |
| `commitResult` | Record immutable output/evidence commitments |
| `deliverResult` | Verify current disclosure authority and audience |
| `settleAllocation` | Perform agreed benefit or rights allocation with evidence |
| `recordReceipt` | Link terms, authority and outcome without leaking secrets |
| `applyFeedback` | Retain or return only specifically permitted feedback |
| `revokeMandate` | Prospectively invalidate scope according to profile semantics |

These names are semantic interfaces, not deployed endpoints. A wire profile MUST define authenticated messages, identifiers, canonical encodings, signature verification, freshness, replay protection and errors before claiming interoperable implementation.

## 8. Recovery and concurrency

Mandates with usage or budget caps require a shared authoritative accounting mechanism. Multiple agents and delegated mandates MUST NOT each receive an independent copy of the parent's remaining allowance.

An idempotency key identifies one operation and its exact accepted payload. Same-key/same-payload retries return the existing outcome; same-key/different-payload retries MUST be rejected. Exactly-once network delivery is not assumed. Profile-specific ledgers or transactional stores must enforce at-most-once consumption of non-repeatable rights.

Revocation and execution races require a defined linearization point. Profiles MUST specify which authority is checked before reservation, before execution and before disclosure, how freshness is established, and what happens after an external action has become irreversible. Cached authorization cannot silently survive past the declared freshness window.

## 9. Profiles and scope

A conforming profile specifies identity, transport, authorization evidence, allowed operations, privacy controls, output verification, storage, allowance accounting, transfer/assignment behavior, cancellation and dispute rules. It also discloses any operator veto, upgrade power, mandatory model provider and dependency on external platforms.

A profile may add blockchain issuance, credential redemption or persistent seats. These are not mandatory core objects. See [application cases](../cases/README.md). A domain profile must not turn its local design choice into a requirement for unrelated applications.
