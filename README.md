# proxmox-management

Manage Proxmox guests and their exposure as code.

This repository drives the
[community-scripts](https://community-scripts.org) engine with Ansible.
It keeps the container lifecycle, the network identity, and the Traefik
exposure route in one readable place.

## Status

Version 0.1. Documentation only. No playbook, no guest, and no credential
exist yet. The repository records the decisions that the first code must
follow.

## Start here

| I want to | Read |
| --- | --- |
| Understand the model | [docs/explanation/layers.md](docs/explanation/layers.md) |
| Know why OpenTofu is absent | [docs/explanation/why-not-opentofu.md](docs/explanation/why-not-opentofu.md) |
| Read the decisions | [docs/adr/index.md](docs/adr/index.md) |
| Learn the vocabulary | [docs/glossary.md](docs/glossary.md) |
| Work on the documentation | [AGENTS.md](AGENTS.md) |

## Documentation

The documentation uses the [Diataxis](https://diataxis.fr) structure and lives
in `docs/`. It builds with MkDocs.

```bash
mise install
mise run docs:serve      # local preview on http://127.0.0.1:8000
mise run docs:check      # every check that CI runs
```

## License

Private. No license is granted.
