# SDP-0002: Personal agents, autonomy and developer authority

Status: draft `0.2.0-draft.1`. Normative vocabulary follows [the core](SDP-0001-core.md).

## 1. User representation

A personal agent represents a principal through a mandate, not through a claim that it knows the principal. Hosting, model ownership and wallet ownership are separate implementation matters. The binding MUST identify both principal and agent and allow the relevant verifier to establish the scope and current validity of their relationship.

The agent can transform authorized context into a public-safe answer, creative expression, service, matching request or action. The principal need not manually specify each intermediate step when the mandate already covers it. Material expansion of purpose, disclosure, audience, cost or delegation requires additional authorization.

## 2. Autonomy inside a boundary

The agent MAY choose reasoning steps, tools, output structure and intermediate plans within policy. It MUST NOT treat creative or operational autonomy as authority to spend without limits, disclose all memories, select a different beneficiary, grant persistent access, or continue unrelated tasks.

Applications may be interactive, autonomous or mixed. A mandatory no-draft creative workflow belongs to a particular profile, not to all SDP applications. Likewise, a user may explicitly request review before disclosure or authorize automatic delivery within defined conditions.

## 3. Distinct authority classes

| Authority | What it permits | What it does not imply |
|---|---|---|
| Context access | Read selected sources for a defined purpose | Publication, sale or training on all source material |
| Derivation | Produce an inference, answer or artifact | Disclosure to every counterparty |
| Disclosure | Send allowed output classes to named audiences | Unlimited retention or onward sharing |
| Invocation | Use a capability or execute a task | Delegate that capability or spend beyond limits |
| Delegation | Assign a narrower subtask to an eligible agent | Expand scope or multiply allowance |
| Assignment | Move a defined consumable execution entitlement | Transfer the underlying data, token, copyright or all user authority |
| Settlement | Pay or allocate agreed benefits | Change beneficiary or accepted terms |
| Memory | Retain specified feedback in approved storage | Absorb untrusted instructions or third-party data without permission |

## 4. Developer non-sovereignty

A developer designs the application. An operator runs it. Neither role automatically carries the principal's authority.

AUTH-01: Administrators MUST NOT issue principal authorizations merely by changing internal database state. If a profile permits a guardian or recovery authority, it MUST describe that separate delegation and its activation conditions.

AUTH-02: Operators MUST NOT substitute their own preferred output for a committed principal-agent result or silently change its attributed author, intended recipient or usage conditions. Content moderation can prevent delivery under a disclosed policy; it cannot masquerade as the participant creating a different result.

AUTH-03: Service signatures MUST be distinguished from participant authority. A verifier can attest that conditions were checked without acquiring the power to spend, publish or execute for the principal.

AUTH-04: Developers MUST NOT reassign accepted benefits or consumable rights for operational convenience. Account recovery and rights succession require their own explicit procedures and authorization evidence.

AUTH-05: Actual powers to pause, censor, inspect logs, rotate keys, change policies, upgrade code or terminate service MUST be disclosed. A claim that an action is technically impossible requires deployed enforcement evidence.

AUTH-06: These restrictions MUST also apply when developer, agent host, verifier and settlement provider are the same organization. Combining roles increases shared trust; it does not remove the boundaries.

## 5. Private-context transformation

Agents SHOULD minimize outbound context. They MUST preserve source restrictions through tool calls and sub-agent delegation. Sending private context to a remote inference provider is itself a disclosure to that provider, even if the final output is public-safe.

A conforming profile must name or describe relevant processor audiences and their retention assumptions. Local execution, confidential computing or zero-knowledge techniques may reduce exposure, but none is required or implied by the core.

A derived result can reveal personal information without quoting a source. Profiles SHOULD assess inference and combination risks, not only exact text matches. Public hashes of private or predictable facts SHOULD be avoided. Training, cross-user memory and unrelated product analytics require explicit scope; they are not automatic consequences of using the service.

## 6. Delegation and assignment

A delegated mandate MUST identify its parent and have equal or narrower context scope, operations, output classes, purpose and audience constraints. Its time window cannot outlive the parent. The parent must explicitly permit the target agent or delegation class.

All children share the parent's authoritative consumption ledger. A child with a quota of one does not create a new unit in addition to the parent's quota. Revocation semantics MUST cover descendants and define the maximum propagation delay.

Assignment of a consumable entitlement differs from delegation. Assignment changes the authorized recipient under a signed/verified handoff and invalidates the old recipient's ability to consume the same entitlement. A profile that intentionally creates a successor entitlement must record predecessor and successor separately rather than pretending the same right was copied.

## 7. Evidence levels

Each reported assurance MUST be categorized:

- **Declared:** a policy or party assertion.
- **Agent-attested:** an execution record reported by the agent or its runtime.
- **Verifier-checked:** specified checks performed by an identified verifier under stated trust assumptions.
- **Externally established:** an independent signed receipt or consensus/finality result, to the extent that it actually proves the claim.

Content hashes establish byte integrity. They do not establish correctness, originality, private-context fidelity or genuine AI execution. Token ownership does not prove all-purpose user consent. A successful settlement does not prove task quality.

## 8. Revocation and irreversible actions

Principals MUST have the profile's declared way to stop future use of a mandate. The profile MUST specify authenticated revocation, propagation and freshness checks. Revocation cannot recall an already disclosed secret, undo a completed ledger operation or erase another party's legitimate receipt.

Applications MUST distinguish revoking future authority from cancelling accepted obligations, receiving a refund and deleting retained data. These have different conditions. No universal refund or erasure guarantee is created by this draft.

See [exchange rights](SDP-0003-exchange-and-rights.md) and [security](../docs/security.md).
