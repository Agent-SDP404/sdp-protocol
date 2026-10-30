# Engineering roadmap and open questions

This roadmap describes work, not dates, adoption claims or promised integrations.

## Available in 3.0.0

- General data-source model and independent protocol identity.
- A concrete signed local exchange profile and executable alpha.
- Research, NFT-succession and token-creation proof bundles.
- Assignment, revocation, persistent replay protection and local concurrency tests.

## Next implementation work

1. A network adapter with durable outbox, operation reconciliation and authenticated delivery.
2. A source-provider adapter that preserves usage conditions, updates, revocation and stream checkpoints.
3. Multi-hop delegation with shared budgets and explicit descendant revocation.
4. A real model adapter with reproducible execution evidence and controlled data disclosure.
5. A testnet asset adapter with finality/reorg handling and explicit separation from the local simulator.
6. Interoperability experiments mapping the profile onto MCP and A2A.

## Questions for contributors

- Which source-use conditions can be machine-checked, and which must remain attested?
- How should mutable streams and derived datasets preserve origin and usage restrictions?
- How can counterparties verify useful performance beyond byte integrity?
- What is the narrowest portable format for task authority across execution environments?
- Which guarantees survive when source controller, operator and recipient do not trust one another?
- How should paid obligations, cancellations and refunds compose with revocation?

Submit a [protocol proposal](../CONTRIBUTING.md) with a concrete message trace, affected authority and expected failure behavior. Improve a bounded interoperable path before broadening claims.
