# Application case: agent-created tokens

**An Agent turns permitted project data, organizational intent or community context into an authorized token creation and distribution plan.**

Status: illustrative agent-sdp application profile. This document describes a proposed workflow, not a deployed token, launch service or executable contract. It creates no requirement for other agent-sdp applications to issue tokens.

## Run the case

Run `python -m agent_sdp.demo --output dist/demo-trace.json` from the repository root after installing requirements. Inspect `exchange:token` in [the signed proof bundle](../../examples/traces/local-exchange.json).

The fixture begins with a principal-approved one-use creation mandate, then assigns it to a successor Agent with principal/current-agent/successor signatures. The agreement pins a synthetic 1,000-unit supply, exact allocations and named administrator. The local adapter verifies allocation totals, records the simulated token and commits a signed result/receipt. The recipient signs an acknowledgement.

This is a real signed exchange with a simulated issuance adapter. It performs no blockchain transaction. The failure suite covers missing handoff acceptance, execution by the old holder, reused allowance and allocation mismatch. See [local wire semantics](../../spec/SDP-0004-local-wire.md) and [tests](../../tests/test_reference.py).


## 1. From permitted data to a shared instrument

A person, organization or collective may have an idea, a dataset, a community, a body of work or a way of organizing shared effort. An authorized Agent can interpret that permitted context and express it as a token concept: what it represents, how it will be used, who can participate, and how issuance and control should work.

The agent's contribution is broader than filling in a name and symbol. It connects source information and intended use to a public expression and a set of executable rules. Within the user's mandate, it can develop the concept, prepare public metadata, select an allowed issuance template, propose distribution and execute an approved creation plan.

The token becomes an externally usable representation within an application. It may support participation, access, recognition or another explicitly defined coordination mechanism. Possessing the token does not automatically convey ownership of the principal's memories, identity, future work or agent.

**Permitted source data → agent interpretation → token concept → authorized creation → agreed distribution → participant interaction and feedback.**

Token creation is the issuance step. Exchange occurs when the resulting representation, access or participation rights are delivered and used under an agreement. Creating a token alone does not establish demand, economic value or fulfilled utility.

## 2. Mapping to agent-sdp

| agent-sdp object | Token-creation application |
|---|---|
| Principal | The person or organization authorizing the token initiative |
| Context | Approved intent, preferences, community information and project material |
| Mandate | Permission to design, disclose, deploy, distribute or administer within explicit limits |
| Representation | Token concept, public metadata, usage terms and executable creation plan |
| Agreement | Accepted issuance parameters, recipients, charges, control assignments and delivery conditions |
| Capability | A scoped ability to create a token, issue units, distribute units or manage a named function |
| Receipt | Creation identifier, network/domain, committed plan, execution evidence and actual control assignments |
| Allocation | Token balances, access rights and any agreed service compensation |
| Feedback | Authorized participation observations or results returned to the principal's agent |

An application can use a fungible token or another ledger-native unit. The general protocol does not prescribe a token standard, network, wallet, launchpad or payment asset.

## 3. A concrete user journey

Consider a principal who wants to coordinate a community around their creative practice. Their agent has permission to read selected project notes and community goals, but not private conversations belonging to other people.

1. **Interpret:** the agent derives a token concept from that permitted context. It explains the intended role and which proposed rights require application support.
2. **Prepare:** it produces a public name, symbol, description and creation plan. Private source material is not included merely because the agent used it during interpretation.
3. **Authorize:** the principal approves the concrete plan, or the agent verifies that an existing mandate already covers every material parameter. An open-ended request to brainstorm does not authorize deployment.
4. **Create:** the agent invokes an allowed creation capability with bounded transaction authority. It can submit through an explicitly authorized relayer; the transaction sender need not be the owner or beneficiary.
5. **Verify:** it checks the resulting token identity, supply, recipients and control assignments against the accepted plan, under the adapter's finality policy.
6. **Distribute:** it delivers units to the agreed recipients only if distribution is separately covered. A creation receipt alone does not prove that all distributions completed.
7. **Report and learn:** it returns an issuance receipt and records outstanding obligations. Any retained participant information or memory update remains subject to its own permission.

This can be an autonomous workflow when a sufficiently precise mandate already exists. Requiring authorization does not mean requiring a manual click for every intermediate action.

## 4. Separate the powers

