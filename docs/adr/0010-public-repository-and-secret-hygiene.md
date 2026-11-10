---
type: adr
title: "0010 Public repository and secret hygiene"
status: accepted
date: 2026-11-10
---

# 0010 Public repository and secret hygiene

## Context

The repository started private. A private repository on the free plan cannot
enable branch protection or rulesets. The API answers `403` with a request to
upgrade. That leaves `main` writable by a force push, and no required check
before a merge.

The content holds no secret today. A scan of the full history with `gitleaks`
finds nothing. The only address in the tree is the loopback address in the
entry page.

The repository will later hold guest files. A guest file holds identity and
the envelope, and that means a real hostname, a real address, and a real MAC
address. Those facts are not credentials. They are reconnaissance.

A public repository is permanent. Search engines, mirrors, and forks keep a
copy after a deletion.

## Decision

The repository is public.

- Branch protection requires a pull request, the `docs / Documentation checks`
  and `docs / Secret scan` status checks, and no approval. Force push and
  deletion are off. A solo author cannot approve a personal change, so the
  approval count stays at zero.
- Secret scanning and push protection are enabled. Both are free for a public
  repository.
- `gitleaks` scans the full history in CI. The same command runs before each
  local commit, and `mise run check` includes it.
- A guest file never holds a secret. It holds no password, no token, and no
  private key. It holds a reference to a Bitwarden item instead.
- A guest file holds real addresses. The inventory needs them, and an address
  on a private network is not a credential.
- The commit author email is the public GitHub address. No other personal
  detail is added.

## Consequences

- A leaked secret is public in seconds. Push protection and the local hook are
  the only defence, and both act before the push.
- A fork keeps the history after a deletion. A revocation in Bitwarden is the
  real remedy, not a history rewrite.
- A stranger can open an issue or a pull request. The default token is
  read-only, and no workflow secret exists.
- The documentation is readable by anyone. That is the point.
- The plan costs nothing, and the protection that a private repository blocks
  becomes available.

## Rejected options

- **Private without protection.** `main` accepts a force push, and no check
  gates a merge.
- **Private on a paid plan.** It fixes the protection and keeps the content
  dark. The trade-off is a subscription, and the secret scanning of a public
  repository is the better guard for the real risk.
- **A public documentation repository and a private operation repository.**
  Two repositories to keep in step, and the guest files end up in the private
  one anyway.
- **Rewrite the history before a publication.** There is nothing to remove.
  A rewrite would only break the links.

## References

- [ADR-0005](0005-secrets-and-least-privilege.md)
- [Documentation checks](../reference/doc-checks.md)
- [Glossary](../glossary.md)
