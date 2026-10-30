# Case: source-aware research exchange

An organization requests an aggregate from a research source controlled by another organization. This demonstrates an exchange without a person, NFT, token or payment as the central object.

## Input and agreement

The synthetic source contains readings `[12, 18, 24]`. Its controller signs the snapshot hash and permits the requesting principal to derive/disclose an aggregate for the stated purpose and audience. The principal authorizes its agent to execute `data-summary` once. Principal, agent and recipient accept the same unit, sources and exchange identity.

## Execution and output

The reference verifies both source and task authority, then produces `sampleCount: 3` and `sum: 54`. The Agent signs the result. The local operator commits a signed receipt with the accepted agreement hash and recipient allocation. The recipient checks the result and signs an acknowledgement.

Run:

```sh
python -m agent_sdp404.demo --output dist/demo-trace.json
python -m agent_sdp404.verify_trace dist/demo-trace.json
```

Inspect `exchange:research` in [the public trace](../../examples/traces/local-exchange.json).

## Failure behavior

Changing input bytes fails integrity verification. Changing the recipient or purpose fails scope verification. Replaying the same agreement returns the original receipt. Changing the unit under the same exchange ID fails with `IDEMPOTENCY_CONFLICT`. A new exchange cannot consume the single-use grant again.

## Extension boundary

Device observations, public datasets and environmental readings can use the same source descriptor model. Real sensors need source authentication/freshness, public datasets need their actual usage conditions, and streams need bounded checkpoints. The synthetic data and signed controller assertion do not establish real-world truth.
