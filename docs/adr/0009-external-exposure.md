---
type: adr
title: "0009 External exposure"
status: accepted
date: 2026-11-10
---

# 0009 External exposure

## Context

Traefik runs on another host and terminates TLS. It reads a file provider. The
repository must publish a new service without owning the Traefik host.

A container filesystem is ephemeral. A file written with `docker cp` vanishes
when the container is recreated, and the route disappears with it. Nothing
warns the operator.

A dynamic configuration file that holds a syntax error can break every route,
not only the new one.

## Decision

The repository writes a file into a directory on the Traefik host. That
directory is mounted into the container. The default path is
`/opt/traefik/dynamic`.

- The exposure layer needs three facts about the host: the SSH target, the
  mounted directory, and the reload mechanism.
- The default reload mechanism is the file watch of the provider. If the watch
  is off, the mechanism is a signal to the container, and the guest file
  records which signal.
- One file per guest. A change to one service never rewrites another file.
- The write is atomic. The repository writes a temporary file, validates it,
  then moves it into place on the same filesystem.
- The previous file stays as a backup for one rollback.
- The repository never calls `docker cp`.
- Traefik keeps the certificates. The repository writes routers and services
  only.

## Consequences

- A recreate of the Traefik container keeps every route.
- A bad file is rejected before it reaches the live directory.
- One rollback step exists: restore the previous file and let the watch reload
  it.
- The controller needs SSH access to a host outside PVE. That host is a
  second entry in the inventory.

## Rejected options

- **`docker cp` into the running container.** The route dies at the next
  recreate, silently.
- **The Docker label provider.** It needs the Docker socket on the same host
  and moves the routing data into a container definition.
- **Manage Traefik in this repository.** It adds a third operating system and
  a certificate lifecycle to the scope.
- **One large dynamic file.** Two guests cannot change it at the same time, and
  one syntax error breaks every route.

## References

- [ADR-0001](0001-scope-and-layers.md)
- [ADR-0005](0005-secrets-and-least-privilege.md)
- [How to expose a service](../how-to/expose-a-service.md)
