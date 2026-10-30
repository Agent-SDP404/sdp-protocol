# Validation

Install [requirements.txt](../requirements.txt), then run:

```sh
python tools/check.py
```

The command runs documentation/legacy-fixture checks, reference-runtime unit tests and offline verification of the committed proof bundle.

## Reference-runtime tests

Tests exercise real Ed25519 verification, three-party acceptance, purpose/source/audience constraints, tampering, expiry, domain separation, durable replay after restart, conflicting replays, finite allowance, revocation, creation-right assignment, old-holder rejection, failed-adapter rollback, concurrent duplicate execution and NFT predecessor consent. These tests apply to the local profile only.

## Documentation and historical fixtures

`python tools/validate.py` checks local file links, the explicitly retained v1 mandate examples and 20 bounded legacy authority checks. Its small structural validator is not a general JSON Schema implementation. The v2 runtime instead uses jsonschema to validate its full envelope schema.

Local link checking excludes virtual environments and build outputs. External links and heading anchors are not validated automatically.

## Proof verification

`python -m agent_sdp404.verify_trace examples/traces/local-exchange.json` validates the four checked-in exchanges, including signatures, accepted terms, source integrity/policies, one-hop assignment evidence, acknowledgement bindings, receipt sequence and deterministic adapter outputs. The public keys are synthetic local identities, not independently attested real-world principals.

## Limits

There is no production audit, network conformance certification, actual payment, blockchain settlement or live-model execution in these checks. Source truth, legal rights, AI authorship, real-world delivery, malicious-operator resistance and distributed recovery require additional implementation and evidence. See [conformance](conformance.md).
