> Application profile, preserved from the initial NFT-focused draft. Its seats, one-output rules, retirement semantics and mint entitlements apply to this case only. They are not requirements of the general agent-sdp core. See [the general protocol](../../README.md).

# NFT-CASE-02: Authority, AI execution and mint entitlements

Status: application case in agent-sdp `3.0.0`. Normative vocabulary follows [NFT-CASE-01](lifecycle.md).

## 1. The AI application boundary

This application profile treats an agent as the executor of a participant-authorized creative workload. The agent is not merely an interface to a centrally pre-generated collection. It must interpret the permitted context, form a creative direction, execute a creation method and commit its original result.

The application defines a shared output grammar: media type, dimensions where relevant, integrity rules, safety constraints, optional form references and delivery requirements. The participant supplies bounded authorization. The agent determines the individual work within that scope.

Applications can use remote models, local models, agent-authored rendering or other declared creation runtimes. A profile MAY require capabilities and an aesthetic, but MUST NOT misrepresent tool independence if its implementation forces one proprietary provider.

## 2. Developer non-sovereignty

This is a protocol design principle, not a claim that developers lack all operational power.

**Implementing or administering an application does not itself authorize the developer to exercise a participant's creation or mint entitlement.**

| Capability | Participant | Participant's agent | Developer/operator |
|---|---|---|---|
| Authorize scope, recipient and spending | Own decision | Only within explicit delegation | Cannot substitute administrator approval |
| Select private context sources | Controls access | Uses permitted sources | Cannot require raw private history as public input |
| Decide personal creative direction | Delegates this decision | Autonomous within pinned rules | Cannot choose or replace it as an administrative action |
| Execute creation | Delegates | Runs permitted tool/runtime | Supplies infrastructure; cannot impersonate participant-agent execution |
| Commit original output | Authorizes workflow | Commits actual result | Verifies and persists; cannot swap the result |
| Exercise mint entitlement | Controls account authorization | Executes within that grant | May validate/sign a permit, not spend or mint as the participant without their authorization |
| Retrieve a succession capability | Explicit separate request | Executes selected-work request | Must enforce ownership and specific authorization |
| Bind an accepted claim to another recipient | Not through ordinary retry | Not through ordinary retry | Prohibited |
| Set common application rules | Chooses whether to participate | Reads pinned policy | Defines and publishes policy; no silent rewrite of accepted rights |
| Pause or exclude | Profile-dependent | Cannot invent authority | Only declared powers; actions must be observable |

A developer may participate through its own account under the same public rules. This is distinct from administrator-created inventory or exercising another person's entitlement.

## 3. Required separation of authorizations

NFT-AUTH-01: Authentication MUST prove account control or delegated identity; it MUST NOT implicitly authorize payment, credential disclosure or minting.

NFT-AUTH-02: Creation delegation MUST identify instance, recipient, scope, policy, permitted actions and economic limits. Its representation may be a session grant, wallet delegation or another profile-defined proof. The agent MUST preserve the evidence; an application's `requireConfirmation=false` flag is not participant consent.

NFT-AUTH-03: Payment authorization MUST bind payer, payee/contract, asset, amount, order and network. An unlimited token approval is not a requirement of agent-sdp.

NFT-AUTH-04: Mint authorization MUST bind the beneficiary, order, immutable content commitments, applicable policy and ledger domain. A protocol service's permit is a statement that conditions are met; participant authorization is independently required. Explicitly delegated relayers MAY submit when the adapter verifies beneficiary authority and the same bindings. The default observed application route is participant-wallet submission.

NFT-AUTH-05: Succession capability retrieval MUST be separately requested for a selected currently eligible work. Login or initial mint approval MUST NOT substitute for this request.

NFT-AUTH-06: Accepted recipient binding MUST survive failures and restarts. An operator MUST NOT rebind it for convenience or use another participant's agent to complete it.

NFT-AUTH-07: Agent tool observations MUST be described accurately. Self-reported execution or originality MUST NOT be represented as independently verified inference.

NFT-AUTH-08: Operator upgrades, signer rotation and inclusion administration MUST have disclosed scope. A claim that an action is technically impossible requires evidence of enforcement in the deployed authority, not just this specification's MUST NOT language.

