# Run and inspect a complete exchange

Use Python 3.10 or later. Creating an isolated environment is recommended:

```sh
python -m venv .venv
```

Activate `.venv` using your platform's normal procedure, then run:

```sh
python -m pip install -r requirements.txt
python -m agent_sdp404.demo --output dist/demo-trace.json
python -m agent_sdp404.verify_trace dist/demo-trace.json
python tools/check.py
```

The reference uses cryptography for Ed25519 and jsonschema for the full local wire envelope. The checked-in proof bundle can be verified without running the demo:

```sh
python -m agent_sdp404.verify_trace examples/traces/local-exchange.json
```

## Read the trace

The [public bundle](../examples/traces/local-exchange.json) contains four exchange records. Each includes signed source descriptors, a principal mandate, an agreement accepted by principal/agent/recipient, synthetic input data, an agent-signed result, an operator-signed receipt and recipient acknowledgement. The token record also contains the signed assignment of its creation entitlement.

The research example processes synthetic readings `[12, 18, 24]` into a count of `3` and sum of `54`. It returns no source credentials. It demonstrates an organization using research data, not a person selling private memory.

The demo repeats this exchange and receives the exact same receipt without consuming a second allowance. It then changes the accepted unit and correctly receives `IDEMPOTENCY_CONFLICT`.

The token simulation assigns one unused creation right to `agent:successor`, records the accepted 1,000-unit allocation and leaves administration with the plan's named principal. These values are synthetic demonstration parameters, not tokenomics recommendations or an existing asset.

The NFT simulation creates a predecessor and a new successor in the same seat. The previous owner signs the succession agreement. The old record stays owned by that owner and is marked retired; the successor has its own identifier and source-derived content commitment.

## What verification establishes

The offline verifier checks signatures against the bundle's public-key registry, accepted-term bindings, source policies and integrity, allowances represented in the bundle, acknowledgement bindings, receipt chaining and deterministic adapter outputs. Its trace format supports the demonstrated single handoff per grant; it is not a general multi-hop history reconciler.

The included keys are self-contained demonstration identities. Valid signatures do not establish a real-world identity, ownership of source data, truth of a sensor observation, genuine AI authorship, remote delivery or blockchain execution. Receipt chaining exposes changes relative to a retained checkpoint; it does not prevent a trusted operator from withholding history or starting a separate history.

Every demo run creates fresh keys in memory, so signatures vary. Private keys are never saved. The fixed demonstration clock makes example expiry behavior reproducible; it is not permission to execute expired grants in a live application.
