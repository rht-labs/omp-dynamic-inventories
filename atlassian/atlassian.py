#!/usr/bin/env python

import argparse
import requests
import datetime
from datetime import date

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
            "jira": {
                "lead": self.return_value_with_tags(users_url, 'atlassian_lead', my_tag, 'email').split('@')[0],
                "project": {
                    "name": self.return_value_with_tags(residencies_url, my_tag, my_tag, 'name'),
                    "key": self.generate_key(),
                    "category_description": "residency",
                    "description": "Project for " + self.return_value_with_tags(residencies_url, my_tag, my_tag, 'name'),
                    "category_name": "residency2"
                },
                "groups": self.get_group_roles(my_tag),
                "permission_scheme": {
                    "name": self.generate_key(),
                    "description": "permission scheme for" + self.return_value_with_tags(residencies_url, my_tag, my_tag, 'name')
                }
            },
            "confluence": {
                "source": {
                    "key": os.environ['CONFLUENCE_SOURCE_KEY'],
                },
                "destination": {
                    "key": self.generate_key(),
                    "name": self.return_value_with_tags(residencies_url, my_tag, my_tag, 'name'),        
                    "description": "Residency wiki for " + self.return_value_with_tags(residencies_url, my_tag, my_tag, 'name')
                }
            }
        }
        

        atlassian = {
            "atlassian": atlassian,
        }

        self.inventory = {'all': { "vars": atlassian}}

    def get_group_roles(self, tag):
        atlassian_roles = []

        atlassian_admins = requests.get(groups_url + '/' + tag + ',' + "atlassian_admin").json()
        atlassian_members = requests.get(groups_url + '/' + tag + ',' + "atlassian_team_member").json()
        atlassian_viewers = requests.get(groups_url + '/' + tag + ',' + "atlassian_viewer").json()

        for admin in atlassian_admins:
            atlassian_roles.append({
                "name": admin['group_name'],
                "role": "admin"})
                
        for member in atlassian_members:
            atlassian_roles.append({
                "name": member["group_name"],
                "role": "member"})

        for viewer in atlassian_viewers:
            atlassian_roles.append({
                "name": viewer["group_name"],
                "role": "read"})
                
        return atlassian_roles

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
