#!/usr/bin/env python

import argparse
import requests
import datetime
from datetime import date
from configparser import ConfigParser

import os


try:
    import json
except ImportError:
    import simplejson as json


# Define the following environment variables:
# API_URL - The base url for the omp-data-api
# TAG - The tag you want to pull users and groups from.
# CONFLUENCE_SOURCE_KEY - The key of the confluence workspace to copy from.
# ATLASSIAN_URL - The URL to your atlassian workspace (in the form of https://<workspace>.atlassian.net)
# ATLASSIAN_USERNAME - The username for your Atlassian account
# ATLASSIAN_PASSWORD - The api token or password for your Atlassian account
api_url = os.environ['API_URL']
my_tag = os.environ['TAG']

users_url = api_url + "/users"
groups_url = api_url + "/groups"
customers_url = api_url + "/customers"
clusters_url = api_url + "/clusters"
residencies_url = api_url + "/residencies"


class Inventory(object):

    def __init__(self):

        self.parse_cli_args()

        self.inventory = {}

        if self.args.list:
            self.handle_list()
        elif self.args.host != None:
            self.handle_host()

        print(json.dumps(self.inventory))

    def handle_list(self):

        my_tag_users = users_url + '/' + my_tag
        r_users = requests.get(my_tag_users).json()

        atlassian = {
            "url": os.environ['ATLASSIAN_URL'],
            "username": os.environ['ATLASSIAN_USERNAME'],
            "password": os.environ['ATLASSIAN_PASSWORD'],
            "users": [],
            "groups": [],
            "jira": {
                "admin_group": self.return_value_with_tags(groups_url, 'atlassian_admin', my_tag, 'group_name'),
                "lead": self.return_value_with_tags(users_url, 'atlassian_lead', my_tag, 'user_name'),
                "core_team": self.return_value_with_tags(groups_url, 'atlassian_core_group', my_tag, 'group_name'),
                "project": {
                    "name": self.return_value_with_tags(residencies_url, my_tag, my_tag, 'name'),
                    "key": self.generate_key(),
                    "description": "Project for " + self.return_value_with_tags(residencies_url, my_tag, my_tag, 'name'),
                    "category_name": "residency"
                },
                "group": {
                    "team_member": self.return_value_with_tags(groups_url, 'atlassian_team_member', my_tag, 'group_name'),
                    "viewer": self.return_value_with_tags(groups_url, 'atlassian_viewer', my_tag, 'group_name'),
                    "lead": self.return_value_with_tags(groups_url, 'atlassian_group_lead', my_tag, 'group_name')
                },
                "permission_scheme": {
                    "name": self.generate_key(),
                    "description": "permission scheme for" + self.return_value_with_tags(residencies_url, my_tag, my_tag, 'name')
                }
            },
            "confluence": {
                "source": {"key": os.environ['CONFLUENCE_SOURCE_KEY']},
                "destination": {
                    "key": self.generate_key(),
                    "name": self.return_value_with_tags(residencies_url, my_tag, my_tag, 'name'),
                    "description": "Residency wiki for " + self.return_value_with_tags(residencies_url, my_tag, my_tag, 'name')
                }
            }
        }

        all_valid_groups = []

        for user in r_users:
            valid_groups = []
            for group in self.check_if_valid(user, 'tags', 'list'):
                valid_groups.append(self.does_group_with_tag_exist(
                    group, valid_groups))

            valid_groups = [value for value in valid_groups if value != None]

            atlassian['users'].append({
                "first_name": self.check_if_valid(user, 'first_name'),
                "last_name": self.check_if_valid(user, 'last_name'),
                "email": self.check_if_valid(user, 'email'),
                "state": "present",
                "groups": valid_groups
            })

            all_valid_groups = list(set(valid_groups + all_valid_groups))

        atlassian['groups'] = all_valid_groups

        self.inventory = atlassian

    def does_group_with_tag_exist(self, tag, groups_list):
        r_groups = requests.get(groups_url + '/' + tag + ',' + my_tag).json()

        if r_groups:
            for group in r_groups:
                if 'group_name' in group.keys():
                    return group['group_name']
                else:
                    return None

    def return_value_with_tags(self, url, tag, my_tag, value):
        r = requests.get(url + '/' + tag + ',' + my_tag).json()
        if not r:
            return ''
        else:
            return r[0][value]

    def handle_host(self):
        self.inventory.update(
            {"_meta": {"hostvars": {'127.0.0.1': {'var2': 'bar'}}}})

    def check_if_valid(self, dictionary, value, value_type='string'):
        if value in dictionary.keys():
            return dictionary[value]
        else:
            if value_type == 'list':
                return []
            else:
                return ''

    def generate_key(self):
        return (self.return_value_with_tags(customers_url, my_tag, my_tag, 'customer_name')[0:3] + date.today().strftime("%b%y")).upper()

    def parse_cli_args(self):
        parser = argparse.ArgumentParser(
            description='Produce an Ansible Inventory from a file')
        parser.add_argument('--list', action='store_true')
        parser.add_argument('--host', action='store')
        self.args = parser.parse_args()


Inventory()
