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
# USERNAME - The email username from which you want to send notifications from 
# PASSWORD - The password for said username
api_url = os.environ['API_URL']
my_tag = os.environ['TAG']
username = os.environ['EMAIL_USERNAME']
password = os.environ['EMAIL_PASSWORD']

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

        mail = {
            "mail": {
                "host": "smtp.gmail.com",
                "port":"465",
                "username": username,
                "password": password,
                "to": self.get_send_addresses(r_users),
                "subject": "Testing",
                "body":"<html><body><h1>Testing</h1></body></html>",
                "subtype": "html"
            }
        }

        self.inventory = {'all': { "vars": mail}}


    def return_value_with_tags(self, url, tag, my_tag, value):
        r = requests.get(url + '/' + tag + ',' + my_tag).json()
        if not r:
            return ''
        else:
            return r[0][value]

    def get_send_addresses(self, user_request):
        send_addresses = []
        for user in user_request:
            send_addresses.append(user['email'])

        return send_addresses

    def parse_cli_args(self):
        parser = argparse.ArgumentParser(
            description='Produce an Ansible Inventory from a file')
        parser.add_argument('--list', action='store_true')
        parser.add_argument('--host', action='store')
        self.args = parser.parse_args()


Inventory()
