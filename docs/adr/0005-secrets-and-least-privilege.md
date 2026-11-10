---
type: adr
title: "0005 Secrets and least privilege"
status: accepted
date: 2026-11-10
---

# 0005 Secrets and least privilege

## Context

Two different credentials are needed. They differ in privilege and in
transport, and a mistake is expensive.

- The API token drives the Ansible modules for PVE. It reads the guest list and
  writes the envelope.
- Root over SSH runs the engine. The engine calls `pct create` and installs
  packages on the node.

A third credential reaches the Traefik host. A fourth reaches the EdgeRouter.
All four must stay out of Git.

## Decision

- The API token belongs to a dedicated user, `ansible@pve`, with a custom
  role. The role grants `VM.Audit`, `VM.Allocate`, `VM.Config.*`,
  `VM.PowerMgmt`, `Datastore.Audit`, and `Datastore.AllocateSpace` on the guest
  storages. It never grants `Sys.*` or `Realm.*`.
- `root@pam` is never used for the API. Root over SSH stays a separate path,
  used only by the engine.
- Secrets live in Bitwarden. `fnox` injects them at run time. No secret file
  exists in the working tree.
- Every task that reads a secret sets `no_log: true`.
- SSH authentication goes through the `pass-cli` agent, which the repository
  `mise.toml` already starts at the parent level.
- The Traefik host gets its own user and its own key. The EdgeRouter gets a
  dedicated login. Neither shares the PVE credential.
- `check` needs the token and therefore an unlocked Bitwarden. A read-only run
  still needs an unlock.

## Consequences

- A leaked laptop exposes no stored token. The Bitwarden session unlocks the
  access, and the vault revokes it.
- A lost token is revoked in one place.
- An API call that needs `Sys.*` fails. The failure is the design.
- The first run needs an interactive unlock. An unattended run needs a
  service account later, and that is a new ADR.

## Rejected options

- **`root@pam` API token.** Every log line and every error message can carry
  it, and it grants the whole cluster.
- **An `ansible-vault` file in Git.** It moves the secret into the repository
  and adds a second password to protect it.
- **An `.env` file.** It leaks through a screenshot, a backup, and a shell
  history.
- **One credential for every host.** A compromise on the EdgeRouter becomes a
  compromise of the hypervisor.

## References

- [ADR-0003](0003-no-state-pve-is-the-source-of-truth.md)
- [ADR-0009](0009-external-exposure.md)
