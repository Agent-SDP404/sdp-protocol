"""Synthetic data and ephemeral keys for examples/tests. No private keys exported."""
from datetime import datetime, timezone
from .crypto import digest, key, sign
from .engine import VERSION

NOW = int(datetime(2026, 10, 30, 12, tzinfo=timezone.utc).timestamp())


class World:
    def __init__(self):
        self.keys = {name: key() for name in ["org:publisher", "org:incoming", "org:receiver",
                     "org:source", "agent:maker", "agent:successor", "operator:local"]}
        self.registry = {name: secret.public_key() for name, secret in self.keys.items()}

    def signed(self, body, identities):
        return sign(body, {name: self.keys[name] for name in identities})

    def bundle(self, name="research", kind="research", capability="data-summary",
               principal="org:publisher", recipient="org:receiver", plan=None, payload=None,
               agent="agent:maker", assignment_hash=None):
        payload = payload if payload is not None else {"readings": [12, 18, 24]}
        source = {"version": VERSION, "domain": "local:demo", "type": "source",
                  "sourceId": "source:" + name, "kind": kind, "controller": "org:source",
                  "access": "restricted", "termsRef": "example:synthetic-use-only",
                  "payloadHash": digest(payload), "allowedPrincipals": [principal],
                  "allowedPurposes": ["purpose:" + name], "audiences": [recipient],
                  "allowedOperations": ["derive", "disclose"]}
        grant = {"version": VERSION, "domain": "local:demo", "type": "mandate",
                 "grantId": "grant:" + name, "principal": principal, "agent": agent,
                 "recipient": recipient, "purpose": "purpose:" + name,
                 "sourceIds": [source["sourceId"]], "capability": capability,
                 "operations": ["derive", "disclose", "invoke"], "notBefore": NOW - 60,
                 "expiresAt": NOW + 3600, "maxUses": 1, "maxChargeMinor": 0,
                 "assignableAgents": ["agent:successor"]}
        agreed = {"version": VERSION, "domain": "local:demo", "type": "agreement",
                  "exchangeId": "exchange:" + name, "grantId": grant["grantId"],
                  "grantHash": digest(grant), "principal": principal, "agent": agent,
                  "recipient": recipient, "purpose": grant["purpose"], "capability": capability,
                  "sources": [{"sourceId": source["sourceId"], "descriptorHash": digest(source)}],
                  "plan": plan if plan is not None else {"kind": "data-summary", "unit": "synthetic-units"},
                  "nonce": "nonce:" + name, "expiresAt": NOW + 600, "assignmentHash": assignment_hash}
        return {"grant": self.signed(grant, [principal]),
                "agreement": self.signed(agreed, [principal, recipient, agent]),
                "sources": [self.signed(source, [source["controller"]])],
                "payloads": {source["sourceId"]: payload}}

    def resign_agreement(self, bundle, extra=()):
        body = bundle["agreement"]["body"]
        bundle["agreement"] = self.signed(body, {body["principal"], body["recipient"], body["agent"], *extra})

    def assignment(self, bundle):
        grant = bundle["grant"]["body"]
        body = {"version": VERSION, "domain": "local:demo", "type": "assignment",
                "grantId": grant["grantId"], "grantHash": digest(grant),
                "fromAgent": grant["agent"], "toAgent": "agent:successor", "epoch": 0,
                "nonce": "handoff:" + grant["grantId"], "expiresAt": NOW + 600}
        return self.signed(body, [grant["principal"], body["fromAgent"], body["toAgent"]])
