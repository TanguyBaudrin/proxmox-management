---
type: adr
title: "0007 Restore and rebuild"
status: accepted
date: 2026-11-10
---

# 0007 Restore and rebuild

## Context

Two different operations used to share one name. The difference matters.

A backup holds reality. It holds the guest as it was at 03:00, with the files
and the application version of that moment. A guest file holds intent. It holds
the guest that the repository wants.

A restore puts reality back. It never converges to intent. If the two words
merge, then a rebuild becomes a silent rollback to yesterday.

The rollback plan for this repository is a daily backup on a NAS volume,
mounted over NFS on the node.

## Decision

The repository uses two verbs.

**restore** is disaster recovery. It puts a backup back under the same CTID.
It does not enforce the desired state. A `check` after a restore will report
drift, and that report is correct.

**rebuild** is intent. It destroys the guest, provisions it again from the
guest file with the pinned procedure, then imports the application data from
the most recent backup. A `check` after a rebuild must report zero drift. That
report is the acceptance test.

The backup policy is part of the same decision.

- One daily `vzdump` job writes to the NAS volume over NFS.
- Retention is seven daily copies and four weekly copies.
- A container on NFS storage is likely to use suspend mode. Expect a short
  freeze at 03:00. Confirm the mode on the node and write the result here.
- Backups sit on a different physical device from the guests. That is the
  reason for the NAS.
- `check` asserts backup freshness for every managed guest. A successful backup
  must be younger than 26 hours. A failed mount therefore fails the check.
- No snapshot is taken per change. The backup is the rollback.

## Consequences

- A rebuild loses the data written since the last backup. The data import is a
  documented step per application, and it needs its own path.
- A restore is fast and keeps the data. It does not fix a configuration
  mistake.
- A silent backup failure becomes a visible check failure within one day.
- A container backup freezes the guest for a short time each night.

## Rejected options

- **A snapshot before each change.** It protects one change and not the daily
  update. It also needs storage that supports snapshots, and a directory on
  NFS does not.
- **Restore as the rebuild path.** It restores the problem that the rebuild was
  meant to remove.
- **Local backups on the node.** One disk failure removes the guests and the
  copies together.
- **No freshness assertion.** A mount that fails at 03:00 fails silently until
  the day it matters.

## References

- [ADR-0008](0008-update-policy.md)
- [How to rebuild a guest](../how-to/rebuild-a-guest.md)
- [Glossary](../glossary.md)
