# AGENTS.md — working rules for this repository

This file is the entry point for a coding agent. The documentation lives in
`docs/`. This file holds only the rules that an agent must always follow.

## 1. What this repository is

The repository manages the lifecycle of Proxmox guests with Ansible and the
community-scripts engine. It also owns the network identity of each guest and
its exposure route in an external Traefik instance.

Read [docs/explanation/layers.md](docs/explanation/layers.md) before you change
anything. The layer model defines what this repository may write.

## 2. Must-know rules

- **The engine provisions, Ansible orchestrates.** Never create a container
  with an Ansible module. Never run an `install/<app>.sh` file directly.
  See [ADR-0002](docs/adr/0002-ansible-orchestrator-not-opentofu.md).
- **There is no state file.** PVE is the source of truth. Ansible compares live
  state with the guest file, and corrects only the envelope.
  See [ADR-0003](docs/adr/0003-no-state-pve-is-the-source-of-truth.md).
- **Never use `root@pam`.** Use the `ansible@pve` token for API work. Use root
  over SSH only because the engine requires it.
  See [ADR-0005](docs/adr/0005-secrets-and-least-privilege.md).
- **Never `curl | bash`.** Run a pinned procedure from a local checkout.
  See [ADR-0004](docs/adr/0004-script-supply-chain.md).
- **Never `docker cp` into Traefik.** Write to the mounted directory.
  See [ADR-0009](docs/adr/0009-external-exposure.md).
- **Do not add an unmanaged guest to the inventory.** Unmanaged guests stay
  unmanaged until someone writes a guest file for them.
- **Do not commit a secret.** Secrets come from Bitwarden through `fnox`.
  The repository is public. See
  [ADR-0010](docs/adr/0010-public-repository-and-secret-hygiene.md).

## 3. Documentation rules

- **Language.** English only. French appears only in the name of a device or a
  host.
- **Style.** Apply ASD-STE100 to `docs/how-to/`, `docs/tutorials/`, and
  `docs/reference/`. Use plain technical English elsewhere.
  See [docs/reference/style-ste100.md](docs/reference/style-ste100.md).
- **Structure.** One page belongs to one Diataxis type. The type is in the
  front matter and decided before the title.
- **Front matter.** Every page in `docs/` starts with `type` and `title`.
  An ADR also starts with `status` and `date`.
- **One concept, one term.** Use the term from
  [docs/glossary.md](docs/glossary.md). Do not invent a second name for an
  existing concept.
- **New term.** Add it to the glossary in the same change that uses it.
- **New decision.** Write an ADR. Do not hide a decision in a how-to guide.
- **Links.** Use relative Markdown links. Do not use wikilinks.
- **Code blocks.** Use fenced blocks with a language tag.

## 4. Checks

Run the full set before you commit.

```bash
mise run check
```

The command runs the structure checks, the prose checks, the spell check, the
Markdown lint, a strict MkDocs build, and a scan of the full Git history for a
secret. See [docs/reference/doc-checks.md](docs/reference/doc-checks.md).

## 5. Layout

```text
docs/
  index.md              entry page
  glossary.md           vocabulary and acronyms
  adr/                  architecture decisions, one file per decision
  how-to/               task procedures, STE100
  reference/            rules and facts, STE100
  explanation/          reasoning, plain English
  tutorials/            guided learning, empty until v0.2
scripts/
  check_docs.py         structure and prose checks
  terminology.json      canonical terms and banned variants
styles/                 Vale style pack
```

## 6. Commands

| Command | Effect |
| --- | --- |
| `mise install` | Install the toolchain |
| `mise run check` | Run the documentation checks and the secret scan |
| `mise run docs:check` | Run the documentation checks only |
| `mise run secrets:check` | Scan the full Git history for a secret |
| `mise run docs:serve` | Serve the documentation locally |
| `mise run docs:fix` | Apply the automatic fixes that exist |

## 7. Out of scope

Do not add these to this repository without a new ADR.

- Proxmox installation or node hardening
- The operating system of a network appliance
- Application configuration inside a guest, beyond provision and update
- A second source of truth for resource facts
