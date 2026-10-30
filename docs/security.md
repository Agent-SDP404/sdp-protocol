# Security and trust boundaries

The assets are source data, execution authority, finite rights, accepted terms, results and evidence. Source controllers, task principals, Agent hosts, counterparties and operators may be different parties.

| Threat | Implemented local control | Remaining boundary |
|---|---|---|
| Forged authority or changed terms | Ed25519, schema, domain and scope checks | Registry key bindings must be trustworthy |
| Wrong source or substituted bytes | Signed descriptor and payload/descriptor hashes | Controller assertions do not prove ownership, truth or sensor authenticity |
| Unauthorized disclosure | Source audience/purpose checks plus task recipient binding | No semantic privacy filter; live model-provider disclosure needs its own adapter policy |
| Repeated execution | Persistent exchange identity, nonce and transactional consumption | Only local SQLite effects are atomic |
| Concurrent duplicates | BEGIN IMMEDIATE and uniqueness | No distributed consensus or cross-service atomicity |
| Creation-right duplication | Principal/current/new Agent signatures and serialized holder change | Database operator remains trusted |
| Revoked or expired new action | Checks under the ledger transaction | Delivered data cannot be recalled; exact result readback remains possible |
| Changed result or receipt | Agent/operator signatures and accepted-term bindings | Byte integrity is not usefulness or proof of AI authorship |
| Withheld or forked history | Hash-chained receipts and retained checkpoints | No public transparency log or operator-independent consensus |
| Prompt injection or poisoned sources | No model/tool prompt execution in the reference | Live Agent integration must enforce authority outside the model |
| Accidental memory/state write | No automatic feedback operation in local-1 | Other profiles must explicitly authorize writes |

## Key custody and source data

Demo identities and keys are generated in memory. The public trace contains only public keys, synthetic payloads and signed records. Never replace those inputs with real private data and publish the resulting bundle without checking disclosure rights.

The example SQLite ledger stores outputs in plaintext. Filesystem permissions, encryption, retention, secure deletion, real key custody and authenticated network transport are deployment responsibilities, not guarantees of this alpha. The operator can deny service or alter its database; valid signatures and retained receipts expose some changes but do not eliminate that trust.

Private-source commitments can leak guessable values. The public trace intentionally hashes synthetic data. Real profiles should use appropriate private storage, opaque references and disclosure controls rather than copy the demo's public-payload layout.

## Implementation limitations

The code is a small inspectable reference, not an audited authorization service. It has no network endpoint, real-world identity enrollment, live model provider, wallet, paid settlement or multi-tenant deployment hardening. The offline proof verifier accepts a bundle-supplied synthetic registry for demonstrations; production verification must anchor identities independently.

## Reporting

Use [GitHub Issues](https://github.com/Agent-SDP404/sdp-protocol/issues) for non-sensitive specification and reproducibility problems. A private security contact has not been established. Do not publish credentials, private inputs or exploit details affecting a live third-party deployment in a public issue.
