import tempfile
import unittest
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from agent_sdp.crypto import ProtocolError, canonical, digest, parse
from agent_sdp.engine import Engine, VERSION, verify_delivery
from agent_sdp.fixtures import NOW, World
from agent_sdp.verify_trace import verify_trace


class ReferenceTests(unittest.TestCase):
    def setUp(self):
        self.world = World()
        self.temp = tempfile.TemporaryDirectory()
        self.path = str(Path(self.temp.name) / "test.sqlite")
        self.engine = self.open()
        self.bundle = self.world.bundle()

    def open(self, clock=lambda: NOW):
        return Engine(self.path, self.world.registry, "operator:local",
                      self.world.keys["operator:local"], clock=clock)

    def tearDown(self):
        self.engine.close()
        self.temp.cleanup()

    def execute(self, bundle=None, engine=None):
        bundle = bundle or self.bundle
        return (engine or self.engine).execute(bundle["grant"], bundle["agreement"], bundle["sources"],
                    bundle["payloads"], self.world.keys[bundle["agreement"]["body"]["agent"]])

    def reject(self, code, action):
        with self.assertRaises(ProtocolError) as caught:
            action()
        self.assertEqual(caught.exception.code, code)

    def test_all_source_kinds(self):
        for kind in ("personal", "organizational", "public", "research", "device", "environmental", "agent-generated", "composite"):
            with self.subTest(kind=kind):
                response = self.execute(self.world.bundle(kind, kind=kind))
                self.assertEqual(response["result"]["body"]["output"]["sum"], 54)

    def test_public_access_still_requires_purpose(self):
        source = self.bundle["sources"][0]["body"]
        source.update(access="public", allowedPrincipals=["*"], audiences=["*"], allowedPurposes=["other"])
        self.bundle["sources"][0] = self.world.signed(source, ["org:source"])
        self.bundle["agreement"]["body"]["sources"][0]["descriptorHash"] = digest(source)
        self.world.resign_agreement(self.bundle)
        self.reject("SOURCE_PURPOSE_FORBIDDEN", self.execute)

    def test_nonce_cannot_cross_grants(self):
        self.execute()
        other = self.world.bundle("other")
        other["agreement"]["body"]["nonce"] = self.bundle["agreement"]["body"]["nonce"]
        self.world.resign_agreement(other)
        self.reject("NONCE_REPLAY", lambda: self.execute(other))

    def test_canonical_vectors(self):
        vectors = parse((Path(__file__).parents[1] / "examples/wire-vectors.json").read_text(encoding="utf-8"))
        for vector in vectors["vectors"]:
            self.assertEqual(canonical(vector["input"]).decode("ascii"), vector["canonicalAscii"])
            self.assertEqual(digest(vector["input"]), vector["sha256"])

    def test_wire_schema_is_valid(self):
        from jsonschema import Draft202012Validator
        schema = parse((Path(__file__).parents[1] / "agent_sdp/schemas/wire.schema.json").read_text(encoding="utf-8"))
        Draft202012Validator.check_schema(schema)

    def test_delivered_readback_after_revocation_and_expiry(self):
        response = self.execute()
        grant = self.bundle["grant"]["body"]
        revocation = self.world.signed({"version": VERSION, "domain": "local:demo", "type": "revocation",
                    "grantId": grant["grantId"], "grantHash": digest(grant), "nonce": "revoke:after"}, [grant["principal"]])
        self.engine.revoke(self.bundle["grant"], revocation)
        self.engine.clock = lambda: NOW + 7200
        self.assertEqual(self.execute(), response)

    def test_signed_delivery(self):
        response = self.execute()
        receipt = verify_delivery(response, self.bundle["agreement"], self.world.registry, "operator:local")
        self.assertEqual(receipt["status"], "DELIVERED")
        self.assertEqual(response["result"]["body"]["output"]["sum"], 54)

    def test_altered_signature(self):
        self.bundle["agreement"]["body"]["purpose"] = "other"
        self.reject("BAD_SIGNATURE", self.execute)

    def test_operator_cannot_replace_principal(self):
        self.bundle["grant"] = self.world.signed(self.bundle["grant"]["body"], ["operator:local"])
        self.reject("MISSING_SIGNATURE", self.execute)

    def test_counterparty_acceptance_required(self):
        self.bundle["agreement"] = self.world.signed(self.bundle["agreement"]["body"], ["org:publisher", "agent:maker"])
        self.reject("MISSING_SIGNATURE", self.execute)

    def test_purpose_cannot_expand(self):
        self.bundle["agreement"]["body"]["purpose"] = "other"
        self.world.resign_agreement(self.bundle)
        self.reject("SCOPE_MISMATCH", self.execute)

    def test_source_bytes_must_match(self):
        self.bundle["payloads"]["source:research"]["readings"][0] = 99
        self.reject("SOURCE_INTEGRITY", self.execute)

    def test_source_disclosure_policy(self):
        source = self.bundle["sources"][0]["body"]
        source["audiences"] = ["org:incoming"]
        self.bundle["sources"][0] = self.world.signed(source, ["org:source"])
        self.bundle["agreement"]["body"]["sources"][0]["descriptorHash"] = digest(source)
        self.world.resign_agreement(self.bundle)
        self.reject("SOURCE_AUDIENCE_FORBIDDEN", self.execute)

    def test_domain_is_bound(self):
        self.bundle["agreement"]["body"]["domain"] = "local:other"
        self.world.resign_agreement(self.bundle)
        self.reject("DOMAIN_MISMATCH", self.execute)

    def test_expiry(self):
        self.engine.clock = lambda: NOW + 7200
        self.reject("EXPIRED_OR_EARLY", self.execute)

    def test_replay_persists_after_restart(self):
        response = self.execute()
        self.engine.close()
        self.engine = self.open()
        self.assertEqual(self.execute(), response)
        self.assertEqual(self.engine.db.execute("SELECT uses FROM grants").fetchone()[0], 1)

    def test_changed_replay_rejected(self):
        self.execute()
        self.bundle["agreement"]["body"]["plan"]["unit"] = "changed"
        self.world.resign_agreement(self.bundle)
        self.reject("IDEMPOTENCY_CONFLICT", self.execute)

    def test_new_operation_cannot_double_spend(self):
        self.execute()
        self.bundle["agreement"]["body"]["exchangeId"] = "exchange:again"
        self.bundle["agreement"]["body"]["nonce"] = "nonce:again"
        self.world.resign_agreement(self.bundle)
        self.reject("ALLOWANCE_EXHAUSTED", self.execute)

    def test_revocation_blocks_new_execution(self):
        grant = self.bundle["grant"]["body"]
        revocation = self.world.signed({"version": VERSION, "domain": "local:demo", "type": "revocation",
                    "grantId": grant["grantId"], "grantHash": digest(grant), "nonce": "revoke:1"}, [grant["principal"]])
        self.engine.revoke(self.bundle["grant"], revocation)
        self.reject("REVOKED", self.execute)

    def test_assignment_invalidates_old_agent(self):
        move = self.world.assignment(self.bundle)
        self.engine.assign(self.bundle["grant"], move)
        self.reject("WRONG_ENTITLEMENT_HOLDER", self.execute)

    def test_assigned_agent_consumes_same_allowance(self):
        move = self.world.assignment(self.bundle)
        assignment_hash = self.engine.assign(self.bundle["grant"], move)
        self.assertEqual(self.engine.assign(self.bundle["grant"], move), assignment_hash)
        self.bundle["agreement"]["body"].update(agent="agent:successor", assignmentHash=assignment_hash)
        self.world.resign_agreement(self.bundle)
        self.execute()
        self.assertEqual(self.engine.db.execute("SELECT uses FROM grants").fetchone()[0], 1)

    def test_assignment_requires_recipient_acceptance(self):
        move = self.world.assignment(self.bundle)
        move = self.world.signed(move["body"], ["org:publisher", "agent:maker"])
        self.reject("MISSING_SIGNATURE", lambda: self.engine.assign(self.bundle["grant"], move))

    def test_fulfilled_right_cannot_be_assigned(self):
        self.execute()
        self.reject("ENTITLEMENT_ALREADY_USED", lambda: self.engine.assign(self.bundle["grant"], self.world.assignment(self.bundle)))

    def test_output_tampering_detected(self):
        response = self.execute()
        response["result"]["body"]["output"]["sum"] = 0
        self.reject("BAD_SIGNATURE", lambda: verify_delivery(response, self.bundle["agreement"], self.world.registry, "operator:local"))

    def test_failed_adapter_rolls_back(self):
        token = self.world.bundle("bad-token", capability="token-create", plan={"kind": "token-create",
                    "name": "Example", "symbol": "EX", "supply": 100, "allocations": {"org:publisher": 99}, "admin": "org:publisher"})
        self.reject("ALLOCATION_MISMATCH", lambda: self.execute(token))
        self.assertEqual(self.engine.db.execute("SELECT COUNT(*) FROM exchanges").fetchone()[0], 0)
        self.assertEqual(self.engine.db.execute("SELECT COUNT(*) FROM grants").fetchone()[0], 0)

    def test_concurrent_duplicate_has_one_effect(self):
        def call(_):
            engine = self.open()
            try:
                return self.execute(engine=engine)
            finally:
                engine.close()
        with ThreadPoolExecutor(max_workers=2) as pool:
            results = list(pool.map(call, range(2)))
        self.assertEqual(results[0], results[1])
        self.assertEqual(self.engine.db.execute("SELECT COUNT(*) FROM exchanges").fetchone()[0], 1)

    def test_nft_successor_requires_previous_owner(self):
        genesis = self.world.bundle("genesis", capability="nft-create", recipient="org:publisher",
                    plan={"kind": "nft-create", "seatId": "seat:1", "predecessor": None, "beneficiary": "org:publisher"})
        predecessor = self.execute(genesis)["result"]["body"]["output"]["assetId"]
        successor = self.world.bundle("successor", capability="nft-create", principal="org:incoming", recipient="org:incoming",
                    plan={"kind": "nft-create", "seatId": "seat:1", "predecessor": predecessor, "beneficiary": "org:incoming"})
        self.reject("MISSING_SIGNATURE", lambda: self.execute(successor))
        self.world.resign_agreement(successor, ["org:publisher"])
        self.execute(successor)
        record = self.engine.db.execute("SELECT owner,retired FROM assets WHERE id=?", (predecessor,)).fetchone()
        self.assertEqual(tuple(record), ("org:publisher", 1))

    def test_duplicate_json_fields_rejected(self):
        self.reject("DUPLICATE_FIELD", lambda: parse('{"grantId":"a","grantId":"b"}'))

    def test_floats_rejected(self):
        self.reject("INVALID_JSON_TYPE", lambda: canonical({"amount": 1.5}))

    def test_published_trace_verifies(self):
        trace = parse((Path(__file__).parents[1] / "examples/traces/local-exchange.json").read_text(encoding="utf-8"))
        self.assertEqual(verify_trace(trace), 4)
        trace["exchanges"][0]["output"]["receipt"]["body"]["recipient"] = "org:incoming"
        self.reject("BAD_SIGNATURE", lambda: verify_trace(trace))


if __name__ == "__main__":
    unittest.main()
