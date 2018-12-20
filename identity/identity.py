#!/usr/bin/env python

import argparse
import requests

import os


try:
    import json
except ImportError:
    import simplejson as json


# Define the following environment variables:
# API_URL - The base url for the omp-data-api
# TAG - The tag you want to pull users and groups from.
# IDENTITY_PROVIDERS - The list of identity providers you want to populate users for. (example: IDENTITY_PROVIDERS=atlassian,idm)
api_url = os.environ['API_URL']
my_tag = os.environ['TAG']
identity_provider_list = os.environ.get(
    'IDENTITY_PROVIDERS', 'atlassian,idm').split(',')

# If desired, you can set a different endpoint using these environment variables.
users_url = api_url + os.environ.get("USERS_ENDPOINT", "/users")
groups_url = api_url + os.environ.get("GROUPS_ENDPOINT", "/groups")


class Inventory(object):

    def __init__(self):

        self.parse_cli_args()

        self.inventory = {}

        if self.args.list:
            self.handle_list()

        print(json.dumps(self.inventory))

    def handle_list(self):

        r_users = requests.get(users_url + '/' + my_tag).json()
        r_groups = requests.get(groups_url + '/' + my_tag).json()

        identity_data = {
            "targets": identity_provider_list,
            "users": [],
            "groups": []
        }

        for user in r_users:
            if not set(self.check_if_valid(user, 'identity_providers')).isdisjoint(identity_provider_list):
                identity_data['users'].append({
                    "first_name": self.check_if_valid(user, 'first_name'),
                    "last_name": self.check_if_valid(user, 'last_name'),
                    "user_name": self.check_if_valid(user, 'email').split('@')[0],
                    "email": self.check_if_valid(user, 'email'),
                    "targets": self.check_if_valid(user, 'identity_providers'),
                    "tags": self.check_if_valid(user, 'tags')
                })
        for group in r_groups:
            if not set(self.check_if_valid(group, 'tags')).isdisjoint(identity_provider_list):
                group_name = self.check_if_valid(group, 'group_name')
                targets = []
                for tag in self.check_if_valid(group, 'tags'):
                    if tag in identity_provider_list:
                        targets.append(tag)
                members = []
                for user in identity_data['users']:
                    if group_name in self.check_if_valid(user, 'tags'):
                        members.append(user['user_name'])
                identity_data['groups'].append({
                    "name": group_name,
                    "targets": targets,
                    "members": members
                })

        identities = {
            "identities": identity_data
        }

        self.inventory = {
            'all': {"vars": identities}}

    def check_if_valid(self, dictionary, value, value_type='string'):
        if value in dictionary.keys():
            return dictionary[value]
        else:
            if value_type == 'list':
                return []
            else:
                return ''

    def parse_cli_args(self):
        parser = argparse.ArgumentParser(
            description='Produce an Ansible Inventory for Identities')
        parser.add_argument('--list', action='store_true')
        parser.add_argument('--host', action='store')
        self.args = parser.parse_args()


Inventory()