## 4. AI execution contract

A conforming invocation has four logical inputs:

1. **Private context access:** participant-approved history or memory available to the agent. This remains outside public artifact data.
2. **Pinned policy:** output requirements, permitted tools, references, privacy rules and one-output semantics.
3. **Accepted entitlement:** order, recipient, seat and the permitted creation budget or fee conditions.
4. **Execution identity:** an attempt identifier and a recoverable record of the actual runtime invocation.

The output contains the original artifact bytes, public-safe metadata, their digests, the declared method and execution status. The method label is provenance information, not cryptographic proof that a particular model ran.

The agent MUST NOT invent biographical facts when context is sparse. It MAY create fictional symbols and scenes that do not assert private real-world events. It MUST NOT upload raw history, access tokens, wallet secrets, sensitive contact information or bearer capabilities as part of a direction, prompt log or artwork.

Creation is autonomous within an authorized task. This removes mandatory creative-brief questionnaires, draft selection and subjective redraw loops from the one-output profile. It does not remove wallet controls, spending limits or the participant's ability to stop future execution.

Stopping execution is distinct from cancelling an already funded entitlement. Applications MUST disclose whether any refund or cancellation exists. This profile does not invent one.

## 5. What the mint entitlement means

An entitlement starts as a conditional, scoped opportunity. It becomes FUNDED when the required settlement is accepted. After the agent commits and freezes valid content, the verifier can issue a content-bound mint permit. One successful mint and inclusion fulfills it.

```text
participation authorization
    → accepted entitlement
    → settlement/funding
    → agent-created content commitment
    → content-bound mint permit
    → participant-authorized mint
    → verified fulfillment
```

An entitlement is therefore not the same object as a mint signature. The former binds a recipient to a lifecycle before final artwork exists; the latter binds that lifecycle to its specific completed output. A permit expiry MUST NOT erase confirmed funding. A renewed permit must refer to the same frozen work and unfulfilled order.

## 6. Transfer of creation-and-mint rights

In the credential profile, the holder delegates the opportunity for the seat's next creation to an eligible recipient. The predecessor's completed entitlement is not reused. A **new successor entitlement** is established, linked to the same seat and predecessor.

The right being passed is the right to execute that next lifecycle. It does not pass the holder's memories, old image, previous signature or token ownership. Retrieval, accepted claim, settlement and fulfillment are distinct events with different effects.

The capability's bearer can request a claim; the verifier still checks eligibility and ownership conditions. Acceptance fixes the recipient and order. Settlement retires the predecessor and funds the successor. The new participant's agent must then create independently.

## 7. Enforcement matrix

| Guarantee | Suitable enforcement | Remaining trust |
|---|---|---|
| One fulfilled mint per order | Ledger uniqueness check and finalized proof | Adapter/finality correctness |
| No competing successor | Atomic compare-and-set and consumed capability commitment | Claim authority and cross-domain reconciliation |
| No output substitution | Content hashes bound into mint authorization | Correct agent-side comparison and wallet delegation |
| No developer spending as participant | Account signature or bounded delegation | Wallet/agent key security |
| No private-context publication | Client-side filtering and narrow interfaces | Agent/runtime behavior; hashes do not prove privacy |
| Genuine original AI execution | Declared runtime evidence; optional attestation | No mandatory independent AI-authorship proof in this application profile |
| Persistent access to work | Content addressing, pinning and independent replicas | Storage availability and retention policy |
| No arbitrary exclusion | Contract or governance constraints, where implemented | A service-only promise does not eliminate operator discretion |

A service can still refuse to sign or go offline even if it cannot mint for the participant. Implementers MUST describe censorship and availability assumptions. An adapter may add accountable denial records, redundant verifiers or an exit path, but these are extensions until specified and implemented.

## 8. Conformance evidence

For every AUTH requirement, an implementation SHOULD publish the enforcing component, verification procedure, administrator override conditions and negative test cases. A conforming report must distinguish on-chain checks, service-side checks, client checks and agent attestations. Treating all four as equally trustless is non-conforming documentation.
