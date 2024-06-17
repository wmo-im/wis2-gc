# Docker

## Overview

This Docker setup uses Docker and Docker Compose to manage the following services:

- **MinIO**: GC storage backend
- **mosquitto**: Local broker that is subscribed to by the Global Broker
- **wis2-gc-management**: management service to cache data and metadata published from a WIS2 Global Broker instance
  - the default Global Broker connection is to Météo-France.  This can be modified in `pywis-pubsub.yml` to point to an alternate Global Broker

See [`wis2-gc.env`](wis2-gc.env) for default environment variable settings.

To adjust service ports, edit [`docker-compose.override.yml`](docker-compose.override.yml) accordingly.

## Running

The [`Makefile`](../Makefile) in the root directory provides options to manage the Docker Compose setup.
