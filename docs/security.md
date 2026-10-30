# Security and trust model

The assets are private context, delegated authority, finite execution rights, committed results, accepted allocations and execution evidence. Adversaries can include malicious counterparties, compromised agents, dishonest services and administrators acting beyond their mandate.

| Threat | Required or recommended control | Residual limitation |
|---|---|---|
| Prompt injection in context/tool output | Separate data from instructions; enforce actions outside the model | Model-side instruction following alone is insufficient |
| Overbroad consent | Distinct access, derivation, disclosure, spending and memory permissions | Users can still knowingly grant broad scope |
| Hidden model-provider disclosure | Declare processor audiences and retention | Hosted providers may still observe permitted inputs |
| Sensitive inference | Minimize and assess derived outputs before delivery | Filtering cannot guarantee that no inference is possible |
| Forged or replayed mandate | Authenticated binding, exact signed scope, expiry, nonce and replay ledger | This repository does not implement cryptography |
| Duplicate delegated spending | Shared atomic parent/child allowance accounting | Distributed accounting requires defined consistency |
| Assignment double use | Atomic invalidation/grant or a declared locking protocol | Cross-domain finality and failures need reconciliation |
| Revocation race | Declared freshness and irreversible-action checkpoints | Revocation cannot recall disclosed information |
| Operator substitution | Commit terms/output; bind recipient and verify at execution | Operator may censor, pause or refuse service |
| Receipt correlation | Minimal metadata, opaque context handles and controlled access | Even metadata can identify behavior |
| Tool timeout | Reconcile stable operation ID before irreversible retry | External systems may lack idempotency support |
| Feedback poisoning | Separate memory permission; treat feedback as untrusted input | Retained misinformation can still degrade decisions |

## Enforcement disclosure

For each guarantee, publish the enforcing component, proof or test method, administrator override, dependency assumptions and failure behavior. Distinguish cryptographic checks, transactional server checks, client controls, agent attestations and policy promises.

A signature proves control of a signing key under a defined verification scheme; it does not establish the truth of every assertion. A content hash is not evidence of confidential handling. A ledger event establishes only the event semantics under the stated finality model.

## Domain-specific cases

A bearer succession credential can be stolen, copied or leaked through logs. The NFT case therefore requires secret handling, fresh authenticated retrieval, explicit recipient binding and authoritative single consumption. These controls address that case; they are not a reason to make bearer credentials mandatory for every SDP application.

## Reporting

Do not place private context, credentials, signing keys or exploitable live-system details in public issues. This project has no designated private security contact yet. A maintainer must establish a contact before deploying or presenting the repository as an operational service.
