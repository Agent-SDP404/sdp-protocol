"""Bounded documentation checks and illustrative authority tests; not a runtime."""
import copy
import json
import re
from datetime import datetime
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]


def require(condition, message):
    if not condition:
        raise ValueError(message)


def timestamp(value):
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    require(parsed.tzinfo is not None, "timestamp requires timezone")
    return parsed


def structural(value, schema, path="$"):
    """Only the schema keywords used by this repository; fail on unknown ones."""
    supported = {"$schema", "$id", "title", "description", "type", "required",
                 "properties", "additionalProperties", "items", "minItems",
                 "uniqueItems", "minLength", "minimum", "enum", "format"}
    require(not set(schema) - supported, f"{path}: unsupported schema keywords")
    types = schema.get("type")
    types = types if isinstance(types, list) else [types]
    matches = {
        "object": isinstance(value, dict), "array": isinstance(value, list),
        "string": isinstance(value, str), "integer": type(value) is int,
        "null": value is None,
    }
    require(any(matches.get(t, False) for t in types), f"{path}: wrong type")
    if "enum" in schema:
        require(value in schema["enum"], f"{path}: invalid enum")
    if isinstance(value, dict):
        require(set(schema.get("required", [])) <= value.keys(), f"{path}: missing field")
        props = schema.get("properties", {})
        if schema.get("additionalProperties") is False:
            require(not value.keys() - props.keys(), f"{path}: unexpected field")
        for key, item in value.items():
            if key in props:
                structural(item, props[key], path + "." + key)
    if isinstance(value, list):
        require(len(value) >= schema.get("minItems", 0), f"{path}: too few items")
        if schema.get("uniqueItems"):
            enc = [json.dumps(x, sort_keys=True) for x in value]
            require(len(set(enc)) == len(enc), f"{path}: duplicate item")
        for i, item in enumerate(value):
            structural(item, schema["items"], f"{path}[{i}]")
    if isinstance(value, str):
        require(len(value) >= schema.get("minLength", 0), f"{path}: short string")
        if schema.get("format") == "date-time":
            timestamp(value)
    if type(value) is int and "minimum" in schema:
        require(value >= schema["minimum"], f"{path}: below minimum")


def delegation(child, parent):
    """Structural attenuation only; does not authenticate either mandate."""
    require(child["delegation"]["parentMandateId"] == parent["id"], "wrong parent")
    require(child["agent"] in parent["delegation"]["allowedAgents"], "unapproved delegate")
    require("delegate" in parent["operations"], "delegation not permitted")
    for field in ("instance", "principal", "purpose"):
        require(child[field] == parent[field], "changed " + field)
    for field in ("audiences", "contextRefs", "capabilityRefs", "operations", "outputClasses"):
        require(set(child[field]) <= set(parent[field]), "expanded " + field)
    require(set(child["delegation"]["allowedAgents"]) <=
            set(parent["delegation"]["allowedAgents"]), "expanded delegates")
    require(timestamp(child["validFrom"]) >= timestamp(parent["validFrom"]), "early child")
    require(timestamp(child["expiresAt"]) <= timestamp(parent["expiresAt"]), "late child")
    require(child["limits"]["unit"] == parent["limits"]["unit"], "changed budget unit")
    for field in ("maxUses", "maxChargeMinor"):
        require(child["limits"][field] <= parent["limits"][field], "expanded " + field)


def authorize(mandates, mandate_id, request, usage, revoked=()):
    """Illustrative guard on trusted synthetic records, not a secure verifier.

    No signatures, persistent transactions, disclosure filtering or actual
    execution occur here. An operation consumes shared allowance at each parent.
    """
    chain, visited = [], set()
    current = mandate_id
    while current is not None:
        require(current not in visited, "delegation cycle")
        visited.add(current)
        grant = mandates[current]
        require(current not in revoked, "revoked mandate")
        if chain:
            delegation(chain[-1], grant)
        chain.append(grant)
        current = grant["delegation"]["parentMandateId"]
    leaf = chain[0]
    require(request["agent"] == leaf["agent"], "wrong agent")
    require(request["instance"] == leaf["instance"], "wrong instance")
    require(request["purpose"] == leaf["purpose"], "wrong purpose")
    require(request["operation"] in leaf["operations"], "unauthorized operation")
    require(request["audience"] in leaf["audiences"], "wrong audience")
    require(set(request["contextRefs"]) <= set(leaf["contextRefs"]), "context expansion")
    require(request["outputClass"] in leaf["outputClasses"], "output expansion")
    if request["operation"] in {"invoke", "assign"}:
        require(request["capabilityRef"] in leaf["capabilityRefs"], "capability expansion")
    require(request["previousOutcome"] != "UNKNOWN", "unreconciled operation")
    require(type(request["chargeMinor"]) is int and request["chargeMinor"] >= 0,
            "invalid charge")
    for grant in chain:
        require(timestamp(grant["validFrom"]) <= timestamp(request["at"]) <
                timestamp(grant["expiresAt"]), "outside validity")
        require(request["unit"] == grant["limits"]["unit"], "wrong budget unit")
        used, charged = usage.get(grant["id"], (0, 0))
        require(used + 1 <= grant["limits"]["maxUses"], "usage exhausted")
        require(charged + request["chargeMinor"] <= grant["limits"]["maxChargeMinor"],
                "budget exceeded")
    # Single-process illustration only. Real implementations need atomic storage.
    for grant in chain:
        used, charged = usage.get(grant["id"], (0, 0))
        usage[grant["id"]] = (used + 1, charged + request["chargeMinor"])


