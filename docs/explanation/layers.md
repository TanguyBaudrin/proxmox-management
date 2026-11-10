---
type: explanation
title: Layers
---

# Layers

The repository has five layers. Each layer has one owner, one write target,
and one failure mode. A change that crosses two layers needs a plan.

## The five layers

```text
desired state  ->  provision  ->  reconcile  ->  exposure
                        |
                        +--> recovery (backup, restore, rebuild)
```

### Desired state

The guest file declares one guest. The inventory declares the hosts that
Ansible connects to. Both live in Git. Neither holds a secret.

A guest file holds three groups of facts. Identity covers the CTID, the
hostname, and the node. The envelope covers cores, memory, disk size, tags,
start policy, and the network identity. The application covers the script name,
the template, and the health check.

### Provision

Provision creates a guest that does not exist. The engine does the work. It
resolves the template, calls `pct create`, and runs the application script.
Ansible passes an explicit `var_*` set and `MODE=default`. No wizard appears.
See [ADR-0002](../adr/0002-ansible-orchestrator-not-opentofu.md).

Provision is not repeatable over an existing guest. A second run is a no-op,
because the check comes first.

### Reconcile

Reconcile compares live state with the desired state. It corrects the envelope
and nothing else. It never creates, never destroys, and never touches the
application.

This layer is the answer to a manual edit in the web interface. The edit
becomes drift, and the next check reports it. See
[ADR-0003](../adr/0003-no-state-pve-is-the-source-of-truth.md).

### Exposure

Exposure writes the network edge. The EdgeRouter holds the DHCP reservation.
Traefik holds the route. Both writes are narrow, and both are reversible.

The reservation comes before the guest. The route comes after the guest
answers. That order is the contract with the network.

### Recovery

Recovery holds three verbs. A backup copies reality. A restore puts reality
back. A rebuild returns to intent and imports the data. The three verbs are not
interchangeable. See [ADR-0007](../adr/0007-restore-and-rebuild.md).

## What the layers do not do

- No layer installs Proxmox. The node exists first.
- No layer owns an unmanaged guest.
- No layer reconciles the application. The script and the update wrapper do.
- No layer holds a second copy of the resource facts.

## A change, end to end

1. A human edits one guest file.
2. `check` renders the difference: envelope, reservation, and route.
3. `provision` runs once. It creates the guest.
4. `reconcile` runs on every later check. It keeps the envelope true.
5. `expose` writes one route and validates it.
6. The nightly backup and the nightly update run inside the guest.

## Related

- [Why not OpenTofu](why-not-opentofu.md)
- [ADR-0001](../adr/0001-scope-and-layers.md)
