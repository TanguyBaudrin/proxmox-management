---
type: index
title: Decisions
---

# Decisions

An ADR records one decision. The format is Nygard: context, decision,
consequences. Each ADR also lists the options that were rejected.

A new decision needs a new number. A reversed decision keeps its number and
adds a `superseded-by` field.

| ADR | Title | Status |
| --- | --- | --- |
| [0001](0001-scope-and-layers.md) | Scope and layers | accepted |
| [0002](0002-ansible-orchestrator-not-opentofu.md) | Ansible orchestrates, the engine provisions | accepted |
| [0003](0003-no-state-pve-is-the-source-of-truth.md) | No state, PVE is the source of truth | accepted |
| [0004](0004-script-supply-chain.md) | Script supply chain | accepted |
| [0005](0005-secrets-and-least-privilege.md) | Secrets and least privilege | accepted |
| [0006](0006-documentation-language-and-style.md) | Documentation language and style | accepted |
| [0007](0007-restore-and-rebuild.md) | Restore and rebuild | accepted |
| [0008](0008-update-policy.md) | Update policy | accepted |
| [0009](0009-external-exposure.md) | External exposure | accepted |
| [0010](0010-public-repository-and-secret-hygiene.md) | Public repository and secret hygiene | accepted |
| [0011](0011-documentation-engine-and-publishing.md) | Documentation engine and publishing | accepted |
| [0012](0012-license.md) | License | accepted |

## Reading order

1. Start with 0001. It defines the boundary of the repository.
2. Read 0002 and 0003 together. They define the split between Ansible and the
   engine, and the absence of a state file.
3. Read 0004 and 0005 before the first run. They define trust and access.
4. Read 0007 and 0008 before the first update.
5. Read 0009 before the first exposure route.
6. Read 0010 before you add a guest file to the public repository.
7. Read 0011 before you change the documentation build or the site.
8. Read 0012 before you copy the content into another project.
