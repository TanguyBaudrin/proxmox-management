---
type: reference
title: Documentation checks
---

# Documentation checks

One command runs every check.

```bash
mise run docs:check
```

The command fails when a check fails. A pull request that fails a check is not
ready.

## The checks

| Check | Tool | Blocks |
| --- | --- | --- |
| Structure and prose | `scripts/check_docs.py` | Yes |
| markdownlint | `markdownlint-cli2` | Yes |
| Spelling | `codespell` | Yes |
| Style | Vale, `styles/ste100` | Yes |
| Site build | `mkdocs build --strict` | Yes |

## What the structure check does

The script `scripts/check_docs.py` reads every page in `docs/`. It reports a
line and a rule for each failure.

| Rule | Meaning |
| --- | --- |
| `nav` | A page exists but the navigation does not list it |
| `nav-target` | The navigation lists a page that does not exist |
| `front-matter` | A page has no `type` in the front matter |
| `type` | The `type` is not in the allowed set |
| `adr-status` | An ADR has no valid status |
| `adr-date` | An ADR has no date |
| `adr-index` | The ADR index does not link the ADR |
| `glossary-unused` | A glossary term appears in no page |
| `acronym` | An uppercase token is not in the glossary |
| `synonym` | A banned variant of a canonical term appears |
| `sentence` | A sentence is too long for the page type |
| `semicolon` | A semicolon appears in a procedure |
| `contraction` | A contraction appears |
| `phrase` | A banned phrase appears |

## What the prose checks do

Vale reads the same pages and applies `styles/ste100`. The pack holds four
rules: a forbidden term, a filler word, a contraction, and a semicolon. The
style page is exempt, because it quotes the forbidden forms on purpose.

`codespell` catches a typo that a dictionary misses, such as a swapped letter
in a code sample.

## What a machine cannot check

A machine cannot judge these points. A reviewer judges them.

- One instruction per sentence
- Active voice
- A warning that comes before the step
- A definition that a reader understands
- A decision that belongs in an ADR

## Fix a failure

1. Read the reported path and line.
2. Change the page, not the rule.
3. Run `mise run docs:check` again.
4. If the rule is wrong, change the rule in the same commit and say why.

## Run one check

```bash
mise run docs:structure   # scripts/check_docs.py
mise run docs:prose       # vale docs
mise run docs:spell       # codespell
mise run docs:style       # markdownlint-cli2
mise run docs:build       # mkdocs build --strict
```

## Related

- [Style rules](style-ste100.md)
- [Glossary](../glossary.md)
