---
type: adr
title: "0008 Update policy"
status: accepted
date: 2026-11-10
---

# 0008 Update policy

## Context

An application script carries its own update function. The function checks the
upstream release and installs the newest one. It does not accept a version
argument.

That creates a tension. A cron job that runs inside the guest cannot pin an
application version, because the script does not offer one. A pinned
application version therefore needs a human on a laptop. A cron job that waits
for a human is not a cron job.

The update path is also the riskiest actor in the system. It runs as root, it
runs unattended, and it changes the application without a commit.

## Decision

Ansible owns the envelope. Cron owns the execution.

- Ansible writes a wrapper and a systemd timer into the guest.
- The wrapper pins the engine and the application script to the commit that
  provision recorded. It exports `COMMUNITY_SCRIPTS_CORE_DIR` and runs the
  `ct/` file from the cache.
- The application tracks its upstream release. The repository does not pin an
  application version, and this ADR records that trade-off.
- Before the update, the wrapper starts one `vzdump` of the guest. After the
  update, it runs a health check on the local service.
- The wrapper writes one line per event to a fixed path. A future log shipper
  reads that path. Until then, the container log is the only record.
- A failed update sends no automatic restore. A restore loses data. The
  operator runs `mise run rollback -- <guest>`.
- `check` reports two facts per guest: the installed commit against
  `scripts/lock.yml`, and the result of the last update.

## Consequences

- An application version moves without a commit. The repository records the
  procedure and the result, not the version.
- A failed update stays failed until a human sees it. The check makes it
  visible at the next run.
- A pre-update backup doubles the backup count on the update night. Retention
  covers it.
- The wrapper must know the application health check. The guest file holds
  that fact.

## Rejected options

- **Ansible runs the update from the controller.** It needs a laptop at 03:00,
  or a laptop at 09:00 with stale packages.
- **Pin the application version.** The script does not accept one. It would
  also remove the reason for the cron.
- **Automatic restore on failure.** It replaces a broken application with lost
  data, without a human decision.
- **No update at all.** The security patches stay behind, and the drift grows.

## References

- [ADR-0004](0004-script-supply-chain.md)
- [ADR-0007](0007-restore-and-rebuild.md)
- [How to rebuild a guest](../how-to/rebuild-a-guest.md)
