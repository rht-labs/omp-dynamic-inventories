# Identity Dynamic Inventory

## Requirements

This dynamic inventory is reliant on a [`omp-data-api`](https://github.com/rht-labs/omp-data-api) service to exist and be accessible to wherever this inventory is run from.

Alongside the `identity.py` specific environment variables must be defined (as explained below).

## Configuration

The following environment variables must be defined before running the dynamic inventory.

| Environment Variable | Description |
| --- | --- |
| API_URL | The api url for your instance of [`omp-data-api`](https://github.com/rht-labs/omp-data-api) |
| TAG | The tag you want to pull users and groups from.  |
| IDENTITY_PROVIDERS | The list of identity providers you want to populate users for. (example: IDENTITY_PROVIDERS=atlassian,idm) |