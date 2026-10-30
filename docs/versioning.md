# Versioning and migration

Current protocol: **agent-sdp**. Specification: **3.0.0**. Reference implementation maturity: alpha.

Major versions change signed semantics or wire compatibility. Minor versions add compatible functionality; patches correct compatible defects or documentation.

## Version 3 migration

The module is `agent_sdp`, distribution is `agent-sdp-reference`, and specification filenames use `SDP-0001` through `SDP-0004`.

The wire namespace is `agent-sdp/3.0`; signature prefix is `agent-sdp/3.0/SDP-JSON-1` followed by a zero byte. Earlier signed envelopes cannot be relabeled. Obtain fresh acceptance and use a fresh local ledger. Synthetic example signatures are regenerated for this version.

Version 1 contained illustrative mandates. Version 2 introduced executable signed exchanges. Legacy v1 fixtures remain in [examples/legacy-v1](../examples/legacy-v1/mandates.json). Historical Git tags and published source archives preserve their original bytes. Current documentation, including changelog wording, uses the current protocol brand.

GitHub owner URLs identify the actual hosting account, not the protocol name. This protocol has no separate official website; the NFT application is one case.
