---
type: explanation
title: Why not OpenTofu
---

# Why not OpenTofu

OpenTofu is a good tool. It solves the wrong problem here. This page records
the reasoning, so that a later reader does not reopen the question without new
facts.

## The creation step belongs to a shell script

The community-scripts engine creates the container. It resolves the template,
calls `pct create`, checks the storage, and retries a failed start. It runs as
root on the node.

A provider cannot call that script in a meaningful way. The two paths would
compete. One path creates the container with the provider, and the other path
creates it again with the script. This is not a detail. It is a second
implementation of the same act.

## The application lifecycle lives in the script, not in the file

The `ct/<app>.sh` file defines `update_script()`. That function holds the
application-specific update logic: which release to fetch, which files to
back up, which service to restart.

The `install/<app>.sh` file does not run alone. It reads
`$FUNCTIONS_FILE_PATH`, and the engine sets that variable. A tool that
replaces the engine must replace both. That tool would then own a moving
target of six hundred scripts.

## The provider covers one third of the stack

The repository touches three systems: PVE, the EdgeRouter, and the Traefik
host. OpenTofu has a mature provider for PVE. It has no official provider for
EdgeOS or for a Traefik dynamic file.

The result would be two tools, two state models, and one boundary that nobody
can draw. Ansible covers all three with one execution model.

## The token would land in the state file

This repository uses a read-write token for PVE. A provider writes that token
into the state file. The state then becomes a root-equivalent secret on a
laptop, protected by file permissions and hope.

Ansible holds no state. The token stays in Bitwarden and arrives at run time.
See [ADR-0005](../adr/0005-secrets-and-least-privilege.md).

## The engine is already scriptable

The wizard is optional. Every `ct/` file reads `var_*` variables with a
default fallback. The engine treats `MODE=default` as an unattended run. The
environment decides the CTID, the hostname, the address, the size, and the
tags.

The engine is therefore a provisioning tool with a shell interface. Ansible
drives it with a small, explicit variable set. No provider is needed, and no
provider is missing.

## When this decision should change

Reopen this ADR when one of these facts changes.

- The number of managed guests passes roughly twenty-five.
- Placement across several nodes becomes a real constraint.
- A change needs a destroy-and-recreate graph that Ansible cannot express.
- An official provider appears for the EdgeRouter and for Traefik.

Until then, a second tool adds cost and removes nothing.

## Related

- [ADR-0002](../adr/0002-ansible-orchestrator-not-opentofu.md)
- [Layers](layers.md)
