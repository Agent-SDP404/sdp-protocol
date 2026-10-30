# SDP-0003: Exchange, rights and value allocation

Status: draft `0.2.0-draft.1`. Normative terms follow [the core](SDP-0001-core.md).

## 1. What can be exchanged

An SDP exchange may deliver information, a derived result, access to a capability, an executed action, a scoped entitlement or a collaboration outcome. Compensation is optional. The agreement MUST describe the actual thing provided and the rights granted, rather than treating all exchanges as ownership transfers.

The source context, derived representation, execution authority and economic benefit are separate. Acquiring one MUST NOT silently grant the others.

## 2. Rights vocabulary

| Right | Meaning | Required boundary |
|---|---|---|
| View | Inspect a specified result | Audience, duration and disclosure conditions |
| Use | Apply a result for a defined purpose | Permitted use, retention and onward sharing |
| Invoke | Request an operation from a capability | Inputs, operation scope, quota and budget |
| Delegate | Let another eligible agent execute a bounded part | Parent mandate, attenuation and shared accounting |
| Assign | Change the authorized recipient of an entitlement | Explicit assignability, acceptance and atomic invalidation |
| Consume | Exercise a finite right | Unique operation identity and authoritative decrement |
| Publish | Expose a result to a wider audience | Separate publication authority and content boundary |
| Settle | Allocate agreed benefits | Beneficiary, asset/unit, amount/limit and evidence |

Rights are protocol permissions. They do not automatically establish a legal copyright assignment, exclusive ownership or rights over third-party inputs.

## 3. Entitlements as optional objects

An entitlement expresses a particular right under conditions: issuer, beneficiary, capability, operation scope, quantity, expiry, assignment rules and consumption state. It can represent a service invocation, a task-execution opportunity, a creation allowance or a mint opportunity.

Applications MAY omit entitlement objects when a mandate and agreement suffice. They MUST use an authoritative consumption mechanism when they promise finite or exclusive exercise.

A new recipient MUST NOT gain private source context merely by receiving an entitlement. Context access requires independent authority. Assigning an entitlement does not mean assigning the principal-agent relationship itself.

## 4. Transfer and delegation

Before assignment, the verifier MUST check the current beneficiary, assignability, remaining allowance, recipient eligibility, agreement and authenticated acceptance. The authoritative handoff MUST invalidate the old beneficiary's ability to consume the assigned units at the same logical checkpoint that it grants the new beneficiary those units.

If atomic cross-system handoff is unavailable, the profile MUST specify locking, escrow or another reconciliation process and MUST NOT advertise unconditional atomicity. Two systems showing the same entitlement is not evidence that both may consume it.

Delegation leaves the parent relationship in place, creates narrower authority and consumes shared parent allowance. Assignment changes who may exercise a right. A successor entitlement is a new right linked to a predecessor. These three mechanisms MUST be labeled distinctly.

## 5. Value allocation

Before acceptance, an agreement MUST identify result recipients and any payment, credit, access or other benefit recipients. Where there is a charge, the asset/unit and maximum amount MUST be explicit. Where there is no charge, the record MUST say so rather than leave payment authority ambiguous.

The developer MAY receive an agreed service fee. It MUST NOT introduce one after acceptance without additional authorization, or redirect a participant's result or compensation through an administrative override.

Allocations can be asymmetric. A free answer can be a valid exchange, and a collaboration can provide reciprocal results without money. SDP does not assume that each party owns all inputs, that every output is scarce, or that all value can be priced.

## 6. Evidence, disputes and failure

A receipt MUST distinguish acceptance, reservation, execution, delivery and settlement evidence. A profile MUST define when performance is complete, what constitutes rejection, how disagreements are recorded and which party can resolve them.

An exchange can be delivered but unsettled, funded but unexecuted, or executed with delivery unknown. These conditions MUST NOT be collapsed into a single success flag.

The profile MUST state how unused reservations are released and how accepted obligations survive revocation, expiration, provider failure or cancellation. Revocation cannot by itself create a refund, erase a completed disclosure or silently reassign a funded right.

## 7. Worked examples

- A specialist's agent derives an answer from approved notes. The recipient can use the answer for one specified task but receives no access to the notes.
- A personal agent publishes a constrained request. A matching agent returns candidates; it receives no authority to purchase or publish the requester's identity.
- A coordinator delegates one analysis step to a worker. The worker consumes the parent's allowance and cannot independently subdelegate unless authorized.
- In the [NFT case](../cases/agent-created-nft/README.md), the new participant receives a successor creation-and-mint entitlement. This is an application-specific linked right, not a requirement that all SDP exchanges create tokens.
