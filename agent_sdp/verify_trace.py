"""Offline signature/binding verification and replay of the local simulation adapters."""
import argparse
import base64
from pathlib import Path
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey
from .crypto import check, digest, key, parse, verify
from .engine import Engine, validate, verify_delivery


def verify_trace(trace):
    registry = {name: Ed25519PublicKey.from_public_bytes(base64.b64decode(raw, validate=True))
                for name, raw in trace["publicKeys"].items()}
    previous = None
    seen = set()
    nonces = set()
    uses = {}
    grants = {}
    audit_key = key()
    replay = Engine(":memory:", {**registry, "verifier:local": audit_key.public_key()},
                    "verifier:local", audit_key, clock=lambda: trace["clock"])
    try:
        for index, record in enumerate(trace["exchanges"], 1):
            bundle, response = record["input"], record["output"]
            grant = validate(bundle["grant"], "mandate")
            verify(bundle["grant"], registry, [grant["principal"]])
            receipt = verify_delivery(response, bundle["agreement"], registry, "operator:local")
            agreed = bundle["agreement"]["body"]
            check(receipt["grantHash"] == digest(grant), "GRANT_MISMATCH")
            check(grant["domain"] == agreed["domain"] == "local:demo", "DOMAIN_MISMATCH")
            check(grant["notBefore"] <= trace["clock"] < agreed["expiresAt"] <= grant["expiresAt"], "EXPIRED_OR_EARLY")
            for field in ("principal", "recipient", "purpose", "capability"):
                check(agreed[field] == grant[field], "SCOPE_MISMATCH")
            check(agreed["grantId"] == grant["grantId"] and agreed["plan"]["kind"] == grant["capability"], "GRANT_MISMATCH")
            check({"derive", "disclose", "invoke"} <= set(grant["operations"]), "OPERATION_FORBIDDEN")
            identifier = grant["grantId"]
            check(identifier not in grants or grants[identifier] == digest(grant), "GRANT_ID_CONFLICT")
            grants[identifier] = digest(grant)
            uses[identifier] = uses.get(identifier, 0) + 1
            check(uses[identifier] <= grant["maxUses"], "ALLOWANCE_EXHAUSTED")
            nonce = (grant["principal"], agreed["nonce"])
            check(nonce not in nonces, "NONCE_REPLAY")
            nonces.add(nonce)
            if "assignment" in record:
                move = validate(record["assignment"], "assignment")
                verify(record["assignment"], registry, [grant["principal"], move["fromAgent"], move["toAgent"]])
                check(move["domain"] == grant["domain"] and move["grantId"] == identifier and
                      move["grantHash"] == digest(grant) and move["fromAgent"] == grant["agent"] and
                      move["toAgent"] == agreed["agent"] and move["toAgent"] in grant["assignableAgents"] and
                      move["epoch"] == 0 and trace["clock"] < move["expiresAt"] <= grant["expiresAt"] and
                      digest(move) == agreed["assignmentHash"] and uses[identifier] == 1, "ASSIGNMENT_BINDING")
            else:
                check(agreed["agent"] == grant["agent"] and agreed["assignmentHash"] is None, "WRONG_ENTITLEMENT_HOLDER")
            check(receipt["exchangeId"] not in seen, "DUPLICATE_EXCHANGE")
            seen.add(receipt["exchangeId"])
            check(receipt["sequence"] == index and receipt["previousReceiptHash"] == previous, "RECEIPT_CHAIN")
            check(len(bundle["sources"]) == len(agreed["sources"]), "SOURCE_MISMATCH")
            source_ids = []
            for source, reference in zip(bundle["sources"], agreed["sources"]):
                body = validate(source, "source")
                verify(source, registry, [body["controller"]])
                source_ids.append(body["sourceId"])
                check(body["domain"] == grant["domain"] and body["sourceId"] == reference["sourceId"] and
                      digest(body) == reference["descriptorHash"] and body["sourceId"] in grant["sourceIds"], "SOURCE_MISMATCH")
                check(body["payloadHash"] == digest(bundle["payloads"][body["sourceId"]]), "SOURCE_INTEGRITY")
                check(grant["principal"] in body["allowedPrincipals"] or
                      (body["access"] == "public" and "*" in body["allowedPrincipals"]), "SOURCE_PRINCIPAL_FORBIDDEN")
                check(grant["recipient"] in body["audiences"] or
                      (body["access"] == "public" and "*" in body["audiences"]), "SOURCE_AUDIENCE_FORBIDDEN")
                check(grant["purpose"] in body["allowedPurposes"] and
                      {"derive", "disclose"} <= set(body["allowedOperations"]), "SOURCE_OPERATION_FORBIDDEN")
            check(len(source_ids) == len(set(source_ids)) and set(source_ids) == set(bundle["payloads"]), "SOURCE_MISMATCH")
            check(replay._adapter(agreed, bundle["payloads"], bundle["agreement"]) == response["result"]["body"]["output"], "ADAPTER_OUTPUT_MISMATCH")
            ack = validate(record["acknowledgement"], "acknowledgement")
            verify(record["acknowledgement"], registry, [receipt["recipient"]])
            check(ack["receiptHash"] == digest(receipt) and ack["exchangeId"] == receipt["exchangeId"] and
                  ack["domain"] == receipt["domain"] and ack["recipient"] == receipt["recipient"], "ACKNOWLEDGEMENT_BINDING")
            previous = digest(receipt)
    finally:
        replay.close()
    return len(seen)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Check signatures, bindings, input integrity and receipt chain; does not prove actual external delivery or source truth.")
    parser.add_argument("trace")
    args = parser.parse_args()
    count = verify_trace(parse(Path(args.trace).read_text(encoding="utf-8")))
    print(f"PASS: {count} signed exchanges and recipient acknowledgements; receipt chain verified")
