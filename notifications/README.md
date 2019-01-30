# Notifications Dynamic Inventory

## Requirements

This dynamic inventory is reliant on a [`omp-data-api`](https://github.com/rht-labs/omp-data-api) service to exist and be accessible to wherever this inventory is run from.

Alongside the `notifications.py` specific environment variables must be defined (as explained below).

## Configuration

The following environment variables must be defined before running the dynamic inventory.

| Environment Variable | Description |
| --- | --- |
| API_URL | The api url for your instance of [`omp-data-api`](https://github.com/rht-labs/omp-data-api) |
| TAG | The tag which all member objects belong to. For instance, if you are on a residency with the tag `super_corp_2` you would want all related customers, users, groups, and clusters to have that tag as well. This is the tag you would use in the .ini file.  |
| EMAIL_CONTENT_URL | A url which points to a yaml file containing the content for the email |
| EMAIL_USERNAME| The username of the account that you wish to send your messages from, must be fully qualified |
| EMAIL_PASSWORD| Password of account that you wish to send emails from |

## Exaple email content yaml file
```yaml
---

title: "This is an example title"

body: |
  This is an example body.
```