def request_for(grant):
    return {"agent": grant["agent"], "instance": grant["instance"],
            "purpose": grant["purpose"], "operation": "disclose",
            "audience": grant["audiences"][0], "contextRefs": grant["contextRefs"],
            "outputClass": grant["outputClasses"][0], "capabilityRef": "",
            "at": "2026-10-30T12:00:00Z", "chargeMinor": 0, "unit": "NONE",
            "previousOutcome": "NOT_STARTED"}


def rejects(fn, expected):
    try:
        fn()
    except ValueError as error:
        require(expected in str(error), f"unexpected failure: {error}")
    else:
        raise ValueError("negative case accepted: " + expected)


def main():
    schema = json.loads((ROOT / "schemas/legacy-v1/mandate.schema.json").read_text(encoding="utf-8"))
    items = json.loads((ROOT / "examples/legacy-v1/mandates.json").read_text(encoding="utf-8"))["mandates"]
    mandates = {item["id"]: item for item in items}
    require(len(mandates) == len(items), "duplicate mandate id")
    for item in items:
        structural(item, schema)
        require(timestamp(item["validFrom"]) < timestamp(item["expiresAt"]), "invalid period")
        parent = item["delegation"]["parentMandateId"]
        if parent:
            delegation(item, mandates[parent])
    exchanges = json.loads((ROOT / "examples/legacy-v1/exchanges.json").read_text(encoding="utf-8"))["exchanges"]
    require(len({x["id"] for x in exchanges}) == len(exchanges), "duplicate exchange id")
    for exchange in exchanges:
        grant = mandates[exchange["mandateId"]]
        require(exchange["representation"] in grant["outputClasses"], "unexpected representation")
        require(exchange["counterparty"] in grant["audiences"], "unapproved counterparty")
        require(exchange["allocation"]["beneficiary"] == exchange["resultRecipient"],
                "example recipient mismatch")
        require(exchange["allocation"]["chargeMinor"] == 0, "examples must be free")

    link_count = 0
    for file in ROOT.rglob("*.md"):
        if any(part in {".git", ".venv", "dist", "__pycache__"} for part in file.relative_to(ROOT).parts):
            continue
        for target in re.findall(r"\[[^\]\n]*\]\(([^)\n]+)\)", file.read_text(encoding="utf-8")):
            target = target.strip("<>")
            parsed = urlsplit(target)
            if parsed.scheme or not parsed.path:
                continue
            destination = (file.parent / unquote(parsed.path)).resolve()
            require(destination.is_relative_to(ROOT), f"link escapes repository: {file}: {target}")
            require(destination.is_file(), f"missing link: {file}: {target}")
            link_count += 1

    base = mandates["mandate:knowledge"]
    request = request_for(base)
    authorize(mandates, base["id"], request, {})
    cases = [
        ("agent", "agent:operator", "wrong agent"),
        ("instance", "example:other", "wrong instance"),
        ("purpose", "sell-profile", "wrong purpose"),
        ("operation", "remember", "unauthorized operation"),
        ("operation", "settle", "unauthorized operation"),
        ("audience", "public:anyone", "wrong audience"),
        ("contextRefs", ["context:all-chats"], "context expansion"),
        ("outputClass", "raw-notes", "output expansion"),
        ("at", "2026-11-01T00:00:00Z", "outside validity"),
        ("at", "2026-10-29T00:00:00Z", "outside validity"),
        ("previousOutcome", "UNKNOWN", "unreconciled operation"),
        ("chargeMinor", 1, "budget exceeded"),
        ("chargeMinor", -1, "invalid charge"),
        ("unit", "USDT", "wrong budget unit"),
    ]
    for field, value, reason in cases:
        altered = dict(request, **{field: value})
        rejects(lambda: authorize(mandates, base["id"], altered, {}), reason)
    rejects(lambda: authorize(mandates, base["id"], request, {}, [base["id"]]), "revoked")
    worker = mandates["mandate:worker"]
    worker_request = request_for(worker)
    usage = {"mandate:coordinator": (3, 0)}
    authorize(mandates, worker["id"], worker_request, usage)
    require(usage["mandate:coordinator"][0] == 4, "child did not consume parent allowance")
    rejects(lambda: authorize(mandates, worker["id"], worker_request, usage), "usage exhausted")
    rejects(lambda: authorize(mandates, worker["id"], worker_request, {}, ["mandate:coordinator"]),
            "revoked")
    expanded = copy.deepcopy(worker)
    expanded["operations"].append("settle")
    rejects(lambda: delegation(expanded, mandates["mandate:coordinator"]), "expanded operations")
    wrong_cap = dict(worker_request, operation="invoke", capabilityRef="capability:purchase")
    rejects(lambda: authorize(mandates, worker["id"], wrong_cap, {}), "capability expansion")
    malformed = copy.deepcopy(base)
    malformed["limits"]["maxUses"] = True
    rejects(lambda: structural(malformed, schema), "wrong type")
    require((ROOT / "cases/agent-created-nft/lifecycle.md").is_file(), "missing preserved case")
    print(f"PASS: {len(items)} legacy-v1 mandate structures; {len(exchanges)} scenario mappings; "
          f"{link_count} local links; 20 negative boundary checks; parent quota consumption.")
    print("Scope: structural examples and illustrative guards only; no signature, network, "
          "blockchain or production verification.")


if __name__ == "__main__":
    main()
