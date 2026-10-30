# SDP404-0004: Local signed exchange profile

Specification: 2.0.0 · Profile: `agent-sdp404/local-1` · Implementation maturity: alpha.

This profile is a concrete, bounded implementation of the general exchange model. It supports finite snapshots, zero-fee exchanges, local deterministic adapters, unused-right assignment and local revocation. It does not claim to implement every general-core extension.

## 1. Message types and schema

The normative envelope shape is defined in [wire.schema.json](../agent_sdp404/schemas/wire.schema.json):

```json
{
  "body": {
    "version": "agent-sdp404/2.0",
    "domain": "local:demo",
    "type": "agreement"
  },
  "signatures": [
    {"signer": "identity:example", "signature": "base64-encoded-ed25519-signature"}
  ]
}
```

This fragment illustrates framing only; an executable agreement requires all schema fields. Unknown envelope/body fields are rejected, except the explicitly extensible result output object. Signers are unique and must resolve in the verifier's trusted registry. Every supplied signature is verified.

| Body type | Required signatures | Meaning |
|---|---|---|
| `source` | Source controller | Snapshot, origin classification and applicable use/disclosure conditions |
| `mandate` | Execution principal | Agent, source IDs, capability, purpose, recipient and finite allowance |
| `agreement` | Principal + executing agent + recipient | Exact plan, source descriptor hashes, nonce and output destination |
| `assignment` | Principal + current agent + successor agent | Handoff of an unused right at a specific grant epoch |
| `revocation` | Principal | Stop new execution under one bound grant |
| `result` | Executing agent | Output and accepted-agreement commitment |
| `receipt` | Named local operator | Committed execution record, result binding and allocation |
| `acknowledgement` | Recipient | Receipt accepted by the recipient in the demo trace |

NFT succession also requires the predecessor owner's signature over the new agreement. An operator signature alone cannot substitute for any required party.

## 2. Canonical bytes and signatures

This profile uses **SDP404-JSON-1**, not RFC 8785/JCS. Its restricted input is JSON objects/arrays, strings, booleans, null and integers in `[-9007199254740991, 9007199254740991]`. Floats and lone Unicode surrogates are rejected. Property names must be ASCII and duplicate property names must be rejected before parsing into a map.

Canonicalization recursively sorts object property names in ascending ASCII order, preserves array order, emits no insignificant whitespace, represents integers in base 10 without leading zeros and serializes strings using Python `json.dumps(..., ensure_ascii=True)` escaping. Non-ASCII characters are escaped as lowercase hexadecimal `\u` sequences, using surrogate pairs for supplementary characters. Standard short escapes are used for backspace, tab, newline, form feed and carriage return; quotation marks and backslashes are escaped; forward slashes are not escaped. Implementations must match the [canonical vectors](../examples/wire-vectors.json).

Content digests are lowercase hexadecimal SHA-256 of canonical body/output bytes. Signature bytes are:

```text
UTF8("AGENT-SDP404/2.0/SDP404-JSON-1") || 0x00 || canonical(body)
```

Each signature is Ed25519 over those bytes, encoded in standard padded Base64. Keys come from a trusted identity registry and must not be accepted merely because an untrusted envelope supplies them. The demo's public registry is synthetic and self-contained; it establishes no external identity.

The profile fixes body version and domain, and binds grant/descriptor hashes into agreements. A signature does not authorize unrelated capabilities or prove data quality.

## 3. Source and task authority

A signed source descriptor contains `sourceId`, kind, controller, access classification, terms reference, payload hash, permitted principals, purposes, disclosure audiences and derive/disclose operations. `public` permits wildcard principals or audiences only when explicitly declared; it does not bypass purpose or operation checks. A terms reference is an attested policy reference, not proof of licensing rights.

A signed mandate names source IDs, one capability, recipient, purpose, validity and finite uses. Agreement source IDs must be distinct, be permitted by the mandate and match the supplied descriptor hashes. Payload keys must match exactly the sources supplied. Payload bytes must match each descriptor commitment.

Source-policy checks and task-authority checks are separate. The controller and execution principal need not be the same identity. Current local adapters derive and disclose a result, so both source operations and mandate operations must permit that path.

This profile handles finite synthetic snapshots. It does not implement streaming checkpoints, secret storage, public disclosure filtering or real source revocation feeds.

## 4. Acceptance and execution

An agreement binds `exchangeId`, `grantId`, `grantHash`, executing agent, principal, recipient, purpose, capability, sources, exact plan, nonce, expiration and any applied assignment hash. All required parties sign the same body. Changed terms require new signatures and a new exchange identity if a prior exchange already committed.

The verifier checks signatures, scope, source policies and integrity before executing. Under `BEGIN IMMEDIATE`, it checks current entitlement holder, revocation, expiration, remaining allowance and nonce. The local adapter effect, signed result, receipt, nonce and allowance consumption commit in one SQLite transaction.

