---
type: how-to
title: Expose a service
---

# Expose a service

!!! warning "Not implemented in version 0.1"
    This page documents the procedure that version 0.2 will run. The playbooks
    do not exist yet.

This guide publishes one guest on the Traefik host. Traefik keeps the
certificates. The repository writes one dynamic file and nothing else.

## Before you start

- A provisioned guest with a stable address.
- A DNS record that points at the Traefik host.
- The SSH target of the Traefik host in the inventory.
- The mounted directory of the file provider. The default is
  `/opt/traefik/dynamic`.

## Steps

1. Open the guest file.
2. Fill the `exposure` block.

    ```yaml
    exposure:
      host: app.example.com
      port: 8080
      scheme: http
      healthcheck: /health
    ```

3. Set the reload mechanism. Leave `watch: true` when the provider watches the
   directory.
4. Run the check. It shows the rendered file and the live file.

    ```bash
    mise run check
    ```

5. Read the rendered file. Check the host, the port, and the health check.
6. Apply the route.

    ```bash
    mise run expose -- <name>
    ```

7. Open the URL. The certificate must be valid.
8. Run the check again. The drift count must be zero.

## What the command does

1. It renders `dynamic/<name>.yml` from the guest file.
2. It validates the YAML.
3. It writes a temporary file on the Traefik host.
4. It moves the file into the mounted directory.
5. It keeps the previous file as `<name>.yml.bak`.

## If the route fails

- A syntax error is caught before the move. The live directory is untouched.
- A 404 means Traefik runs but no router matches. Check the host name.
- A 502 means the router matches and the guest does not answer. Check the port.
- A bad certificate means the host name is wrong. Traefik cannot get a
  certificate for a name that does not resolve.
- A missing route after a container recreate means the previous step used
  `docker cp`. Revert to the mounted directory. See
  [ADR-0009](../adr/0009-external-exposure.md).

## Roll back one route

1. Copy `<name>.yml.bak` over `<name>.yml`.
2. Wait for the watch, or send the reload signal.
3. Run the check.

## Related

- [ADR-0009](../adr/0009-external-exposure.md)
- [Provision a guest](provision-a-guest.md)
