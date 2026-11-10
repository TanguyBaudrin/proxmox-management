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
in `docs/`. It builds with [Zensical](https://zensical.org) and publishes to
[GitHub Pages](https://tanguybaudrin.github.io/proxmox-management/).

```bash
mise install
mise run docs:serve      # local preview on http://127.0.0.1:8000
mise run check           # every check that CI runs
```

## Security

The repository is public and holds no secret. Secrets come from Bitwarden
through `fnox`. GitHub secret scanning and push protection are enabled, and
`mise run check` scans the full history with `gitleaks`. See
[docs/adr/0010-public-repository-and-secret-hygiene.md](docs/adr/0010-public-repository-and-secret-hygiene.md).

## License

No license is granted.
