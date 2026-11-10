---
type: index
title: proxmox-management
---

# proxmox-management

This repository manages the lifecycle of Proxmox guests with Ansible and the
[community-scripts](https://community-scripts.org) engine. It also owns the
network identity of each guest and its exposure route in an external Traefik
deployment.

## The problem

A fresh container used to take a wizard, a shell paste, and a free afternoon.
The result was invisible to Git. A second node makes the problem worse, because
the same manual work must happen twice.

This repository replaces the wizard with a guest file. It replaces the free
afternoon with a playbook. It replaces trust with a pinned procedure.

## The model in one table

| Layer | Owner | Writes |
| --- | --- | --- |
| Desired state | Git | The guest file |
| Provision | The engine, driven by Ansible | A new guest |
| Reconcile | Ansible | The envelope only |
| Exposure | Ansible | EdgeOS and Traefik |
| Recovery | PVE, driven by Ansible | Backups |

## Status

Version 0.1 is documentation only. No playbook exists. The decisions are
recorded so that the first playbook follows them.

## Where to go

- New to the vocabulary: [Glossary](glossary.md)
- New to the model: [Layers](explanation/layers.md)
- Curious about the tool choice: [Why not OpenTofu](explanation/why-not-opentofu.md)
- Ready to read the rules: [Decisions](adr/index.md)
