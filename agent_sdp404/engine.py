"""Local signed exchanges. All adapter effects commit in one SQLite transaction.

No network adapters, model calls, wallets, payments or blockchain writes.
The store and verifier are trusted; signatures do not remove operator custody.
"""
import json
import sqlite3
import time
from pathlib import Path

from jsonschema import Draft202012Validator
from .crypto import ProtocolError, canonical, check, digest, sign, verify

VERSION = "agent-sdp404/2.0"
SCHEMA = json.loads((Path(__file__).parent / "schemas/wire.schema.json").read_text(encoding="utf-8"))
VALIDATOR = Draft202012Validator(SCHEMA)


def validate(envelope, kind):
    check(not list(VALIDATOR.iter_errors(envelope)), "SCHEMA_INVALID")
    check(envelope["body"]["type"] == kind, "WRONG_MESSAGE_TYPE")
    return envelope["body"]


class Engine:
    def __init__(self, database, registry, operator_id, operator_key, domain="local:demo", clock=time.time):
        self.registry, self.operator_id, self.operator_key = registry, operator_id, operator_key
        self.domain, self.clock = domain, clock
        check(operator_id in registry and registry[operator_id].public_bytes_raw() ==
              operator_key.public_key().public_bytes_raw(), "OPERATOR_KEY_MISMATCH")
        self.db = sqlite3.connect(database, isolation_level=None, timeout=10)
        self.db.row_factory = sqlite3.Row
        self.db.executescript("""
        CREATE TABLE IF NOT EXISTS grants(
          id TEXT PRIMARY KEY, hash TEXT NOT NULL, agent TEXT NOT NULL,
          uses INTEGER NOT NULL DEFAULT 0, epoch INTEGER NOT NULL DEFAULT 0,
          assignment_hash TEXT, revoked INTEGER NOT NULL DEFAULT 0);
        CREATE TABLE IF NOT EXISTS exchanges(
          id TEXT PRIMARY KEY, request_hash TEXT NOT NULL, response TEXT NOT NULL,
          receipt_hash TEXT NOT NULL, sequence INTEGER UNIQUE NOT NULL);
        CREATE TABLE IF NOT EXISTS nonces(
          principal TEXT NOT NULL, nonce TEXT NOT NULL, exchange_id TEXT NOT NULL,
          PRIMARY KEY(principal, nonce));
        CREATE TABLE IF NOT EXISTS assignments(hash TEXT PRIMARY KEY, grant_id TEXT NOT NULL);
        CREATE TABLE IF NOT EXISTS assets(id TEXT PRIMARY KEY, kind TEXT NOT NULL,
          owner TEXT NOT NULL, content TEXT NOT NULL, retired INTEGER NOT NULL DEFAULT 0);
        CREATE TABLE IF NOT EXISTS seats(id TEXT PRIMARY KEY, head TEXT NOT NULL);
        """)

    def close(self):
        self.db.close()

    def _domain(self, body):
        check(body["domain"] == self.domain, "DOMAIN_MISMATCH")

    def _grant(self, envelope):
        grant = validate(envelope, "mandate")
        verify(envelope, self.registry, [grant["principal"]])
        self._domain(grant)
        check(grant["notBefore"] < grant["expiresAt"], "INVALID_VALIDITY")
        return grant

    def _register(self, grant):
        hashed = digest(grant)
        self.db.execute("INSERT OR IGNORE INTO grants(id,hash,agent) VALUES(?,?,?)",
                        (grant["grantId"], hashed, grant["agent"]))
        record = self.db.execute("SELECT * FROM grants WHERE id=?", (grant["grantId"],)).fetchone()
        check(record["hash"] == hashed, "GRANT_ID_CONFLICT")
        return record

    def _current(self, grant, record):
        check(not record["revoked"], "REVOKED")
        check(grant["notBefore"] <= self.clock() < grant["expiresAt"], "EXPIRED_OR_EARLY")

    def assign(self, grant_envelope, assignment):
        grant = self._grant(grant_envelope)
        move = validate(assignment, "assignment")
        self._domain(move)
        verify(assignment, self.registry, [grant["principal"], move["fromAgent"], move["toAgent"]])
        check(move["grantId"] == grant["grantId"] and move["grantHash"] == digest(grant), "GRANT_MISMATCH")
        hashed = digest(move)
        self.db.execute("BEGIN IMMEDIATE")
        try:
            record = self._register(grant)
            # Readback of an already applied assignment is not a fresh grant.
            if self.db.execute("SELECT 1 FROM assignments WHERE hash=?", (hashed,)).fetchone():
                self.db.execute("COMMIT")
                return hashed
            self._current(grant, record)
            check(self.clock() < move["expiresAt"] <= grant["expiresAt"], "EXPIRED_ASSIGNMENT")
            check(record["uses"] == 0, "ENTITLEMENT_ALREADY_USED")
            check(record["agent"] == move["fromAgent"] and record["epoch"] == move["epoch"], "STALE_ASSIGNMENT")
            check(move["toAgent"] != move["fromAgent"] and move["toAgent"] in grant["assignableAgents"], "ASSIGNMENT_FORBIDDEN")
            self.db.execute("UPDATE grants SET agent=?,epoch=epoch+1,assignment_hash=? WHERE id=?",
                            (move["toAgent"], hashed, grant["grantId"]))
            self.db.execute("INSERT INTO assignments VALUES(?,?)", (hashed, grant["grantId"]))
            self.db.execute("COMMIT")
            return hashed
        except Exception:
            self.db.execute("ROLLBACK")
            raise

    def revoke(self, grant_envelope, revocation):
        grant = self._grant(grant_envelope)
        body = validate(revocation, "revocation")
        self._domain(body)
        verify(revocation, self.registry, [grant["principal"]])
        check(body["grantId"] == grant["grantId"] and body["grantHash"] == digest(grant), "GRANT_MISMATCH")
        self.db.execute("BEGIN IMMEDIATE")
        try:
            self._register(grant)
            self.db.execute("UPDATE grants SET revoked=1 WHERE id=?", (grant["grantId"],))
            self.db.execute("COMMIT")
        except Exception:
            self.db.execute("ROLLBACK")
            raise

    def execute(self, grant_envelope, agreement, sources, payloads, agent_key):
        grant = self._grant(grant_envelope)
        agreed = validate(agreement, "agreement")
        self._domain(agreed)
        verify(agreement, self.registry, [agreed["principal"], agreed["recipient"], agreed["agent"]])
        check(self.registry[agreed["agent"]].public_bytes_raw() == agent_key.public_key().public_bytes_raw(), "AGENT_KEY_MISMATCH")
        for field in ("principal", "recipient", "purpose", "capability"):
            check(agreed[field] == grant[field], "SCOPE_MISMATCH")
        check(agreed["grantId"] == grant["grantId"] and agreed["grantHash"] == digest(grant), "GRANT_MISMATCH")
        check(agreed["plan"]["kind"] == agreed["capability"], "CAPABILITY_MISMATCH")
        check({"derive", "disclose", "invoke"} <= set(grant["operations"]), "OPERATION_FORBIDDEN")
        check(len(sources) == len(agreed["sources"]), "SOURCE_MISMATCH")
        actual_ids = []
        for source_envelope, reference in zip(sources, agreed["sources"]):
            source = validate(source_envelope, "source")
            verify(source_envelope, self.registry, [source["controller"]])
            self._domain(source)
            identifier = source["sourceId"]
            actual_ids.append(identifier)
            check(identifier == reference["sourceId"] and digest(source) == reference["descriptorHash"], "SOURCE_MISMATCH")
            check(identifier in grant["sourceIds"] and identifier in payloads, "SOURCE_FORBIDDEN")
            check(source["payloadHash"] == digest(payloads[identifier]), "SOURCE_INTEGRITY")
            check(grant["principal"] in source["allowedPrincipals"] or
                  (source["access"] == "public" and "*" in source["allowedPrincipals"]), "SOURCE_PRINCIPAL_FORBIDDEN")
            check(grant["purpose"] in source["allowedPurposes"], "SOURCE_PURPOSE_FORBIDDEN")
            check(grant["recipient"] in source["audiences"] or
                  (source["access"] == "public" and "*" in source["audiences"]), "SOURCE_AUDIENCE_FORBIDDEN")
            check({"derive", "disclose"} <= set(source["allowedOperations"]), "SOURCE_OPERATION_FORBIDDEN")
        check(len(actual_ids) == len(set(actual_ids)) and set(actual_ids) == set(payloads), "SOURCE_MISMATCH")
        request_hash = digest(agreed)
        self.db.execute("BEGIN IMMEDIATE")
        try:
            record = self._register(grant)
            prior = self.db.execute("SELECT * FROM exchanges WHERE id=?", (agreed["exchangeId"],)).fetchone()
            if prior:
                check(prior["request_hash"] == request_hash, "IDEMPOTENCY_CONFLICT")
                # Exact replay returns already disclosed bytes, not a new action.
                self.db.execute("COMMIT")
                return json.loads(prior["response"])
            self._current(grant, record)
            check(self.clock() < agreed["expiresAt"] <= grant["expiresAt"], "EXPIRED_AGREEMENT")
            check(agreed["agent"] == record["agent"] and agreed["assignmentHash"] == record["assignment_hash"], "WRONG_ENTITLEMENT_HOLDER")
            check(record["uses"] < grant["maxUses"], "ALLOWANCE_EXHAUSTED")
            check(not self.db.execute("SELECT 1 FROM nonces WHERE principal=? AND nonce=?",
                                     (grant["principal"], agreed["nonce"])).fetchone(), "NONCE_REPLAY")
            output = self._adapter(agreed, payloads, agreement)
            result = sign({"version": VERSION, "domain": self.domain, "type": "result",
                           "exchangeId": agreed["exchangeId"], "agreementHash": request_hash,
                           "outputHash": digest(output), "output": output}, {agreed["agent"]: agent_key})
            previous = self.db.execute("SELECT sequence,receipt_hash FROM exchanges ORDER BY sequence DESC LIMIT 1").fetchone()
            receipt = sign({"version": VERSION, "domain": self.domain, "type": "receipt",
                            "exchangeId": agreed["exchangeId"], "agreementHash": request_hash,
                            "grantHash": digest(grant), "principal": grant["principal"],
                            "agent": agreed["agent"], "recipient": grant["recipient"],
                            "outputHash": digest(output), "resultHash": digest(result["body"]),
                            "status": "DELIVERED", "allocation": {"beneficiary": grant["recipient"], "chargeMinor": 0, "unit": "NONE"},
                            "sequence": previous["sequence"] + 1 if previous else 1,
                            "previousReceiptHash": previous["receipt_hash"] if previous else None},
                           {self.operator_id: self.operator_key})
            response = {"result": result, "receipt": receipt}
            self.db.execute("INSERT INTO exchanges VALUES(?,?,?,?,?)", (agreed["exchangeId"], request_hash,
                            canonical(response).decode(), digest(receipt["body"]), receipt["body"]["sequence"]))
            self.db.execute("INSERT INTO nonces VALUES(?,?,?)", (grant["principal"], agreed["nonce"], agreed["exchangeId"]))
            self.db.execute("UPDATE grants SET uses=uses+1 WHERE id=?", (grant["grantId"],))
            self.db.execute("COMMIT")
            return response
        except Exception:
            self.db.execute("ROLLBACK")
            raise

    def _adapter(self, agreed, payloads, envelope):
        plan = agreed["plan"]
        if plan["kind"] == "data-summary":
            check(all(isinstance(data, dict) and isinstance(data.get("readings"), list)
                      for data in payloads.values()), "INVALID_READINGS")
            readings = [v for data in payloads.values() for v in data.get("readings", [])]
            check(bool(readings) and all(type(v) is int and abs(v) <= 1000000 for v in readings), "INVALID_READINGS")
            return {"kind": "data-summary", "sampleCount": len(readings), "sum": sum(readings), "unit": plan["unit"]}
        identifier = "simulated:" + plan["kind"] + ":" + digest(agreed)[:24]
        output = {"kind": plan["kind"], "assetId": identifier, "simulation": True,
                  "plan": plan, "derivedFrom": digest(payloads)}
        if plan["kind"] == "token-create":
            check(sum(plan["allocations"].values()) == plan["supply"], "ALLOCATION_MISMATCH")
            self.db.execute("INSERT INTO assets VALUES(?,?,?,?,0)",
                            (identifier, "token", plan["admin"], canonical(output).decode()))
        else:
            check(plan["beneficiary"] == agreed["recipient"], "BENEFICIARY_MISMATCH")
            seat = self.db.execute("SELECT head FROM seats WHERE id=?", (plan["seatId"],)).fetchone()
            if seat:
                check(plan["predecessor"] == seat["head"], "STALE_PREDECESSOR")
                previous = self.db.execute("SELECT owner,retired FROM assets WHERE id=?", (seat["head"],)).fetchone()
                check(previous is not None and not previous["retired"], "PREDECESSOR_RETIRED")
                verify(envelope, self.registry, [previous["owner"]])
                self.db.execute("UPDATE assets SET retired=1 WHERE id=?", (seat["head"],))
            else:
                check(plan["predecessor"] is None, "UNKNOWN_PREDECESSOR")
            self.db.execute("INSERT INTO assets VALUES(?,?,?,?,0)",
                            (identifier, "nft", plan["beneficiary"], canonical(output).decode()))
            self.db.execute("INSERT INTO seats VALUES(?,?) ON CONFLICT(id) DO UPDATE SET head=excluded.head", (plan["seatId"], identifier))
        return output


def verify_delivery(response, agreement, registry, operator_id):
    agreed = validate(agreement, "agreement")
    verify(agreement, registry, [agreed["principal"], agreed["agent"], agreed["recipient"]])
    result = validate(response["result"], "result")
    receipt = validate(response["receipt"], "receipt")
    verify(response["result"], registry, [agreed["agent"]])
    verify(response["receipt"], registry, [operator_id])
    for item in (result, receipt):
        check(item["domain"] == agreed["domain"] and item["exchangeId"] == agreed["exchangeId"] and
              item["agreementHash"] == digest(agreed), "RECEIPT_BINDING")
        check(item["outputHash"] == digest(result["output"]), "OUTPUT_INTEGRITY")
    check(receipt["resultHash"] == digest(result), "RESULT_BINDING")
    for field in ("principal", "agent", "recipient", "grantHash"):
        check(receipt[field] == agreed[field], "RECEIPT_BINDING")
    check(receipt["allocation"]["beneficiary"] == agreed["recipient"], "ALLOCATION_MISMATCH")
    return receipt
