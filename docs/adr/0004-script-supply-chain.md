---
type: adr
title: "0004 Script supply chain"
status: accepted
date: 2026-11-10
---

# 0004 Script supply chain

## Context

The published install command is a pipe into a root shell:

```bash
bash -c "$(curl -fsSL https://community-scripts.org/.../ct/app.sh)"
```

The `ct/` file then loads the engine from `main`, or from
`COMMUNITY_SCRIPTS_CORE_URL` when that variable is set. Both defaults point at
a moving branch. A run tonight executes code that nobody reviewed.

The engine also sends telemetry and error payloads to an HTTP endpoint. The
code reads `TELEMETRY_URL` and a payload version. No documented opt-out
appeared during the review.

## Decision

A pinned procedure replaces the pipe. The file `scripts/lock.yml` records three
facts for each application: the engine commit, the scripts commit, and the SHA
of the `ct/` file.

- `mise run scripts:fetch` clones both repositories at the recorded commits
  into `.cache/`. The cache is not committed.
- The provision play runs the `ct/` file from that checkout. It sets
  `COMMUNITY_SCRIPTS_CORE_DIR`, so no download happens at run time.
- `mise run scripts:bump -- <app>` fetches the new commits and shows the diff of
  one file. The lock file changes only after a human reads that diff.
- The update wrapper uses the same commits that provision used. See
  [ADR-0008](0008-update-policy.md).
- The telemetry endpoint is recorded in this ADR. The network policy decides
  whether the payload leaves the node.

## Consequences

- The first provision needs network access and a checkout.
- A fresh clone cannot provision until `scripts:fetch` runs.
- An upstream fix arrives only through a reviewed bump. That is the point.
- The node may still fetch the application release from another source during
  the install. The engine controls that fetch, not this repository.
- A telemetry payload leaves the node unless the network blocks it. The
  decision is explicit, not accidental.

## Rejected options

- **`main` plus `curl`.** Unreviewed root code, at every run, with no diff.
- **Vendor the whole upstream.** Six hundred files and a licence notice, for a
  copy that goes stale. The cache gives the same result with less noise.
- **Fork the engine.** It takes over a project that is under active
  development.
- **Block every outbound call.** The install itself needs a package mirror and
  a release download. The policy is narrower than a full block.

## References

- [ADR-0002](0002-ansible-orchestrator-not-opentofu.md)
- [ADR-0008](0008-update-policy.md)
- [Style rules](../reference/style-ste100.md)
