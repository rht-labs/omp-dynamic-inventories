# Atlassian Dynamic Inventory

## Requirements

This dynamic inventory is reliant on a [`omp-data-api`](https://github.com/rht-labs/omp-data-api) service to exist and be accessible to wherever this inventory is run from.

Alongside the `atlassian.py` is a required `atlassian.ini` configuration file which must be populated with accurate values.

## Configuration

The `atlassian.ini` file must be updated to match with your environment's values.

| Variable | Description |
| --- | --- |
| default.api_url | The api url for your instance of [`omp-data-api`](https://github.com/rht-labs/omp-data-api) |
| default.tag | The tag which all member objects belong to. For instance, if you are on a residency with the tag `super_corp_2` you would want all related customers, users, groups, and clusters to have that tag as well. This is the tag you would use in the .ini file.  |
| atlassian.url | The url for your atlassian environment. |
| atlassian.username | Your atlassian username. |
| atlassian.password | Your atlassian password. |
| confluence.source_key | The confluence key for the confluence workspace you are going to copy from. |