---
type: adr
title: "0011 Documentation engine and publishing"
status: accepted
date: 2026-11-10
---

# 0011 Documentation engine and publishing

## Context

The site was built with MkDocs and its Material theme. The Material team
announces the end of that theme on 5 May 2027. Zensical comes from the same
team, and it reads the same configuration file.

The documentation is public. See
[ADR-0010](0010-public-repository-and-secret-hygiene.md). A public site adds no
exposure that the repository does not already have.

## Decision

- Zensical builds the site. It replaces `mkdocs-material` in
  `docs/requirements.txt`.
- The configuration stays in `mkdocs.yml`. Zensical reads that file, and MkDocs
  still builds from it. The file name is the only remnant of MkDocs, and it
  keeps a second builder available.
- `zensical build --strict` gates every change. Strict mode stops the build on
  a broken link.
- A push to `main` publishes the site to GitHub Pages. The publish job runs
  only after the two checks pass.
- The build travels through an artifact. Zensical has no `gh-deploy` command,
  and a bot commit to a second branch is more work to protect.
- `site_url` holds the address, so the sitemap and the canonical links are
  correct.
- The site holds the documentation only. It holds no secret and no operational
  data.

## Consequences

- Zensical is on the 0.x line. A breaking change can arrive, and the pin in
  `docs/requirements.txt` holds the version.
- The theme changes. Zensical renders its modern variant, and the content and
  the navigation do not change.
- A broken internal link fails the pull request. The reader never sees the
  broken page.
- A failed check stops the publication. The site keeps the previous version.
- The site is public. That matches ADR-0010.

## Rejected options

- **Stay on Material until 2027.** It postpones a migration that costs one
  afternoon today.
- **Move the configuration to `zensical.toml` now.** It removes the MkDocs
  fallback, and upstream advises the gradual path.
- **Publish from a `gh-pages` branch.** It needs a bot commit and a second
  protected branch.
- **Host the site elsewhere.** It adds an account, a certificate, and a third
  transfer path.

## References

- [ADR-0010](0010-public-repository-and-secret-hygiene.md)
- [Documentation checks](../reference/doc-checks.md)
