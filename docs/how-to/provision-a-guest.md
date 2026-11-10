---
type: how-to
title: Provision a guest
---

# Provision a guest

!!! warning "Not implemented in version 0.1"
    This page documents the procedure that version 0.2 will run. The playbooks
    do not exist yet.

This guide creates one guest from a guest file. It assumes the toolchain is
installed and the vault is unlocked.

## Before you start

- A node that answers over SSH.
- An `ansible@pve` token in the vault.
- A template for the chosen operating system on the node.
- A free address in the DHCP scope of the EdgeRouter.
- A reviewed entry in `scripts/lock.yml` for the application.

## Steps

1. Create the file `guests/<name>.yml`. Copy the nearest guest file and change
   the values.
2. Set the identity fields: `ctid`, `hostname`, `node`, and `address`.
3. Set the envelope fields: `cores`, `memory`, `disk`, `tags`, and `onboot`.
4. Set the application fields: `app`, `template`, and `healthcheck`.
5. Add the exposure field. Leave it empty when the guest needs no route.
6. Add the guest to `inventory/hosts.yml` under the `guests` group.
7. Run the check.

    ```bash
    mise run check
    ```

8. Read the plan. It lists one create, one DHCP reservation, and one route.
9. Run the provision.

    ```bash
    mise run provision -- <name>
    ```

10. Read the log. The last line reports the CTID and the address.
11. Run the check again. The drift count must be zero.
12. Open the service. Use the address from the log.

## What the command does

| Step | Actor | Write |
| --- | --- | --- |
| 1 | Ansible | The DHCP reservation |
| 2 | The engine | The container and the application |
| 3 | Ansible | The envelope, then a check |
| 4 | Ansible | The exposure route |

## If the command fails

- A failed reservation stops the run. Fix the EdgeRouter first.
- A failed provision leaves no guest. Read the log path from the output.
- A failed reconcile keeps the guest. The envelope is wrong. Run the check.
- A failed route keeps the service local. Fix the file and run the route step
  alone.

## After the run

- Record the CTID in the pull request.
- Add the backup job. See [ADR-0007](../adr/0007-restore-and-rebuild.md).
- Add the update timer. See [ADR-0008](../adr/0008-update-policy.md).

## Related

- [Rebuild a guest](rebuild-a-guest.md)
- [Expose a service](expose-a-service.md)
- [ADR-0003](../adr/0003-no-state-pve-is-the-source-of-truth.md)