| Power | What it permits | What it does not automatically permit |
|---|---|---|
| Design | Develop the concept and propose parameters | Deploy or spend |
| Publish | Disclose approved name, metadata and terms | Publish private context or participant identities |
| Create | Instantiate the approved token under the selected adapter | Create arbitrary additional tokens |
| Issue | Mint a bounded amount under an explicit supply policy | Unlimited future inflation |
| Distribute | Send specified units to agreed recipients | Redirect allocations or sell units |
| Administer | Exercise explicitly named post-creation controls | Implicit ownership of treasury, upgrades or all roles |
| Delegate or assign | Hand off a permitted issuance task or entitlement | Transfer personal context or duplicate an exclusive right |
| Market operations | Perform a separately authorized market action | Follow automatically from token creation |

Creating a token does not authorize selling it, adding liquidity, buying it, changing fees or promoting it through the user's accounts. Those are distinct actions with their own scope, budget and recipients.

## 5. The accepted creation plan

Before irreversible execution, the application must bind the plan to a stable agreement version or commitment. The plan identifies:

- Principal, authorized agent, instance and purpose.
- Network or ledger domain and the allowed creation mechanism or implementation identity.
- Public name, symbol, metadata and any relevant precision/unit representation.
- Initial supply, supply cap or explicitly permitted future issuance policy.
- Initial allocation recipients and amounts, including any treasury or escrow.
- Beneficiaries and assignments of issuance, upgrade, pause or other administrative powers; unsupported powers are explicitly absent.
- Transaction costs, service fees, payment assets, payees and maximum authorized spend.
- Creation operation ID, allowance consumption, expiry and recovery rules.
- Distribution conditions, permitted uses, delivery evidence and feedback retention.

These fields must have concrete values in an executable profile. A vague mandate such as “launch whatever works” is not a substitute for defining spending, disclosure and control boundaries.

If the agent changes a material term outside its existing discretion, it must obtain renewed authorization. The committed plan cannot be silently replaced after approval.

## 6. Developer non-sovereignty in issuance

The developer may supply templates, factories, interfaces and verification services. Providing the creation tool does not itself authorize the developer to:

- Allocate tokens or revenue to its own address beyond an accepted fee or allocation.
- Retain an undisclosed mint, freeze, upgrade or administrative role.
- Replace public content or issuance parameters after they have been committed.
- Exercise the user's deployment or distribution rights for another purpose.
- Treat the agent's private context as a reusable platform dataset.

If the implementation necessarily retains operator powers, the profile must disclose them before acceptance. An Agent deploying through a platform does not make that platform permissionless or remove its control over the implementation.

## 7. Creation rights can move without transferring source data

Suppose the principal authorizes one token-creation operation and delegates execution to a specialized issuance agent. The receiving agent gets the approved plan and bounded execution authority. It does not receive every source memory used to develop the concept.

Delegation preserves the principal's authority and shares the parent's allowance. Assignment of an exclusive creation entitlement changes who may consume it and must invalidate the former recipient's ability to consume the same right. Neither operation authorizes a second independent deployment.

After creation, transferring token balances, transferring an administrator role, and transferring an unconsumed creation entitlement remain distinct operations. A token holder does not automatically become the user's agent or acquire future issuance authority.

This is the generalized form of issuance-right transfer: **the right to perform a specified action moves under explicit conditions; source ownership and access to underlying data do not automatically move with it.**

## 8. Failure, recovery and evidence

If the creation request times out, the agent must inspect the original operation before retrying. It must not infer that no token exists merely because a response or transaction identifier is missing.

If creation succeeds but distribution fails, preserve the verified token identity and resume only the unfinished authorized distribution. Do not create a replacement token to conceal an incomplete launch. If deployed parameters or roles differ from the accepted plan, report the mismatch and stop further dependent actions until reconciled.

A completion report distinguishes plan acceptance, creation execution, finality, verified parameters, distribution, control assignments and unresolved obligations. Metadata or agent self-report alone cannot establish the deployed supply or actual administrative powers.

## 9. What this case demonstrates

The same agent-sdp chain can produce an answer, a creative work or a token-backed coordination mechanism. In each case, permitted data supplies context; the agent produces an outward representation; authorization constrains execution; and the result returns to the agreed beneficiaries.

Token issuance is one adapter for that chain. It does not redefine agent-sdp as a token-launch protocol.

See [the general core](../../spec/SDP-0001-core.md), [AI authority](../../spec/SDP-0002-agent-authority.md), [exchange and rights](../../spec/SDP-0003-exchange-rights.md) and [application cases](../README.md).
