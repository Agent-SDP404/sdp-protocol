# Contributing

Keep the core application-neutral. New NFT, wallet, marketplace, model-provider or domain rules belong in a profile unless they are necessary for all exchanges.

For a normative change, describe the problem, affected objects and invariants, authorization consequences, privacy boundary, failure recovery and compatibility impact. Update examples and the changelog. Distinguish proposed behavior from implementation and deployment evidence.

Use synthetic identifiers and data. Never commit credentials, real personal context or wallet material. Run `python tools/validate.py` before submitting a change. This is a documentation draft, and its license has not yet been chosen; see [rights status](RIGHTS.md).