```text
PROPOSED → ACCEPTED (required signatures present)
         → EXECUTING (local transaction)
         → DELIVERED (effect + result + receipt committed)
         → ACKNOWLEDGED (recipient signs receipt in trace)
```

Failed local execution rolls back the transaction. Acknowledgement is separate from runtime delivery and is not stored as part of the execution transaction. DELIVERED means the result is committed and returned to the local caller; remote receipt is not inferred.

## 5. Replay and recovery

An exact replay of the same signed agreement body and exchange ID returns the persisted response and consumes no additional allowance. A changed body under the same exchange ID fails with `IDEMPOTENCY_CONFLICT`. A principal/nonce pair cannot authorize a second exchange. A grant ID cannot be rebound to a different body.

Readback still verifies supplied signatures, scope and input integrity. It can return already delivered results after grant expiration or revocation because it does not create a new effect. It is not a new source access grant or a way to recall disclosed information. Real storage/API implementations must separately control who may retrieve retained responses.

The transaction provides local persistence and serialization, not distributed exactly-once execution. Network or blockchain adapters are outside local-1; ambiguous external outcomes require a separate durable reconciliation design before retry.

## 6. Assignment and revocation

Only unused grants can be assigned. An assignment binds the grant hash, current holder, successor, epoch, nonce and expiration. The successor must appear in the principal's approved `assignableAgents`. Principal, former holder and successor all sign.

The authoritative transaction changes holder, increments epoch and stores the assignment commitment without creating new allowance. New agreements must name the current holder and the applied assignment hash. The old holder's new execution fails. Exact replay of an already applied assignment returns its stored hash; it does not change the current holder again.

Revocation is principal-signed and serialized through the same store. It blocks new executions but does not erase receipts or reverse effects already committed. The runtime supports sequential unused-right handoffs; the published proof-bundle verifier intentionally supports only the demonstrated single handoff per grant. General delegation trees and cross-domain assignment remain outside this profile.

## 7. Adapter contract

- `data-summary`: accepts finite synthetic integer readings and produces count, sum and accepted unit. Values are bounded to one million in absolute magnitude; canonical integer limits still apply to aggregate outputs.
- `token-create`: stores a simulated token record. The sum of allocation amounts must equal supply; administration and all parameters are those in the accepted plan.
- `nft-create`: stores a simulated artifact. A first work needs an empty seat; succession needs the current predecessor and previous owner's acceptance. The old record retains its owner/content and becomes retired; the new work gets a new identity.

The profile's NFT transaction collapses creation and activation into a single local atomic step. It does not implement the application case's paid credential retrieval/redemption or an interval of externally funded pending creation. No claim of full deployed NFT-profile conformance follows from the simulation.

All local-1 exchanges have `maxChargeMinor = 0`. Nonzero economic settlement is rejected by schema. Neither model calls nor blockchain writes are hidden behind the word "simulation".

## 8. Errors and verification

| Error | Meaning |
|---|---|
| `SCHEMA_INVALID`, `WRONG_MESSAGE_TYPE` | Invalid message shape or message used in the wrong operation |
| `BAD_SIGNATURE`, `MISSING_SIGNATURE` | Authentication failed or required acceptance absent |
| `UNKNOWN_OR_DUPLICATE_SIGNER` | Untrusted identity or duplicate proof entry |
| `DOMAIN_MISMATCH`, `SCOPE_MISMATCH` | Domain, principal, recipient, purpose or capability mismatch |
| `GRANT_MISMATCH`, `GRANT_ID_CONFLICT` | Wrong grant commitment or attempted rebinding |
| `SOURCE_MISMATCH`, `SOURCE_INTEGRITY` | Descriptor/payload mismatch |
| `SOURCE_*_FORBIDDEN`, `OPERATION_FORBIDDEN` | Applicable source/task conditions do not permit execution |
| `EXPIRED_OR_EARLY`, `EXPIRED_AGREEMENT`, `EXPIRED_ASSIGNMENT` | Fresh authority required for a new action |
| `IDEMPOTENCY_CONFLICT`, `NONCE_REPLAY` | Conflicting repeated operation or nonce reuse |
| `ALLOWANCE_EXHAUSTED`, `ENTITLEMENT_ALREADY_USED` | Finite authority already consumed |
| `WRONG_ENTITLEMENT_HOLDER`, `STALE_ASSIGNMENT`, `ASSIGNMENT_FORBIDDEN` | Handoff or current-holder check failed |
| `REVOKED` | Principal has stopped new execution |
| `ALLOCATION_MISMATCH`, `STALE_PREDECESSOR` | Adapter plan conflicts with allowed local state |

These errors are local exception codes, not yet an HTTP status mapping. SQLite availability errors and process termination are operational failures; they must not be silently mapped to successful delivery.

See the [runtime](../agent_sdp404/engine.py), [tests](../tests/test_reference.py), [public trace](../examples/traces/local-exchange.json) and [enforcement matrix](../docs/conformance.md).
