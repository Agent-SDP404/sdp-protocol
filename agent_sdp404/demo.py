"""Run real signed local exchanges and explicitly simulated asset adapters."""
import argparse
import base64
import json
import tempfile
from pathlib import Path

from .crypto import ProtocolError, digest, sign
from .engine import Engine, VERSION, verify_delivery
from .fixtures import NOW, World


def run(output=None):
    world = World()
    with tempfile.TemporaryDirectory(prefix="agent-sdp404-") as directory:
        engine = Engine(str(Path(directory) / "ledger.sqlite"), world.registry,
                        "operator:local", world.keys["operator:local"], clock=lambda: NOW)
        trace = {"profile": "agent-sdp404/local-1", "dataNotice": "All source data is synthetic. Asset adapters are local simulations; signatures and SQLite transactions are real.",
                 "clock": NOW, "publicKeys": {name: base64.b64encode(public.public_bytes_raw()).decode()
                                              for name, public in world.registry.items()}, "exchanges": []}

        def perform(bundle, extra=None):
            identity = bundle["agreement"]["body"]["agent"]
            response = engine.execute(bundle["grant"], bundle["agreement"], bundle["sources"], bundle["payloads"], world.keys[identity])
            receipt = verify_delivery(response, bundle["agreement"], world.registry, "operator:local")
            acknowledgement = world.signed({"version": VERSION, "domain": "local:demo", "type": "acknowledgement",
                              "exchangeId": receipt["exchangeId"], "receiptHash": digest(receipt),
                              "recipient": receipt["recipient"]}, [receipt["recipient"]])
            record = {"input": bundle, "output": response, "acknowledgement": acknowledgement}
            if extra:
                record["assignment"] = extra
            trace["exchanges"].append(record)
            print(receipt["exchangeId"] + ": DELIVERED; agent + operator signatures verified; recipient acknowledged")
            return response

        research = world.bundle()
        first = perform(research)
        replay = engine.execute(research["grant"], research["agreement"], research["sources"], research["payloads"], world.keys["agent:maker"])
        assert replay == first
        print("Exact replay: same receipt; no additional allowance consumed")
        altered = json.loads(json.dumps(research))
        altered["agreement"]["body"]["plan"]["unit"] = "different-unit"
        world.resign_agreement(altered)
        try:
            engine.execute(altered["grant"], altered["agreement"], altered["sources"], altered["payloads"], world.keys["agent:maker"])
        except ProtocolError as error:
            assert error.code == "IDEMPOTENCY_CONFLICT"
            trace["conflictingReplay"] = error.code
            print("Changed replay: IDEMPOTENCY_CONFLICT")
        else:
            raise AssertionError("Changed replay must fail")

        token = world.bundle("token", "organizational", "token-create", plan={
            "kind": "token-create", "name": "Synthetic Research Credits", "symbol": "SRC",
            "supply": 1000, "allocations": {"org:publisher": 200, "org:receiver": 800}, "admin": "org:publisher"},
            payload={"project": "synthetic research collaboration", "intent": "coordinate participation"})
        move = world.assignment(token)
        assigned_hash = engine.assign(token["grant"], move)
        token["agreement"]["body"]["agent"] = "agent:successor"
        token["agreement"]["body"]["assignmentHash"] = assigned_hash
        world.resign_agreement(token)
        perform(token, move)

        genesis = world.bundle("nft-genesis", "agent-generated", "nft-create", recipient="org:publisher",
                    plan={"kind": "nft-create", "seatId": "seat:demo", "predecessor": None, "beneficiary": "org:publisher"},
                    payload={"motif": "synthetic collaborative observatory"})
        predecessor = perform(genesis)["result"]["body"]["output"]["assetId"]
        successor = world.bundle("nft-successor", "environmental", "nft-create", principal="org:incoming", recipient="org:incoming",
                    plan={"kind": "nft-create", "seatId": "seat:demo", "predecessor": predecessor, "beneficiary": "org:incoming"},
                    payload={"motif": "synthetic estuary observations"})
        world.resign_agreement(successor, ["org:publisher"])
        perform(successor)
        trace["assetState"] = [dict(row) for row in engine.db.execute("SELECT id,kind,owner,retired FROM assets ORDER BY id")]
        trace["allowanceState"] = [dict(row) for row in engine.db.execute("SELECT id,agent,uses,epoch FROM grants ORDER BY id")]
        engine.close()
        if output:
            destination = Path(output)
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_text(json.dumps(trace, indent=2) + "\n", encoding="utf-8", newline="\n")
            print("Public proof bundle: " + str(destination))
        print("PASS: research exchange, creation-right assignment, token simulation and NFT succession simulation")
        return trace


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", help="Save synthetic inputs, public keys and signed receipts; never private keys")
    run(parser.parse_args().output)
