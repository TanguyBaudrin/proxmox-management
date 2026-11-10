---
type: adr
title: "0003 No state, PVE is the source of truth"
status: accepted
date: 2026-11-10
---

# 0003 No state, PVE is the source of truth

## Context

A state file solves one problem and creates another. It records what a tool
believes, and it drifts from what the node holds. It also stores secrets,
because a provider writes them there.

The engine is create-only. It creates a guest and installs an application. It
has no opinion about a later change to memory, cores, or tags. The guest file is
then the only record of those facts. It lies as soon as somebody edits the
guest in the web interface.

## Decision

The node is the source of truth. The repository holds no ledger and no state
file.

- `check` queries PVE and reports every difference. It is the equivalent of a
  plan.
- `reconcile` corrects the envelope and nothing else.
- The envelope holds cores, memory, disk size, tags, start policy, and the
  network identity: address, gateway, and MAC address.
- The engine owns creation. `reconcile` never creates or destroys a guest.
- Disk size grows and never shrinks. A request to shrink is a reported drift
  that a human resolves.

Application configuration is not reconciled. The application script sets it
once. The update wrapper maintains it. See
[ADR-0008](0008-update-policy.md).

## Consequences

- A manual edit in the web interface becomes a visible drift at the next
  `check`. Nothing hides it.
- The token must allow a read of the whole guest list and a write of the
  envelope. The role stays narrow.
- A `reconcile` run is safe to repeat. It writes the same values and stops.
- The repository has no recovery record. A lost laptop loses nothing.
- The guest file must list every envelope field. An implicit default from an
  upstream script is not a decision, and it changes without notice.

## Rejected options

- **An OpenTofu state file.** It stores the read-write token, it covers PVE
  only, and it reintroduces the create path that the engine already owns.
- **A ledger file in Git.** It is a second source of truth. It rots between
  commits, and a conflict in it is unreadable.
- **Discipline in the web interface.** It leaves no trace and no diff.
- **Reconcile the application too.** It would fight the application script and
  the update wrapper, and it would rewrite files that a package owns.

## References

- [ADR-0002](0002-ansible-orchestrator-not-opentofu.md)
- [ADR-0008](0008-update-policy.md)
- [Layers](../explanation/layers.md)
