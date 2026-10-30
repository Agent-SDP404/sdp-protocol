# Application cases

Cases demonstrate the same protocol across different domains. They are illustrative designs unless explicitly identified otherwise. The NFT documents preserve the earlier application-focused draft; their domain invariants do not become global SDP requirements.

| Case | Private source | Outbound value | Authority that matters | Result/value return |
|---|---|---|---|---|
| Knowledge service | Approved professional notes | A scoped answer | Derive and disclose to the requester | Delivered answer and agreed compensation, if any |
| Intent matching | Preferences and constraints | A minimal matching request | Disclose selected constraints; no implicit purchase authority | Candidate matches, privately delivered |
| Agent collaboration | Approved task inputs | A bounded subtask | Delegate within shared allowance | Subtask result and attributable completion |
| [Agent-created tokens](agent-created-token/README.md) | Personal intent, community goals and approved project context | Token concept, creation plan and defined participation rights | Separately authorize creation, issuance, distribution and administration | Verified token identity, agreed allocations and execution receipts |
| [Creative issuance and succession](agent-created-nft/README.md) | Participant's accessible context | Original artwork and a scoped mint opportunity | Create, publish, mint, retrieve a credential, accept succession | New work, preserved predecessor and explicit lineage |

## Knowledge service

An agent reads permitted expertise and answers a counterparty's question. The answer is delivered under agreed use terms. The requester receives no general access to the principal's notes. A free exchange remains valid; payment is a separate optional settlement step. Feedback enters memory only if allowed.

## Intent matching

An agent derives a concise request from private preferences. It reveals necessary constraints to a matching service, receives candidate results and returns them to the principal. A match does not authorize a booking, payment or public profile. Those require their own permissions and agreement.

## Agent collaboration

A coordinating agent delegates a limited task to a named worker. The worker sees only necessary inputs, has narrower or equal authority and consumes the shared parent budget. It cannot gain permission to delegate again merely because it received a task.

## Agent-created tokens

The [agent-created token case](agent-created-token/README.md) extends this pattern to issuance. It explains how a personal agent turns context into a token concept, executes within a bounded creation mandate and returns the result to the agreed beneficiaries. Token balances, administrator roles and creation entitlements remain distinct rights.

## Profile authoring rule

Describe the principal, context, mandate, outbound representation, agreement, rights, recipients, execution evidence and feedback. Then add domain-specific objects. A profile should still be explainable without treating its local asset model as the protocol itself.

Structured synthetic scenarios are available in [examples/exchanges.json](../examples/exchanges.json).
