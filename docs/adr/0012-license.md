---
type: adr
title: "0012 License"
status: accepted
date: 2026-11-10
---

# 0012 License

## Context

The repository is public. See
[ADR-0010](0010-public-repository-and-secret-hygiene.md). Until now it granted
no right. A public repository without a license allows a reader to view it and
to fork it on GitHub, and nothing more.

The content is documentation and configuration. A reader wants to copy a guest
file, to adapt a playbook, or to reuse a check in another repository. Without a
license, that reader asks for permission, or takes a risk.

The author wants a free use, a free change, and a visible credit.

## Decision

The repository is under the MIT license. The file `LICENSE` holds the text,
and the copyright line names Tanguy Baudrin and the year 2026.

A copy, a change, and a commercial use are allowed. The copyright notice and
the permission notice must travel with every copy and every substantial part.

A contribution arrives under the same terms. Nobody signs a second agreement.

The documentation site shows the license in the footer.

## Consequences

- A reader can reuse the content at once. No request, no form.
- A copy that drops the notice breaks the terms. That is the only condition.
- The grant is permanent for a published version. A later change of license
  governs the later versions only.
- The license covers the text as well as the configuration. A dedicated
  content license is possible later, and it needs a new ADR.
- No warranty. A reader who runs a playbook on a production node carries the
  risk.

## Rejected options

- **No license.** A public repository grants nothing beyond what the GitHub
  terms allow. That contradicts the intent.
- **Apache-2.0.** It adds an explicit patent grant and a notice file. That
  protection matters for a large software project, and it costs more reading
  for a small one.
- **Creative Commons Attribution 4.0 for the documentation, MIT for the
  configuration.** Two texts and two boundaries, and the reader must guess
  which one covers a YAML file.
- **A custom clause for a stronger credit.** A non-standard term frightens a
  company lawyer, and it complicates a reuse that the author wants simple.

## References

- [ADR-0010](0010-public-repository-and-secret-hygiene.md)
- [Glossary](../glossary.md)
