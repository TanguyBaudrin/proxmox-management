---
type: how-to
title: Rebuild a guest
---

# Rebuild a guest

!!! warning "Not implemented in version 0.1"
    This page documents the procedure that version 0.2 will run. The playbooks
    do not exist yet.

This guide destroys one guest and creates it again from its guest file. It then
imports the application data from the latest backup. The guest loses every
change written after that backup.

## Before you start

- A successful backup younger than 26 hours.
- A documented data path for the application.
- A free maintenance window.
- The current guest file on the main branch.

## Decide the operation

| You want | Operation |
| --- | --- |
| Recover from a broken disk or a bad host | restore |
| Return to the declared state | rebuild |
| Undo one bad update | rollback |

A restore keeps the data and the old configuration. A rebuild keeps the intent
and loses the recent data. See
[ADR-0007](../adr/0007-restore-and-rebuild.md).

## Steps

1. Confirm the backup.

    ```bash
    mise run check -- --guest <name>
    ```

2. Stop the update timer. It must not run during the rebuild.
3. Export the application data. Use the documented path for the application.
4. Save the CTID. A rebuild keeps the same number.
5. Destroy the guest.

    ```bash
    mise run rebuild -- <name> --destroy-only
    ```

6. Provision the guest again.

    ```bash
    mise run rebuild -- <name>
    ```

7. Import the application data.
8. Run the health check of the application.
9. Run the check. The drift count must be zero.

    ```bash
    mise run check
    ```

10. Start the update timer again.

## If the rebuild fails

- The old guest is gone. A restore from the backup is the only path back.
- A failed import keeps the fresh guest. The data is lost from the guest, and
  the backup still holds it.
- Do not run a restore over a working guest. A restore replaces the data.

## Related

- [Provision a guest](provision-a-guest.md)
- [ADR-0007](../adr/0007-restore-and-rebuild.md)
- [ADR-0008](../adr/0008-update-policy.md)
