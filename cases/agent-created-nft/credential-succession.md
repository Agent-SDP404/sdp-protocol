# NFT-CASE-03: Credential-based succession

Application profile included in SDP 1.0.0. This document describes a specific succession design, not a generic SDP requirement or a verification of current service behavior. Normative terms apply only to this case.

## Four separate checkpoints

1. **Retrieve:** an eligible holder authorizes retrieval of a private succession credential for a selected work. Ordinary login is insufficient. Retrieval alone does not retire the work or transfer token ownership.
2. **Claim:** an eligible different participant submits the credential. Acceptance binds one recipient and one replacement order. The capability must not be accepted for competing recipients.
3. **Settle:** authoritative settlement checks eligibility again, consumes the capability, permanently retires the predecessor from active inclusion and funds/activates the linked successor entitlement in one atomic transition.
4. **Create and fulfill:** the recipient's agent uses the recipient's context to create a new artifact. Content verification, authorized mint and inclusion complete the successor lifecycle.

The seat can temporarily have no included work while the successor is pending. The predecessor's committed content and token ownership remain unchanged by this succession operation.

## Rights and authority

The passed opportunity is a new linked creation-and-mint entitlement. The predecessor's fulfilled entitlement, private memories and old mint signature are not reused. This is not general delegation of the former participant's agent.

Accepted binding is durable under this profile. Revoking an agent's future execution authority does not reassign the bound order or force the participant to continue. Recovery must obtain appropriate renewed authority while preserving settled entitlement and committed output.

## Credential handling and concurrency

Credentials MUST remain out of public logs, metadata and examples. Retrieval requires fresh, purpose-specific authorization. Claim binding and settlement consumption require authoritative concurrency control. Missing or delayed responses require reconciliation of the same order, not a new independent claim or payment.

The application must explicitly state rotation/revocation behavior, claim-window closure, eligibility and expiry. In this preserved design, retrieval returns a canonical bearer credential, accepted binding is not user-reassignable, new redemption closes when the designated market first opens, and already-funded orders retain completion rights. These are case policy, not core SDP rules.

A future market adapter must separately specify acceptance, settlement, fees and regeneration behavior. It cannot inherit those details merely from being called a marketplace.

See [lifecycle](lifecycle.md), [AI authority](authority-and-ai.md) and the generic [exchange/rights model](../../spec/SDP-0003-exchange-and-rights.md).
