---
type: reference
title: Style rules
---

# Style rules

This page gives the writing rules for this repository. The rules follow
ASD-STE100, also called Simplified Technical English. The standard is written
for English. This repository writes in English so that the standard applies.

## Where the standard applies

| Page type | Style |
| --- | --- |
| how-to | ASD-STE100 |
| tutorial | ASD-STE100 |
| reference | ASD-STE100 |
| explanation | Plain technical English |
| adr | Plain technical English |

An explanation argues. An argument needs long sentences. A procedure does not.

## The rules that a machine checks

The script `scripts/check_docs.py` enforces these rules.

| Rule | Limit | Scope |
| --- | --- | --- |
| Sentence length | 20 words | how-to, tutorial, reference |
| Sentence length | 25 words | explanation, adr, index, glossary |
| Semicolon | Forbidden | how-to, tutorial, reference |
| Contraction | Forbidden | every page |
| Banned phrase | Forbidden | every page |

A table row is exempt from the sentence limit. A code block is exempt from
every rule.

## The rules that a human checks

Read the page again and ask these questions.

1. Does each sentence hold one instruction?
2. Is the voice active?
3. Does the subject perform the action?
4. Is the verb in the approved list below?
5. Can a reader with basic English follow the steps?
6. Does each paragraph start with the point?

## Approved verbs

Use the first verb. Do not use the second.

| Use | Do not use |
| --- | --- |
| use | utilise, utilize, leverage |
| start | initiate, kick off |
| stop | terminate, kill |
| make | create, generate, produce |
| show | display, expose, surface |
| remove | delete, destroy, purge |
| check | verify, validate, ensure |
| send | transmit, push |
| get | retrieve, fetch, obtain |
| keep | retain, preserve, maintain |
| need | require, demand |
| help | assist, facilitate |

Some verbs in the second column are correct in a narrow sense. The point is
consistency. One concept uses one verb.

## Other rules

- Write one instruction in one sentence.
- Write the condition before the action.
- Use the imperative for a step.
- Use the present tense.
- Do not use a contraction.
- Do not use a marketing adjective.
- Do not use a noun cluster of more than three words.
- Put the warning before the step that needs it.
- Use a numbered list for a sequence.
- Use a bullet list for a set.
- Use a table for a comparison.

## Words to avoid

| Avoid | Write |
| --- | --- |
| simply, just | nothing, or the exact condition |
| easy, simple | the number of steps |
| in order to | to |
| please note | (remove) |
| as you can see | (remove) |
| it is important to | (rewrite as an instruction) |
| leverage | use |
| utilize | use |

## Related

- [Glossary](../glossary.md)
- [Documentation checks](doc-checks.md)
- [ADR-0006](../adr/0006-documentation-language-and-style.md)
