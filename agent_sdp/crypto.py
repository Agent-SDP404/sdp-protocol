"""Domain-separated Ed25519 envelopes; keys are supplied by a trusted registry."""
import base64
import hashlib
import json

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

DOMAIN = b"agent-sdp/3.0/SDP-JSON-1\x00"


class ProtocolError(ValueError):
    def __init__(self, code):
        self.code = code
        super().__init__(code)


def check(condition, code):
    if not condition:
        raise ProtocolError(code)


def canonical(value):
    """Restricted JSON: integer-only numbers, sorted ASCII property names.

    Unicode values are escaped with ensure_ascii. This is SDP-JSON-1, NOT JCS.
    Floats, lone surrogates, non-ASCII field names and integers > 2**53-1 fail.
    """
    def walk(item):
        if item is None or type(item) is bool:
            return
        if type(item) is int:
            check(abs(item) <= 9007199254740991, "INVALID_NUMBER")
        elif isinstance(item, str):
            check(not any(0xD800 <= ord(c) <= 0xDFFF for c in item), "INVALID_UNICODE")
        elif isinstance(item, list):
            for child in item:
                walk(child)
        elif isinstance(item, dict):
            for key, child in item.items():
                check(isinstance(key, str) and key.isascii(), "INVALID_FIELD_NAME")
                walk(child)
        else:
            raise ProtocolError("INVALID_JSON_TYPE")
    walk(value)
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode("ascii")


def digest(value):
    return hashlib.sha256(canonical(value)).hexdigest()


def parse(text):
    def pairs(items):
        result = {}
        for key, value in items:
            check(key not in result, "DUPLICATE_FIELD")
            result[key] = value
        return result
    try:
        data = json.loads(text, object_pairs_hook=pairs)
        canonical(data)
        return data
    except (json.JSONDecodeError, UnicodeError) as error:
        raise ProtocolError("INVALID_JSON") from error


def key():
    return Ed25519PrivateKey.generate()


def sign(body, signers):
    message = DOMAIN + canonical(body)
    return {"body": body, "signatures": [
        {"signer": identity, "signature": base64.b64encode(secret.sign(message)).decode("ascii")}
        for identity, secret in sorted(signers.items())
    ]}


def verify(envelope, registry, required):
    check(isinstance(envelope, dict) and set(envelope) == {"body", "signatures"}, "INVALID_ENVELOPE")
    check(isinstance(envelope["signatures"], list), "INVALID_ENVELOPE")
    message = DOMAIN + canonical(envelope["body"])
    seen = set()
    for proof in envelope["signatures"]:
        check(isinstance(proof, dict) and set(proof) == {"signer", "signature"}, "INVALID_PROOF")
        identity = proof["signer"]
        check(isinstance(identity, str) and identity in registry and identity not in seen, "UNKNOWN_OR_DUPLICATE_SIGNER")
        try:
            signature = base64.b64decode(proof["signature"], validate=True)
            registry[identity].verify(signature, message)
        except (ValueError, TypeError, InvalidSignature) as error:
            raise ProtocolError("BAD_SIGNATURE") from error
        seen.add(identity)
    check(set(required) <= seen, "MISSING_SIGNATURE")
    return envelope["body"]
