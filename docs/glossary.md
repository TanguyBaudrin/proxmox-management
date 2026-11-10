---
type: reference
title: Glossary
---

# Glossary

One concept has one term. A second name for the same concept is a defect.
The list of banned variants lives in `scripts/terminology.json`, and the
documentation check fails when a variant appears.

## Terms

| Term | Definition | Avoid |
| --- | --- | --- |
| guest | A container or a virtual machine on a node, managed by this repository. | instance |
| node | A Proxmox host. | server, hypervisor |
| container | An LXC guest. | CT, jail |
| template | An operating-system template stored on a node. | image |
| engine | The shared community-scripts engine that creates a guest. | core, framework |
| application script | The file `ct/<app>.sh` that describes one application. | recipe, installer |
| install script | The file `install/<app>.sh` that runs inside a guest. | setup script |
| guest file | The file `guests/<name>.yml` that declares the desired state of one guest. | manifest, definition |
| inventory | The file `inventory/hosts.yml` that lists the hosts Ansible connects to. | host list |
| desired state | What the repository declares for a guest. | expectation, target |
| envelope | The resource facts this repository owns: cores, memory, disk size, tags, start policy, and network identity. | spec, specification |
| provision | Create a guest that does not exist. | deploy, build |
| reconcile | Compare live state with desired state, then correct the envelope. | converge, enforce |
| drift | A difference between live state and the desired state. | divergence, gap |
| rebuild | Destroy a guest, provision it again, then import application data. | reprovision, reinstall |
| restore | Put a backup back in place, without enforcing the desired state. | rollback, recovery |
| backup freshness | The age of the most recent successful backup of a guest. | backup age |
| exposure route | A Traefik router and service that publish a guest. | vhost, ingress |
| pinned procedure | An engine and application script pair fixed at a commit. | locked version |
| controller | The machine that runs Ansible. | runner, control node |
| managed guest | A guest that a guest file declares. | owned guest |
| unmanaged guest | A guest on a node that no guest file declares. | legacy guest, orphan |

## Verbs at a glance

| Verb | Destroys data | Enforces desired state |
| --- | --- | --- |
| provision | No | Yes |
| reconcile | No | Yes, envelope only |
| rebuild | Yes | Yes |
| restore | Replaces data | No |

## Acronyms

| Acronym | Meaning |
| --- | --- |
| ACME | Automatic Certificate Management Environment |
| ADR | Architecture Decision Record |
| API | Application Programming Interface |
| ASD | AeroSpace and Defence Industries Association of Europe |
| CI | Continuous Integration |
| CPU | Central Processing Unit |
| CTID | Container Identifier, the number PVE assigns to a container |
| DHCP | Dynamic Host Configuration Protocol |
| DNS | Domain Name System |
| HTTP | Hypertext Transfer Protocol |
| HTTPS | Hypertext Transfer Protocol Secure |
| IP | Internet Protocol |
| JSON | JavaScript Object Notation |
| LXC | Linux Containers |
| MAC | Media Access Control, the hardware address of a network interface |
| NAS | Network Attached Storage |
| NFS | Network File System |
| OS | Operating System |
| PVE | Proxmox Virtual Environment |
| RAM | Random Access Memory |
| SHA | Secure Hash Algorithm |
| SSH | Secure Shell |
| STE100 | Simplified Technical English, issue 100 of the ASD standard |
| TLS | Transport Layer Security |
| URL | Uniform Resource Locator |
| VM | Virtual Machine |
| YAML | Data serialization language used for configuration files |

## Related

- [Style rules](reference/style-ste100.md)
- [Documentation checks](reference/doc-checks.md)
- [Layers](explanation/layers.md)
