# Contributing

Keep the core application-neutral. New NFT, wallet, marketplace, model-provider or domain rules belong in a profile unless they are necessary for all exchanges.

For a normative change, describe the problem, affected objects and invariants, authorization consequences, privacy boundary, failure recovery and compatibility impact. Update examples and the changelog. Distinguish proposed behavior from implementation and deployment evidence.

Use synthetic identifiers and data. Never commit credentials, private source data or wallet material. Install `requirements.txt`, then run `python tools/check.py` before submitting a change. Contributions intentionally submitted for inclusion are governed by Section 5 of the [Apache License 2.0](LICENSE), unless explicitly stated otherwise. Submit only material you are authorized to contribute. See [rights scope](RIGHTS.md) and [versioning](docs/versioning.md).
