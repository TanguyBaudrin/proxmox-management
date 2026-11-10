---
type: adr
title: "0006 Documentation language and style"
status: accepted
date: 2026-11-10
---

# 0006 Documentation language and style

## Context

The first plan was to write the documentation in French and to apply
ASD-STE100. The two goals contradict each other. ASD-STE100 is a controlled
form of English. It defines a dictionary of approved words and a set of
grammar rules. The standard does not exist in French.

The repository needs one language, because a mixed corpus creates two
vocabularies and two reading speeds.

## Decision

- The documentation is written in English.
- ASD-STE100 applies to the how-to guides, the tutorials, and the reference
  pages. Those pages describe a procedure or a fact.
- Plain technical English applies to the explanations and the ADRs. Those
  pages argue, and an argument needs a longer sentence.
- A machine enforces the mechanical subset: sentence length, semicolons,
  contractions, and banned phrases.
- A reviewer enforces the rest: one instruction per sentence, active voice, and
  a warning before the step.
- One concept has one term. The glossary is the list, and
  `scripts/terminology.json` is the enforcement.
- The repository does not claim full conformance. It claims a documented
  subset and a review checklist.

## Consequences

- A French device name stays untouched. The prose around it is English.
- The repository joins the other repositories of the same author, which are
  already in English.
- A French reader loses some speed. The glossary and the short sentences
  compensate.
- A new rule needs a test in `scripts/check_docs.py` or a Vale rule. A rule
  that nothing checks is a wish.

## Rejected options

- **French documentation.** ASD-STE100 cannot apply, and the tooling for French
  prose is weaker.
- **Two languages.** Two vocabularies, two glossaries, and one reader who
  reads the wrong page.
- **Full conformance to ASD-STE100.** The standard needs a dictionary and a
  trained reviewer. A partial claim that a machine enforces is honest.

## References

- [Style rules](../reference/style-ste100.md)
- [Documentation checks](../reference/doc-checks.md)
- [Glossary](../glossary.md)
