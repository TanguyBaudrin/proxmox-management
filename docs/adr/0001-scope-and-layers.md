---
type: adr
title: "0001 Scope and layers"
status: accepted
date: 2026-11-10
---

# 0001 Scope and layers

## Context

One Proxmox node runs today. A second node arrives soon. Every guest is built
by hand from the community-scripts website: one shell paste, one wizard, one
free afternoon. The node also carries guests that nobody built this way. A
Ubiquiti EdgeRouter provides DHCP and handles certificates for nothing. A
separate Traefik host publishes services.

The word "manage" hides five different jobs. Without a boundary, the repository
absorbs the hypervisor, the appliance operating systems, and the applications.
It then rots.

## Decision

The repository manages five layers. Each layer has one owner and one write
target.

| Layer | Owner | Write target |
| --- | --- | --- |
| Desired state | Git | The guest file and the inventory |
| Provision | The engine, driven by Ansible | A new guest |
| Reconcile | Ansible | The envelope of a managed guest |
| Exposure | Ansible | The EdgeRouter and Traefik |
| Recovery | PVE, driven by Ansible | Backups and restores |

These items stay out of scope.

- Proxmox installation and node hardening. The node exists before this
  repository runs.
- The operating system of the EdgeRouter and of the Traefik host. The
  repository configures both. It never installs either.
- The configuration inside a guest, beyond the application script and the
  update wrapper.
- An unmanaged guest. A guest without a guest file stays unmanaged, and the
  repository never touches it.

The repository keeps the name `proxmox-management`. PVE is the centre of
gravity. The EdgeRouter and Traefik are satellites with a narrow contract.

## Consequences

- The controller needs network access to the node, the EdgeRouter, and the
  Traefik host.
- A managed guest is fully described by one guest file.
- An unmanaged guest is invisible to every play, by design.
- The scope stays small enough for one person and one evening per change.

## Rejected options

- **Full hypervisor as code.** It needs a provider, a state file, and a bare
  metal install path. The node already exists, and the provider does not cover
  the appliances.
- **Manage the appliance operating systems.** EdgeOS and the Traefik host have
  a vendor upgrade path. A repository that owns their OS owns their downtime.
- **Import the unmanaged guests.** An import needs a complete guest file for
  each one. The value is low, and the risk of a bad `reconcile` is high.
- **Rename the repository.** A new name hides the scope question. The ADR
  answers it instead.

## References

- [Layers](../explanation/layers.md)
- [ADR-0002](0002-ansible-orchestrator-not-opentofu.md)
