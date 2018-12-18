# Atlassian Dynamic Inventory

## Requirements

This dynamic inventory is reliant on a [`omp-data-api`](https://github.com/rht-labs/omp-data-api) service to exist and be accessible to wherever this inventory is run from.

Alongside the `atlassian.py` specific environment variables must be defined (as explained below).

## Configuration

The following environment variables must be defined before running the dynamic inventory.

| Environment Variable | Description |
| --- | --- |
| API_URL | The api url for your instance of [`omp-data-api`](https://github.com/rht-labs/omp-data-api) |
| TAG | The tag which all member objects belong to. For instance, if you are on a residency with the tag `super_corp_2` you would want all related customers, users, groups, and clusters to have that tag as well. This is the tag you would use in the .ini file.  |
| ATLASSIAN_URL | The url for your atlassian environment. |
| ATLASSIAN_USERNAME | Your atlassian username. |
| ATLASSIAN_PASSWORD | Your atlassian password or api token. |
| CONFLUENCE_SOURCE_KEY | The confluence key for the confluence workspace you are going to copy from. |
