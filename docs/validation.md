# Validation

Run with Python 3.10 or later:

```sh
python tools/validate.py
```

No third-party packages are required. The script checks:

- The draft mandate envelope using the specific schema keywords present in this repository. Unsupported keywords fail explicitly; this is not a general JSON Schema implementation.
- Example exchange references, output classes, audiences and result recipients.
- Local Markdown file links. External availability and heading anchors are not checked.
- Rejection of wrong agents, instances, purposes, operations, audiences, context, output classes, validity windows, charges, units, revoked mandates and unreconciled outcomes.
- Parent/child scope attenuation, inherited revocation and shared parent quota consumption.
- Presence of the preserved NFT lifecycle case.

All records are synthetic. `example:NOT-A-SIGNATURE` references are placeholders, not authentication evidence. The illustrative guard assumes trusted records and in-process accounting; it is not an implementation to place in front of real personal data, wallets or services.

The checks do not verify signatures, deployment state, data confidentiality, AI authorship, truth of answers, assignment atomicity, durable idempotency, distributed concurrency, payment finality or actual service performance. Each requires an implementation and its own evidence before a deployment can claim conformance.
