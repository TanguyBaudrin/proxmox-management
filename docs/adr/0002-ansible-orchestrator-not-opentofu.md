---
type: adr
title: "0002 Ansible orchestrates, the engine provisions"
status: accepted
date: 2026-11-10
---

# 0002 Ansible orchestrates, the engine provisions

## Context

The community-scripts project splits one installation into three parts. The
`ct/<app>.sh` file declares an application and its defaults. The
`install/<app>.sh` file installs the application inside a guest. A shared
engine, in a separate repository called `core`, creates the container and
drives the wizard.

Three facts decide the architecture.

1. The `install/` file needs `$FUNCTIONS_FILE_PATH` from the engine. It does
   not run alone.
2. The `ct/` file defines `update_script()`. The application lifecycle lives
   there, not in `install/`.
3. Every `ct/` file reads `var_*` environment variables with a default
   fallback, for example `var_cpu="${var_cpu:-1}"`. The engine accepts
   `MODE=default` for a run without prompts.

The engine therefore exposes a scriptable interface. It is a provisioning
tool with a shell interface, not a wizard.

## Decision

Ansible orchestrates. The engine provisions.

Ansible does these tasks.

- Read the guest file and the inventory.
- Create the DHCP reservation before the guest exists.
- Open one SSH session to the node and run the application script with an
  explicit `var_*` set and `MODE=default`.
- Check the result and record the outcome.
- Write the exposure route after the guest answers.
- Reconcile the envelope on a later run.

Ansible creates no container with a module. Ansible runs no install script.
The engine owns the `pct create` call, the template resolution, the storage
checks, and the retry logic. A second implementation of that logic is a defect.

## Consequences

- Provisioning needs a local checkout of the engine and of the scripts. A
  pinned procedure replaces a `curl` pipe. See
  [ADR-0004](0004-script-supply-chain.md).
- A provision run needs root over SSH on the node. The API token is not
  enough. See [ADR-0005](0005-secrets-and-least-privilege.md).
- The engine creates the guest. Ansible cannot diff a guest file against a
  creation step. Reconcile covers the envelope, and the update wrapper covers
  the application. See [ADR-0003](0003-no-state-pve-is-the-source-of-truth.md).
- An upstream change to an application script needs a reviewed bump. The
  procedure is pinned, so the change is visible before it runs.

## Rejected options

- **OpenTofu creates the guest, Ansible configures it.** Two owners for one
  container. The provider covers PVE only, so the EdgeRouter and Traefik need
  Ansible anyway. The read-write token also lands in the state file.
- **Ansible creates the container with `community.proxmox.proxmox`.** It works,
  and then `install/` still needs the engine. That means two creation paths and
  two ideas of the default resources.
- **A bash wrapper with `mise` only.** It would replace Ansible for the node
  and the engine. It would also lose inventory, loops, and idempotent modules
  for the EdgeRouter and Traefik. The wrapper needs a hand-written diff and
  reporting layer.
- **A fork of the scripts.** Six hundred files to maintain, and the upstream
  fixes stop arriving.

## References

- [Why not OpenTofu](../explanation/why-not-opentofu.md)
- [ADR-0003](0003-no-state-pve-is-the-source-of-truth.md)
- [ADR-0004](0004-script-supply-chain.md)
